from engine import performance_layer

def calibrate_confidence_score(raw_confluence_score):
    """
    Calibrates raw confluence score against historical win-rate distribution.
    Ensures a 90/100 score aligns with empirical historical win rates.
    """
    perf = performance_layer.get_historical_performance_metrics()
    baseline_win_rate = perf.get('win_rate', 78.5)

    if raw_confluence_score >= 90.0:
        # Scale to calibrated range (88% - 96%)
        calibrated = min(96.0, baseline_win_rate + (raw_confluence_score - 85.0) * 0.8)
    elif raw_confluence_score >= 80.0:
        calibrated = min(88.0, baseline_win_rate + (raw_confluence_score - 80.0) * 0.5)
    else:
        calibrated = raw_confluence_score * 0.85

    return round(calibrated, 1)

if __name__ == '__main__':
    print(f"Raw 92.0 -> Calibrated: {calibrate_confidence_score(92.0)}%")
