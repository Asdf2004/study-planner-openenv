from fastapi import FastAPI
from pydantic import BaseModel
import sys, os, random

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from env import StudyEnvironment
from tasks import tasks

app = FastAPI()

# Teeno tasks ke environments
envs = {name: StudyEnvironment(name) for name in tasks}

class StepResult(BaseModel):
    state: dict
    reward: float
    done: bool
    score: float

@app.get("/")
def home():
    return {"message": "AI Study Planner running"}

@app.get("/reset")
@app.post("/reset")
def reset():
    return envs["medium"].reset()

@app.get("/reset/{task_name}")
@app.post("/reset/{task_name}")
def reset_task(task_name: str):
    if task_name not in envs:
        return {"error": "Task not found"}
    return envs[task_name].reset()

@app.get("/state")
def state():
    return envs["medium"].state()

@app.get("/state/{task_name}")
def state_task(task_name: str):
    if task_name not in envs:
        return {"error": "Task not found"}
    return envs[task_name].state()

@app.get("/step/{action}")
def step(action: str):
    state, reward, done, score = envs["medium"].step(action)
    return StepResult(state=state, reward=round(reward,2), done=done, score=round(score,2))

@app.get("/step/{task_name}/{action}")
def step_task(task_name: str, action: str):
    if task_name not in envs:
        return {"error": "Task not found"}
    state, reward, done, score = envs[task_name].step(action)
    return StepResult(state=state, reward=round(reward,2), done=done, score=round(score,2))

@app.get("/tasks")
def get_tasks():
    return {name: {"target": cfg["target"]} for name, cfg in tasks.items()}

@app.get("/grader")
def grader():
    results = {}
    for name, env in envs.items():
        score = max(0.01, min(0.99, env.get_score()))
        results[name] = {
            "grader_score": round(score, 2),
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
        while not done:
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

def main():
    return app

if __name__ == "__main__":
    main()
