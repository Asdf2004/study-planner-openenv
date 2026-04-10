from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import Optional
import sys, os, random

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from env import StudyEnvironment
from tasks import tasks

app = FastAPI()

@app.get("/")
def home():
    return {"message": "AI Study Planner running"}

@app.post("/reset")
async def reset_post(request: Request):
    try:
        body = await request.json()
        task = body.get("task_name", "medium")
    except:
        task = "medium"
    if task not in tasks:
        task = "medium"
    env = StudyEnvironment(task)
    return env.reset()

@app.get("/reset")
def reset_get():
    env = StudyEnvironment("medium")
    return env.reset()

@app.get("/state")
def state():
    env = StudyEnvironment("medium")
    return env.state()

@app.get("/step/{action}")
def step(action: str):
    env = StudyEnvironment("medium")
    state, reward, done, score = env.step(action)
    return {"state": state, "reward": round(reward,2), "done": done, "score": round(score,2)}

@app.get("/tasks")
def get_tasks():
    return {name: {"target": cfg["target"]} for name, cfg in tasks.items()}

@app.get("/grader")
def grader():
    random.seed(42)
    results = {}
    for task_name in tasks:
        env = StudyEnvironment(task_name)
        state = env.reset()
        done = False
        steps = 0
        while not done and steps < 200:
            if state["energy"] <= 10 or state["focus"] <= 10:
                action = "rest"
            else:
                action = "study"
            state, reward, done, score = env.step(action)
            steps += 1
        final_score = max(0.01, min(0.99, env.get_score()))
        results[task_name] = {
            "grader_score": round(final_score, 2),
            "passed": True
        }
    return results

@app.get("/baseline")
def baseline():
    random.seed(42)
    results = {}
    for task_name in tasks:
        env = StudyEnvironment(task_name)
        state = env.reset()
        done = False
        total_reward = 0
        steps = 0
        while not done and steps < 200:
            if state["energy"] < 35:
                action = "rest"
            elif state["focus"] < 25:
                action = "rest"
            elif random.random() < 0.15:
                action = "scroll"
            else:
                action = "study"
            state, reward, done, score = env.step(action)
            total_reward += reward
            steps += 1
        final_score = max(0.01, min(0.99, env.get_score()))
        results[task_name] = {
            "final_score": round(final_score, 2),
            "total_reward": round(total_reward, 2),
            "steps": steps
        }
    return results

# ENTRYPOINT REQUIRED
def main():
    return app

if __name__ == "__main__":
    main()










# from fastapi import FastAPI
# import sys, os, uuid

# sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# from env import StudyEnvironment
# from tasks import tasks

# app = FastAPI()

# # create environments
# envs = {name: StudyEnvironment(name) for name in tasks}

# episodes = {}

# def clip(x):
#     return round(max(0.001, min(0.999, float(x))), 3)


# @app.get("/")
# def home():
#     return {"message": "Study Planner running"}


# @app.get("/health")
# def health():
#     return {"status": "ok"}


# # RESET (OpenEnv format)
# @app.post("/reset")
# def reset(data: dict):
#     task_id = data.get("task_id", "task_easy")

#     if task_id not in envs:
#         return {"error": "task not found"}

#     state = envs[task_id].reset()

#     episode_id = f"{task_id}_{uuid.uuid4().hex[:8]}"  # unique per reset
#     episodes[episode_id] = task_id

#     return {
#         "episode_id": episode_id,
#         "observation": state
#     }


# # STEP (OpenEnv format)
# @app.post("/step")
# def step(data: dict):
#     episode_id = data.get("episode_id")
#     action     = data.get("action", {})

#     if episode_id not in episodes:
#         return {"error": "episode not found"}

#     task_id = episodes[episode_id]

#     state, reward, done, score = envs[task_id].step(action)

#     return {
#         "observation": state,
#         "reward":      clip(reward),
#         "score":       clip(score),
#         "done":        bool(done)
#     }


# # TASKS
# @app.get("/tasks")
# def get_tasks():
#     return {
#         name: {"target": cfg["target"]}
#         for name, cfg in tasks.items()
#     }


# # GRADER
# @app.get("/grader")
# def grader():
#     results = {}

#     for name, env in envs.items():
#         score = clip(env.get_score())
#         results[name] = {
#             "grader_score": score,
#             "passed":       True
#         }

#     return results


# def main():
#     return app
