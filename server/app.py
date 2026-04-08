from fastapi import FastAPI
import uvicorn
from env.environment import EmergencyEnv

app = FastAPI()

env = EmergencyEnv()


@app.get("/")
def root():
    return {"message": "Emergency Response Environment API is running"}


@app.post("/reset")
def reset():
    state = env.reset()
    return {"state": state}


@app.post("/step")
def step(action: dict):
    state, reward, done, _ = env.step(action["action"])
    return {
        "state": state,
        "reward": reward,
        "done": done
    }


# ✅ REQUIRED main function
def main():
    uvicorn.run(app, host="0.0.0.0", port=7860)


# ✅ REQUIRED entry point
if __name__ == "__main__":
    main()
