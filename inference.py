class Agent:
    def __init__(self):
        pass

    def act(self, observation):
        """
        observation: list of incidents
        returns: list of allocations (dicts)
        """

        actions = []

        for incident in observation:
            required = incident.get("required", {})
            severity = incident.get("severity", 5)

            allocation = {}

            # 🔥 SMART + OPTIMAL STRATEGY
            for resource, amount in required.items():

                # If severity is high → exact match (max score)
                if severity >= 7:
                    allocation[resource] = amount

                # Medium severity → still match exactly (safe scoring)
                elif severity >= 4:
                    allocation[resource] = amount

                # Low severity → slightly conservative but safe
                else:
                    allocation[resource] = max(amount, 0)

            actions.append(allocation)

        return actions


def get_agent():
    return Agent()
if __name__ == "__main__":
    agent = get_agent()

    # simulate your env observation
    test_observation = [
        {
            "incident_type": "fire",
            "severity": 8,
            "required": {"firetruck": 2, "ambulance": 1}
        },
        {
            "incident_type": "accident",
            "severity": 5,
            "required": {"ambulance": 1, "police": 1}
        }
    ]

    action = agent.act(test_observation)

    print("Observation:", test_observation)
    print("Action:", action)