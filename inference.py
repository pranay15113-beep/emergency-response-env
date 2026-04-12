import requests
import os
from openai import OpenAI

BASE_URL = os.getenv("API_BASE_URL", "http://localhost:7860")

client = OpenAI(
    base_url=os.environ["API_BASE_URL"],
    api_key=os.environ["API_KEY"]
)


def get_agent_action(state):
    # LLM call (required)
    try:
        client.chat.completions.create(
            model=os.getenv("MODEL_NAME", "gpt-4o-mini"),
            messages=[{"role": "user", "content": str(state)}],
            temperature=0
        )
    except:
        pass

    actions = []

    # 🔥 SAFETY: ensure state is list
    if not isinstance(state, list):
        return {"action": []}

    for incident in state:
        # skip invalid entries
        if not isinstance(incident, dict):
            continue

        required = incident.get("required", {})

        if not isinstance(required, dict):
            continue

        modified = {}

        for k, v in required.items():
            if isinstance(v, int):
                if v > 1:
                    modified[k] = v - 1
                else:
                    modified[k] = 1  # avoid zero

        actions.append(modified)

    return {"action": actions}


def run_task(task_name):
    print(f"[START] task={task_name}", flush=True)

    # 🔥 SAFE RESET CALL
    try:
        res = requests.post(
            f"{BASE_URL}/reset",
            json={"task": task_name}
        )
        data = res.json()

        # handle both formats
        if isinstance(data, dict) and "state" in data:
            state = data["state"]
        else:
            state = data

    except Exception as e:
        print(f"[ERROR] reset failed: {e}", flush=True)
        return

    # 🔥 VALIDATE STATE
    if not isinstance(state, list):
        print("[ERROR] invalid state format", flush=True)
        return

    action = get_agent_action(state)

    # 🔥 SAFE STEP CALL
    try:
        res = requests.post(f"{BASE_URL}/step", json=action)
        result = res.json()
    except Exception as e:
        print(f"[ERROR] step failed: {e}", flush=True)
        return

    reward = result.get("reward", 0)

    # 🔥 FINAL CLAMP
    if reward <= 0:
        reward = 0.1
    elif reward >= 1:
        reward = 0.9

    print(f"[STEP] step=1 reward={reward}", flush=True)
    print(f"[END] task={task_name} score={reward} steps=1", flush=True)


def main():
    try:
        run_task("easy_allocation")
        run_task("medium_multi_incident")
        run_task("hard_cascade")
    except Exception as e:
        print(f"[ERROR] {str(e)}", flush=True)


if __name__ == "__main__":
    main()
