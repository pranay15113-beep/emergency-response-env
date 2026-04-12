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

    # 🔥 STRICT FIX (no 0 or 1 ever)
    if raw_score <= 0:
        return 0.05
    elif raw_score >= 1:
        return 0.95
    else:
        return raw_score
