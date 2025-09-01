def calculate_success_rate(planned_study, real_study, planned_break, real_break, distraction):
    study_ratio = min(real_study/planned_study, 1.0)
    break_ratio = min(real_break/planned_break, 1.0)
    focus = 1 - (distraction / max(1, real_study))

    success_rate = (0.5 * study_ratio + 0.3 * break_ratio + 0.2 * focus) * 100
    return round(success_rate, 2)

# STRESS RATE dipengaruhi oleh banyaknya distraksi, urgensi, dan kurangnya istirahat
def calculate_stress_rate(distraction,urgent_ratio, planned_break, real_break):
    break_deficit = max(0, (planned_break - real_break) / planned_break)
    base_stress = 0.4 * distraction + 0.4 * urgent_ratio + 0.2 * break_deficit
    return min(max(base_stress * 100, 0), 100)

# urgent_ratio = urgent_subjects_studied / total_subjects_studied

def calculate_focus_rate(study_time, distraction_time):
    focus_rate = (study_time / (study_time + distraction_time)) * 100
    return focus_rate


def varianceOfSubject(urgent, middle, leisure):
    values = [urgent, middle, leisure]
    total = sum(values)
    if total == 0:
        return 0.0

    proportions = [v / total for v in values]
    mean = sum(proportions) / len(proportions)
    variance = sum((p - mean) ** 2 for p in proportions) / len(proportions)
    return variance

def progress_score(success_rate, urgent, middle, leisure):
    subject_balance = 1 - varianceOfSubject(urgent, middle, leisure)
    progress = 0.7 * success_rate + 0.3 * subject_balance
    return progress