---
title: Study Planner Env
emoji: 📘
colorFrom: blue
colorTo: purple
sdk: docker
python_version: "3.10"
pinned: false
license: mit
---


# AI Study Planner Environment

AI Study Planner is a reinforcement learning environment that simulates real student study behavior including energy, focus, productivity and time management.

The goal of the agent is to maximize study progress while managing limited energy and focus resources.

## Environment Design

The environment models realistic student productivity patterns where:

• Studying increases progress but consumes energy  
• Resting restores energy and focus  
• Scrolling wastes time and reduces focus  

The episode ends when:
• Target progress is achieved
• Energy reaches zero
• Maximum steps reached

## Action Space

The agent can take 3 actions:

study → increase progress, reduce energy  
rest → increase energy and focus  
scroll → waste time, reduce focus  

## Observation Space

Environment state contains:

energy → remaining energy (0–100)  
progress → task completion progress  
focus → attention level (0–100)  
time → steps taken  
actions → available actions  

## Tasks

Three tasks with increasing difficulty:

Easy → Target progress 30  
Medium → Target progress 60  
Hard → Target progress 100  

Each task has a grader producing scores between 0.01 and 0.99.

## Reward Design

Reward is shaped to guide learning:

+ reward for study progress  
+ small reward for rest  
- penalty for scrolling  
- penalty for invalid actions  

## API Endpoints

/reset → reset environment  
/state → get current state  
/step/{action} → perform action  
/baseline → run baseline agent  
/grader → get task score  
/tasks → list tasks  

## How to Run

Install dependencies:

pip install -r requirements.txt

Run server:

uvicorn server.app:app --host 0.0.0.0 --port 7860

## Baseline Results

Example baseline performance:

Score ≈ 0.85  
Steps ≈ 12–18  
Reward ≈ positive cumulative reward  

## Deployment

Deployed using Docker on HuggingFace Spaces.

## Tech Stack

Python  
FastAPI  
OpenEnv  
Docker  
HuggingFace Spaces  

## Author

Sanjeev Kumar Bind
