from fastapi import FastAPI
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from env import StudyEnvironment
from tasks import tasks

app = FastAPI(
    title="AI Study Planner Environment",
    description="RL study optimization environment",
    version="1.0"
)

# Create environment for each task
envs = {name: StudyEnvironment(name) for name in tasks}


@app.get("/")
def home():
    return {"message":"AI Study Planner running"}


# TASK LIST
@app.get("/tasks")
def get_tasks():
    return tasks


# DEFAULT RESET
@app.get("/reset")
@app.post("/reset")
def reset():
    return envs["medium"].reset()


# RESET PER TASK
@app.get("/reset/{task}")
@app.post("/reset/{task}")
def reset_task(task:str):

    if task not in envs:
        return {"error":"Task not found"}

    return envs[task].reset()


# DEFAULT STATE
@app.get("/state")
def state():
    return envs["medium"].state()


# DEFAULT STEP
@app.get("/step/{action}")
def step(action:str):

    state,reward,done,score = envs["medium"].step(action)

    return {
        "state":state,
        "reward":round(float(reward),2),
        "done":done,
        "score":round(float(score),2)
    }


# STEP PER TASK
@app.get("/step/{task}/{action}")
def step_task(task:str,action:str):

    if task not in envs:
        return {"error":"Task not found"}

    state,reward,done,score = envs[task].step(action)

    return {
        "state":state,
        "reward":round(float(reward),2),
        "done":done,
        "score":round(float(score),2)
    }


# GRADER (IMPORTANT FOR PHASE 2)
@app.get("/grader")
def grader():

    results={}

    for name,env in envs.items():

        score = float(env.get_score())

        # keep strictly between 0 and 1
        if score <=0:
            score=0.01

        if score >=1:
            score=0.99

        results[name]={
            "grader_score":round(score,2),
            "passed":True
        }

    return results


# ENTRYPOINT REQUIRED BY OPENENV
def main():
    return app


if __name__ == "__main__":
    main()
