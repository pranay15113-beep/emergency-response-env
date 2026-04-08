from env.environment import EmergencyEnv

env = EmergencyEnv()

obs = env.reset()
print("Initial Observation:", obs)

actions = []

for incident in obs:
    actions.append(incident["required"])  # naive perfect guess

obs, reward, done, _ = env.step(actions)

print("Final Reward:", reward)