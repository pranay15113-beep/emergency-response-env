def grade_allocation(action, required):
    score = 0
    total = len(required)

    for key in required:
        if key in action:
            if action[key] == required[key]:
                score += 1
            elif action[key] > 0:
                score += 0.5

    if total == 0:
        return 0.5

    raw_score = score / total

    # 🔥 CRITICAL FIX — NEVER return 0 or 1
    if raw_score <= 0:
        return 0.01
    elif raw_score >= 1:
        return 0.99
    else:
        return raw_score
