import random
from env import StudyEnvironment
from tasks import tasks

# reproducible baseline
random.seed(42)

for task_name in tasks:
    print(f"\n{'='*30}")
    print(f"Starting Task: {task_name.upper()}")
    print("---------------------")

    env = StudyEnvironment(task_name)
    state = env.reset()
    done = False
    total_reward = 0

    while not done:
        if state["energy"] < 35:
            action = "rest"
        elif state["focus"] < 25:
            action = "rest"
        elif random.random() < 0.15:
            action = "scroll"
        else:
            action = "study"

        print("Action taken:", action)
        state, reward, done, score = env.step(action)
        total_reward += reward

        print("State:", state)
        print("Reward:", reward)
        print("Score:", round(score, 2))
        print("---------------------")

    print("Task finished")
    print("Total reward:", round(total_reward, 2))
    final_score = max(0.01, min(0.99, env.get_score()))
    print("Final score:", round(final_score, 2))
    print("Steps taken:", state["time"])
    print("Final progress:", round(state["progress"], 2))
    print("Final energy:", state["energy"])
