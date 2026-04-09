import requests
import os

BASE_URL = os.getenv("API_BASE_URL", "http://localhost:7860")

def get_agent_action(state):
    actions = []
    for incident in state:
        # simple smart allocation
        actions.append(incident["required"])
    return {"action": actions}


def main():
    # Step 1: Reset env
    res = requests.post(f"{BASE_URL}/reset")
    state = res.json()["state"]

    # Step 2: Take action
    action = get_agent_action(state)

    res = requests.post(f"{BASE_URL}/step", json=action)
    result = res.json()

    print("Final Reward:", result["reward"])


if __name__ == "__main__":
    main()
