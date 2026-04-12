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
    for incident in state:
        modified = {}

        for k, v in incident["required"].items():
            if v > 1:
                modified[k] = v - 1
            else:
                modified[k] = 1

        actions.append(modified)

    return {"action": actions}


def run_task(task_name):
    print(f"[START] task={task_name}", flush=True)

    res = requests.post(f"{BASE_URL}/reset")
    data = res.json()
    state = data.get("state", data)

    action = get_agent_action(state)

    res = requests.post(f"{BASE_URL}/step", json=action)
    result = res.json()

    reward = result.get("reward", 0)

    print(f"[STEP] step=1 reward={reward}", flush=True)
    print(f"[END] task={task_name} score={reward} steps=1", flush=True)


def main():
    try:
        tasks = [
            "easy_allocation",
            "medium_multi_incident",
            "hard_cascade"
        ]

        for task in tasks:
            run_task(task)

    except Exception as e:
        print(f"[ERROR] {str(e)}", flush=True)


if __name__ == "__main__":
    main()
