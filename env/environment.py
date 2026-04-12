from tasks.graders import grade_allocation
import json
import random
import os


class EmergencyEnv:
    def __init__(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file_path = os.path.join(base_dir, "data", "incidents.json")

        with open(file_path) as f:
            self.incidents = json.load(f)

        self.current = None

  def reset(self, task=None):
        base = random.sample(self.incidents, 2)

        # cascade logic
        if base[0]["incident_type"] == "fire":
            base.append({
                "incident_type": "accident",
                "location": base[0]["location"],
                "severity": 6,
                "required": {"ambulance": 1, "police": 1}
            })

        self.current = base
        return self.current

    def state(self):
        return self.current

    def step(self, action):
        reward = self.evaluate(action)
        done = True
        return self.current, reward, done, {}

    def evaluate(self, action):
        total_score = 0

        for i, incident in enumerate(self.current):
            required = incident["required"]
            act = action[i] if i < len(action) else {}

            score = grade_allocation(act, required)

            # 🔥 safety clamp
            score = max(0.05, min(0.95, score))

            total_score += score

        final_score = total_score / len(self.current)

        # 🔥 final clamp
        final_score = max(0.05, min(0.95, final_score))

        return final_score
