from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

class ResetRequest(BaseModel):
    task_name: Optional[str] = "medium"

@app.post("/reset")
def reset_post(body: Optional[ResetRequest] = None):
    task = body.task_name if body else "medium"
    if task not in tasks:
        task = "medium"
    env = StudyEnvironment(task)
    return env.reset()

@app.get("/reset")
def reset_get():
    env = StudyEnvironment("medium")
    return env.reset()




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
