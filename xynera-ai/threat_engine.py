def get_threat_level(score):

    if score <= 5:
        return "LOW"

    elif score <= 15:
        return "MEDIUM"

    elif score <= 30:
        return "HIGH"

    else:
        return "CRITICAL"
