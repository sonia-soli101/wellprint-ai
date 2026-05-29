def score_sleep_hours(hours):
    """수면 시간을 0~100점으로 변환합니다."""
    if 7 <= hours <= 8:
        return 100
    elif 6 <= hours < 7:
        return 75
    elif 8 < hours <= 9:
        return 80
    elif 5 <= hours < 6:
        return 50
    else:
        return 25


def score_steps(steps):
    """걸음 수를 0~100점으로 변환합니다."""
    if steps >= 8000:
        return 100
    elif steps >= 6000:
        return 80
    elif steps >= 4000:
        return 60
    elif steps >= 2000:
        return 40
    else:
        return 20


def score_stress(stress_level):
    """스트레스 수준을 0~100점으로 변환합니다. 낮을수록 높은 점수입니다."""
    if stress_level <= 2:
        return 100
    elif stress_level <= 4:
        return 80
    elif stress_level <= 6:
        return 60
    elif stress_level <= 8:
        return 35
    else:
        return 15


def score_gratitude(count):
    """감사 표현 횟수를 0~100점으로 변환합니다."""
    if count >= 3:
        return 100
    elif count == 2:
        return 80
    elif count == 1:
        return 60
    else:
        return 30


def score_sugary_drinks(count):
    """단 음료 섭취 횟수를 0~100점으로 변환합니다. 적을수록 높은 점수입니다."""
    if count <= 0:
        return 100
    elif count == 1:
        return 60
    else:
        return 25


def score_ultra_processed_food(count):
    """초가공식품 섭취 횟수를 0~100점으로 변환합니다. 적을수록 높은 점수입니다."""
    if count <= 0:
        return 100
    elif count == 1:
        return 65
    else:
        return 30


def score_water_intake(liters):
    """물 섭취량을 0~100점으로 변환합니다."""
    if 1.5 <= liters <= 2.5:
        return 100
    elif liters >= 1.0:
        return 75
    elif liters >= 0.5:
        return 50
    else:
        return 25


def score_bloating(level):
    """복부팽만/가스 수준을 0~100점으로 변환합니다. 낮을수록 높은 점수입니다."""
    if level <= 2:
        return 100
    elif level <= 4:
        return 80
    elif level <= 6:
        return 55
    elif level <= 8:
        return 35
    else:
        return 15


def calculate_sub_scores(row):
    """
    하루 생활습관 입력값을 바탕으로 하위 점수들을 계산합니다.
    각 하위 점수는 0~100점 기준입니다.
    """

    sleep_hours = row.get("sleep_hours", 7)
    steps = row.get("steps", 5000)
    stress_level = row.get("stress_level_1_10", 5)
    gratitude_count = row.get("gratitude_said_count", 0)

    sugary_drinks = row.get("sugary_drink_count", 0)
    ultra_processed_food = row.get("ultra_processed_food_count", 0)
    water_liters = row.get("water_intake_l", 1.0)
    bloating_level = row.get("bloating_level_1_10", 5)

    sleep_score = score_sleep_hours(sleep_hours)
    activity_score = score_steps(steps)
    stress_score = score_stress(stress_level)
    gratitude_score = score_gratitude(gratitude_count)

    sugary_drink_score = score_sugary_drinks(sugary_drinks)
    ultra_processed_score = score_ultra_processed_food(ultra_processed_food)
    hydration_score = score_water_intake(water_liters)
    gut_score = score_bloating(bloating_level)

    food_score = (
        sugary_drink_score * 0.45 +
        ultra_processed_score * 0.55
    )

    social_score = gratitude_score

    return {
        "sleep_score": round(sleep_score),
        "activity_score": round(activity_score),
        "stress_score": round(stress_score),
        "food_score": round(food_score),
        "hydration_score": round(hydration_score),
        "gut_score": round(gut_score),
        "social_score": round(social_score),
    }


def calculate_wellness_score(row):
    """
    하위 점수를 가중합하여 Wellprint Total Score를 계산합니다.

    이 점수는 의료 진단이 아니라,
    수면, 활동, 스트레스, 식사, 수분, 장 컨디션, 사회적 환경을 종합한
    생활습관 기반 웰니스 점수입니다.
    """

    sub_scores = calculate_sub_scores(row)

    total_score = (
        sub_scores["sleep_score"] * 0.20 +
        sub_scores["activity_score"] * 0.20 +
        sub_scores["stress_score"] * 0.20 +
        sub_scores["food_score"] * 0.15 +
        sub_scores["hydration_score"] * 0.10 +
        sub_scores["gut_score"] * 0.10 +
        sub_scores["social_score"] * 0.05
    )

    return round(total_score)


def get_wellness_level(score):
    """Wellprint Total Score를 등급으로 변환합니다."""
    if score >= 80:
        return "Strong"
    elif score >= 60:
        return "Balanced"
    elif score >= 40:
        return "Needs Attention"
    else:
        return "High Burden"


def get_wellness_message(score):
    """점수에 따른 한글 안내 문구를 반환합니다."""
    if score >= 80:
        return "오늘의 웰니스 패턴이 전반적으로 안정적입니다."
    elif score >= 60:
        return "괜찮은 하루지만 일부 회복 방해 요인이 있습니다."
    elif score >= 40:
        return "수면, 식사, 스트레스, 장 컨디션 중 개선이 필요한 신호가 있습니다."
    else:
        return "오늘은 회복을 우선해야 하는 생활패턴입니다."