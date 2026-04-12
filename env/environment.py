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
        if task == "easy_allocation":
            base = [random.choice(self.incidents)]

        elif task == "medium_multi_incident":
            base = random.sample(self.incidents, 2)

        elif task == "hard_cascade":
            base = random.sample(self.incidents, 2)
            if base[0]["incident_type"] == "fire":
                base.append({
                    "incident_type": "accident",
                    "location": base[0]["location"],
                    "severity": 6,
                    "required": {"ambulance": 1, "police": 1}
                })
        else:
            base = random.sample(self.incidents, 2)

        self.current = base
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

            # clamp (no 0 / no 1)
            score = max(0.05, min(0.95, score))

            total_score += score

        final_score = total_score / len(self.current)
        final_score = max(0.05, min(0.95, final_score))

        return final_score
