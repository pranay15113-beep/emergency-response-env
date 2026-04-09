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
        # Reset
        res = requests.post(f"{BASE_URL}/reset")
        data = res.json()

        # 🔥 SAFE handling
        state = data.get("state", data)

        # Action
        action = get_agent_action(state)

        res = requests.post(f"{BASE_URL}/step", json=action)
        result = res.json()

        print("Final Reward:", result.get("reward", "N/A"))

    except Exception as e:
        print("Error:", str(e))


if __name__ == "__main__":
    main()
