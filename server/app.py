from fastapi import FastAPI
from pydantic import BaseModel
import sys, os, random

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from env import StudyEnvironment
from tasks import tasks

app = FastAPI()

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
    env = StudyEnvironment("medium")
    return env.reset()

@app.get("/reset/{task_name}")
@app.post("/reset/{task_name}")
def reset_task(task_name: str):
    if task_name not in tasks:
        return {"error": "Task not found"}
    env = StudyEnvironment(task_name)
    return env.reset()

@app.get("/state")
def state():
    env = StudyEnvironment("medium")
    return env.state()

@app.get("/state/{task_name}")
def state_task(task_name: str):
    if task_name not in tasks:
        return {"error": "Task not found"}
    env = StudyEnvironment(task_name)
    return env.state()

@app.get("/step/{action}")
def step(action: str):
    env = StudyEnvironment("medium")
    state, reward, done, score = env.step(action)
    return StepResult(state=state, reward=round(reward,2), done=done, score=round(score,2))

@app.get("/step/{task_name}/{action}")
def step_task(task_name: str, action: str):
    if task_name not in tasks:
        return {"error": "Task not found"}
    env = StudyEnvironment(task_name)
    state, reward, done, score = env.step(action)
    return StepResult(state=state, reward=round(reward,2), done=done, score=round(score,2))

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

def main():
    return app

if __name__ == "__main__":
    main()
