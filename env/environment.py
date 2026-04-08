from tasks.graders import grade_allocation
import json
import random

class EmergencyEnv:
    def __init__(self):
        with open("data/incidents.json") as f:
            self.incidents = json.load(f)
        self.current = None

    def reset(self):
        base = random.sample(self.incidents, 2)
        # simulate cascade
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
            total_score += grade_allocation(act, required)
        return total_score / len(self.current)