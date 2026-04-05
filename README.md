# AI Study Planner Environment

This project implements an AI Study Planner Environment using FastAPI and OpenEnv specification. The environment simulates student study behavior including energy, focus, time management and productivity.

## Deployment

This environment is deployed using Docker on HuggingFace Spaces.

## Project Structure

study_env/
│── server/
│    └── app.py          # FastAPI server
│── agent.py             # Agent logic
│── Dockerfile
│── env.py               # Environment logic
│── inference.py         # Baseline inference
│── openenv.yaml         # OpenEnv configuration
│── pyproject.toml
│── README.md
│── requirements.txt
│── tasks.py             # Task definitions
│── uv.lock


## API Endpoints

### Reset Environment
POST /reset  
GET /reset  

Resets the study environment.

### Get State
GET /state  
POST /state  

Returns current environment state.

### Take Action
GET /step/{action}  
POST /step/{action}

Actions:
- study
- rest
- scroll

### Baseline Agent
GET /baseline

Runs baseline agent simulation.

### Grader
GET /grader

Returns environment score.

### Tasks
GET /tasks

Returns difficulty targets.

## Author

Sanjeev Kumar Bind

## Tech Stack

- Python
- FastAPI
- OpenEnv
- Docker
- HuggingFace Spaces
