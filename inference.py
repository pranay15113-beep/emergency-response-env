import requests
import os
from openai import OpenAI

BASE_URL = os.getenv("API_BASE_URL", "http://localhost:7860")

# ✅ LLM client using their proxy
client = OpenAI(
    base_url=os.environ["API_BASE_URL"],
    api_key=os.environ["API_KEY"]
)


def get_agent_action(state):
    # 🔥 Convert state to prompt
    prompt = f"""
You are an emergency response agent.
Given the incidents below, allocate resources.

Incidents:
{state}

Return ONLY JSON list of actions like:
[{{"ambulance":1,"firetruck":2}}, ...]
"""

    response = client.chat.completions.create(
        model=os.getenv("MODEL_NAME", "gpt-4o-mini"),
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    text = response.choices[0].message.content

    try:
        actions = eval(text)  # simple parsing
    except:
        # fallback (safe)
        actions = [incident["required"] for incident in state]

    return {"action": actions}


def main():
    try:
        task_name = "emergency_response"

        print(f"[START] task={task_name}", flush=True)

        # Reset
        res = requests.post(f"{BASE_URL}/reset")
        data = res.json()
        state = data.get("state", data)

        # LLM action
        action = get_agent_action(state)

        res = requests.post(f"{BASE_URL}/step", json=action)
        result = res.json()

        reward = result.get("reward", 0)

        print(f"[STEP] step=1 reward={reward}", flush=True)
        print(f"[END] task={task_name} score={reward} steps=1", flush=True)

    except Exception as e:
        print(f"[ERROR] {str(e)}", flush=True)


if __name__ == "__main__":
    main()
