from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict, Optional
from env.environment import EmergencyEnv

app = FastAPI()
env = EmergencyEnv()


class ActionRequest(BaseModel):
    action: List[Dict]


class ResetRequest(BaseModel):
    task: Optional[str] = None


@app.get("/")
def root():
    return {"message": "Emergency Response Environment API is running"}


@app.post("/reset")
def reset(request: ResetRequest = ResetRequest()):
    state = env.reset(request.task)
    return {"state": state}


@app.post("/step")
def step(request: ActionRequest):
    next_state, reward, done, _ = env.step(request.action)
    return {
        "state": next_state,
        "reward": reward,
        "done": done
    }


def main():
    import uvicorn
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860)


if __name__ == "__main__":
    main()
