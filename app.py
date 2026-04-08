from env.environment import EmergencyEnv

env = EmergencyEnv()

obs = env.reset()
print("Observation:", obs)

action = [
    {"firetruck": 2, "ambulance": 1, "police": 1},
    {"ambulance": 2, "police": 1}
]
obs, reward, done, _ = env.step(action)

print("Reward:", reward)