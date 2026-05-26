def calculate_wellness_score(row):
    """
    Calculate a simple wellness score from lifestyle burden factors.
    This score is not a medical diagnosis.
    """

    score = 50

    # Sleep score
    sleep_hours = row.get("sleep_hours", 0)
    if 7 <= sleep_hours <= 9:
        score += 15
    elif 6 <= sleep_hours < 7 or 9 < sleep_hours <= 10:
        score += 8
    else:
        score += 2

    # Sleep quality
    sleep_quality = row.get("sleep_quality_1_10", 0)
    score += sleep_quality * 1.5

    # Steps
    steps = row.get("steps", 0)
    if steps >= 10000:
        score += 12
    elif steps >= 7000:
        score += 8
    elif steps >= 4000:
        score += 4
    else:
        score += 1

    # Active minutes
    active_minutes = row.get("active_minutes", 0)
    if active_minutes >= 60:
        score += 8
    elif active_minutes >= 30:
        score += 5
    elif active_minutes >= 10:
        score += 2

    # Stress penalty
    stress_level = row.get("stress_level_1_10", 0)
    score -= stress_level * 2

    # Ultra-processed food penalty
    ultra_processed_count = row.get("ultra_processed_food_count", 0)
    score -= ultra_processed_count * 3

    # Hydration
    water_cups = row.get("water_cups", 0)
    if water_cups >= 8:
        score += 8
    elif water_cups >= 5:
        score += 5
    elif water_cups >= 3:
        score += 2

    # Gratitude practice: small supportive factor
    gratitude_said_count = row.get("gratitude_said_count", 0)
    specific_gratitude_events_count = row.get("specific_gratitude_events_count", 0)

    if gratitude_said_count >= 3:
        score += 3
    elif gratitude_said_count >= 1:
        score += 1

    if specific_gratitude_events_count >= 3:
        score += 4
    elif specific_gratitude_events_count >= 1:
        score += 2

    # Keep score between 0 and 100
    score = max(0, min(100, score))

    return round(score, 1)


def get_wellness_level(score):
    """
    Convert wellness score into a simple lifestyle burden level.
    """

    if score >= 80:
        return "Strong"
    elif score >= 60:
        return "Balanced"
    elif score >= 40:
        return "Needs Attention"
    else:
        return "High Burden"