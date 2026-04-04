import os
import random
from env import StudyEnvironment

# Required environment variables (validator compliance)
API_BASE_URL = os.getenv("API_BASE_URL","not_used")
MODEL_NAME = os.getenv("MODEL_NAME","baseline")
HF_TOKEN = os.getenv("HF_TOKEN")

# Reproducible results
random.seed(42)

print("[START] baseline_inference")

env = StudyEnvironment("hard")

state = env.reset()

done = False

total_reward = 0

steps = 0

while not done:

    if state["energy"] < 30:
        action = "rest"

    elif state["focus"] < 30:
        action = "rest"

    elif random.random() < 0.1:
        action = "scroll"

    else:
        action = "study"

    state, reward, done, score = env.step(action)

    total_reward += reward

    steps += 1

    print(f"[STEP] step={steps} action={action} reward={round(reward,2)} score={round(score,2)}")

print("[END]")

print("final_score:",round(env.get_score(),2))
print("total_reward:",round(total_reward,2))
print("steps:",steps)
