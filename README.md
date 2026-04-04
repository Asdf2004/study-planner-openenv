# AI Study Planner Environment

## Project Overview

This project implements a Reinforcement Learning environment that simulates a student's study planning behaviour. The agent must manage energy, focus, and time efficiently to maximize study progress.

The goal is to complete study targets while maintaining good energy levels and making optimal decisions.

## Environment Design

The environment follows a standard RL structure:

- reset() → initializes the environment
- step(action) → performs an action
- state() → returns current state
- get_score() → returns normalized score (0–1)

## Action Space

The agent can take the following actions:

- study → increases progress but reduces energy and focus
- rest → restores energy and focus
- scroll → wastes time and reduces energy

## Observation Space

The environment returns:

- energy → student energy level (0–100)
- progress → study completion progress
- time → steps taken
- focus → concentration level
- actions → available actions

## Reward Design

Reward is designed to encourage productive behaviour:

- Study action → +1 reward
- Rest action → +0.5 reward
- Scroll action → -1 reward
- Invalid action → -2 penalty
- Task completion → +5 bonus
- Energy depletion → penalty
- Random distraction penalty

## Tasks

The environment supports three difficulty levels:

Easy → target progress 30  
Medium → target progress 60  
Hard → target progress 100  

## Episode Termination

Episode ends when:

- Target progress achieved
- Energy becomes zero
- Maximum steps reached

## Scoring System

Final score is normalized:

score = progress / target

Score range:
0.0 → no progress  
1.0 → task completed  

## How to Run

Run the baseline agent:

python agent.py

## Project Structure

study_env/
│
├── env.py
├── agent.py
├── tasks.py
├── openenv.yaml
├── README.md
├── requirements.txt

## Requirements

Python 3.8+

## Future Improvements

Possible improvements:

- Multi subject scheduling
- Fatigue modeling
- Random life events
- Adaptive rewards
- Multi-agent scheduling


## API Endpoints

/reset → reset environment

/state → current state

/baseline → baseline agent score

/grader → grader score



## Author

Sanjeev Kumar Bind