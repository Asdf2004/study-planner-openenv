import os
from openai import OpenAI
from env import StudyEnvironment

print("[START] LLM agent")

# Required environment variables (Hackathon requirement)
API_BASE_URL = os.environ["API_BASE_URL"]
API_KEY = os.environ["API_KEY"]
MODEL_NAME = os.environ["MODEL_NAME"]

# Initialize LLM client (IMPORTANT)
client = OpenAI(
    base_url=API_BASE_URL,
    api_key=API_KEY
)

env = StudyEnvironment("medium")

state = env.reset()

done = False
total_reward = 0
steps = 0

while not done:

    prompt = f"""
    You are an AI study planner.

    Current state:
    Energy: {state['energy']}
    Focus: {state['focus']}
    Progress: {state['progress']}
    Time: {state['time']}

    Possible actions:
    study
    rest
    scroll

    Return only one word action.
    """

    # LLM CALL (this is what validator checks)
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role":"user","content":prompt}
        ],
        temperature=0
    )

    action = response.choices[0].message.content.strip().lower()

    if action not in ["study","rest","scroll"]:
        action = "study"

    state,reward,done,score = env.step(action)

    total_reward += reward
    steps += 1

    print(f"[STEP] {steps} action={action} reward={round(reward,2)} score={round(score,2)}")

print("[END]")

print("final_score:",round(env.get_score(),2))
print("total_reward:",round(total_reward,2))
print("steps:",steps)
