import random
from env import StudyEnvironment

# reproducible baseline
random.seed(42)

# difficulty (easy / medium / hard)
env = StudyEnvironment("hard")

state = env.reset()

done = False

total_reward = 0

print("Starting Environment")
print("---------------------")

while not done:

    # baseline decision policy
    if state["energy"] < 35:

        action = "rest"

    elif state["focus"] < 25:

        action = "rest"

    elif random.random() < 0.15:

        action = "scroll"

    else:

        action = "study"


    print("Action taken:", action)

    state, reward, done, info = env.step(action)

    total_reward += reward


    print("State:", state)

    print("Reward:", reward)

    print("Score:", round(info["score"],2))

    print("---------------------")


print("Task finished")

print("Total reward:", round(total_reward,2))

print("Final score:", round(env.get_score(),2))

print("Steps taken:", state["time"])

print("Final progress:", round(state["progress"],2))

print("Final energy:", state["energy"])