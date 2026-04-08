from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict
from env.environment import EmergencyEnv

app = FastAPI()

env = EmergencyEnv()

# Request model for step
class ActionRequest(BaseModel):
    action: List[Dict]

@app.get("/")
def root():
    return {"message": "Emergency Response Environment API is running"}

@app.post("/reset")
def reset():
    state = env.reset()
    return {
        "state": state
    }

@app.post("/step")
def step(request: ActionRequest):
    action = request.action
    next_state, reward, done, _ = env.step(action)

    return {
        "state": next_state,
        "reward": reward,
        "done": done
    }