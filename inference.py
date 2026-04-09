import requests
import os

BASE_URL = os.getenv("API_BASE_URL", "http://localhost:7860")


def get_agent_action(state):
    actions = []
    for incident in state:
        actions.append(incident["required"])
    return {"action": actions}


def main():
    try:
        task_name = "emergency_response"

        # 🔥 START BLOCK
        print(f"[START] task={task_name}", flush=True)

        # Reset
        res = requests.post(f"{BASE_URL}/reset")
        data = res.json()

        state = data.get("state", data)

        # Take action
        action = get_agent_action(state)

        res = requests.post(f"{BASE_URL}/step", json=action)
        result = res.json()

        reward = result.get("reward", 0)

        # 🔥 STEP BLOCK
        print(f"[STEP] step=1 reward={reward}", flush=True)

        # 🔥 END BLOCK
        print(f"[END] task={task_name} score={reward} steps=1", flush=True)

    except Exception as e:
        print(f"[ERROR] {str(e)}", flush=True)


if __name__ == "__main__":
    main()
