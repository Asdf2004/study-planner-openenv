from fastapi import FastAPI
from pydantic import BaseModel
import random

from env import StudyEnvironment

# Reproducible results
random.seed(42)

main = FastAPI()

env = StudyEnvironment("medium")


# Typed models (OpenEnv requirement)

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


@main.get("/")
def home():

    return {"message":"AI Study Planner Environment running"}


@app.post("/reset")
@app.get("/reset")

def reset():

    state = env.reset()

    return state


@app.post("/state")
@app.get("/state")

def state():

    return Observation(**env.state())


@app.post("/step/{action}")
@app.get("/step/{action}")

def step(action:str):

    state,reward,done,score = env.step(action)

    return StepResult(

        state=state,

        reward=round(reward,2),

        done=done,

        score=round(score,2)

    )


@app.get("/baseline")

def baseline():

    env.reset()

    done=False

    total_reward=0

    while not done:

        if env.energy < 30:

            action="rest"

        elif env.focus < 25:

            action="rest"

        elif random.random() < 0.1:

            action="scroll"

        else:

            action="study"

        state,reward,done,score = env.step(action)

        total_reward += reward

    return {

        "baseline_score":round(score,2),

        "total_reward":round(total_reward,2),

        "steps":env.time

    }


@app.get("/grader")

def grader():

    score = env.get_score()

    return {

        "grader_score":round(score,2),

        "passed": score >= 1.0

    }


@app.get("/tasks")

def tasks():

    return {

        "easy":{"target":30},

        "medium":{"target":60},

        "hard":{"target":100}

    }
