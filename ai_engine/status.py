def determine_status(score):

    if score >= 75:
        return "hot"

    elif score >= 45:
        return "warm"

    return "cold"