def calculate_success_rate(study_time, break_time, user_prefs):
    """
    Success if study session matches user's preferred pattern.
    """
    expected_break = user_prefs["preferred_break_time"]
    expected_focus = user_prefs["max_focus_session"]

    # success drops if user breaks earlier or studies far longer than planned
    deviation = abs(break_time - expected_break) + abs(study_time - expected_focus)
    success = max(0, 100 - deviation)
    return success
def calculate_focus_rate(study_time, distractions_time, user_prefs):
    """
    Focus = (time actually spent focusing) / (total intended time)
    """
    intended = min(study_time, user_prefs["max_focus_session"])
    focus_time = study_time - distractions_time
    return max(0, (focus_time / intended) * 100)

def calculate_stress(daily_study, user_prefs):
    """
    Stress grows if user studies way over their daily available time.
    """
    available = user_prefs["daily_available_time"]
    if daily_study <= available:
        return 20  # baseline low stress
    else:
        overload = daily_study - available
        return min(100, 20 + overload)  # cap at 100

# def varianceOfSubject(urgent, middle, leisure):
#     values = [urgent, middle, leisure]
#     total = sum(values)
#     if total == 0:
#         return 0.0
#
#     proportions = [v / total for v in values]
#     mean = sum(proportions) / len(proportions)
#     variance = sum((p - mean) ** 2 for p in proportions) / len(proportions)
#     return variance
#
# def progress_score(success_rate, urgent, middle, leisure):
#     subject_balance = 1 - varianceOfSubject(urgent, middle, leisure)
#     progress = 0.7 * success_rate + 0.3 * subject_balance
#     return progress

def calculate_consistency(days_logged_in, total_days_from_first_login):
    consistency = days_logged_in / total_days_from_first_login
    return  consistency

def calculate_progress_score(
    primary_goal,
    consistency_rate,   # 0–1 (days logged / total days)
    success_rate,       # 0–1 (sessions completed successfully)
    focus_rate,         # 0–1 (study / (study+distraction))
    stress_rate         # 0–1 (1 - stress/maxStress)
):
    # Default weights
    weights = {
        "consistency": 0.25,
        "success": 0.25,
        "focus": 0.25,
        "stress": 0.25
    }

    # Adjust weights depending on primary goal
    if primary_goal == "consistency":
        weights = {"consistency": 0.5, "success": 0.25, "focus": 0.15, "stress": 0.10}
    elif primary_goal == "productivity":
        weights = {"consistency": 0.20, "success": 0.40, "focus": 0.30, "stress": 0.10}
    elif primary_goal == "wellbeing":
        weights = {"consistency": 0.20, "success": 0.10, "focus": 0.30, "stress": 0.40}

    # Final score calculation
    progress_score = (
        consistency_rate * weights["consistency"] +
        success_rate * weights["success"] +
        focus_rate * weights["focus"] +
        stress_rate * weights["stress"]
    )

    return round(progress_score * 100, 2)  # percentage
