from fastapi import FastAPI
from pydantic import BaseModel
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from env import StudyEnvironment
from tasks import tasks


app = FastAPI()

env = StudyEnvironment("medium")


class Observation(BaseModel):

    energy:int
    progress:float
    time:int
    focus:int
    actions:list


class StepResult(BaseModel):

    state:dict
    reward:float
    done:bool
    score:float


@app.get("/")

def home():

    return {"message":"AI Study Planner running"}


@app.get("/reset")
@app.post("/reset")

def reset():

    return env.reset()


@app.get("/state")

def state():

    return Observation(**env.state())


@app.get("/step/{action}")

def step(action:str):

    state,reward,done,score=env.step(action)

    return StepResult(

        state=state,
        reward=round(reward,2),
        done=done,
        score=round(score,2)

    )


@app.get("/tasks")

def get_tasks():

    return tasks


@app.get("/grader")

def grader():

    score = env.get_score()

    if score <= 0:
        score = 0.01

    if score >= 1:
        score = 0.99

    return {

        "grader_score":round(score,2),
        "passed": score > 0

    }


def main():

    return app


if __name__=="__main__":

    main()
