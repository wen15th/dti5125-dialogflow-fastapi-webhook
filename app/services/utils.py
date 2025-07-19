def to_severity_score(predicted_label: int) -> int:
    return int(predicted_label) + 1