def grade_allocation(action, required):
    score = 0
    total = len(required)

    for key in required:
        if key in action:
            diff = abs(required[key] - action[key])
            score += max(0, 1 - (diff / max(required[key], 1)))

    return score / total