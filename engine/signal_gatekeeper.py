import config

def verify_signal_gatekeeper(
    consensus_price,
    price_valid,
    validation_msg,
    news_risk_active,
    confluence_score,
    rr_ratio,
    is_daily_report=False
):
    """
    Signal Gatekeeper (Production Gatekeeper Layer):
    Strict pre-dispatch safety gatekeeper.
    Report/Signal is BLOCKED if:
    - Real-time spot price fails validation or timestamp > 60s
    - Price mismatch across sources > $1.50
    - High-impact economic news lock is active
    - Confluence score < threshold (for signals)
    - R:R < 1.5 (for signals)
    """
    rejection_reasons = []

    if not price_valid or not consensus_price or consensus_price <= 1000:
        rejection_reasons.append(f"Price Validation Failed: {validation_msg}")

    if news_risk_active and not is_daily_report:
        rejection_reasons.append("High-Impact Economic News Lock Active (+/- 15m window)")

    if not is_daily_report:
        if confluence_score < config.MIN_CONFLUENCE_FOR_SIGNAL:
            rejection_reasons.append(f"Confluence Score ({confluence_score:.1f}) < Threshold ({config.MIN_CONFLUENCE_FOR_SIGNAL:.1f})")

        if rr_ratio < 1.5:
            rejection_reasons.append(f"Risk:Reward Ratio (1:{rr_ratio:.2f}) < 1:1.5 Minimum")

    passed = len(rejection_reasons) == 0
    status_str = "APPROVED FOR DISPATCH" if passed else f"BLOCKED BY GATEKEEPER ({'; '.join(rejection_reasons)})"

    return {
        'passed': passed,
        'status_str': status_str,
        'rejection_reasons': rejection_reasons
    }

if __name__ == '__main__':
    res = verify_signal_gatekeeper(4090.12, True, "Consensus verified", False, 88.0, 2.2)
    print("Gatekeeper test:", res)
