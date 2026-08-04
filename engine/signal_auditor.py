def execute_pre_flight_self_audit(
    data_fresh,
    price_valid,
    macro_conflict,
    news_risk,
    rr_ratio,
    confluence_score
):
    """
    Self-Audit & Signal Quality AI (Layer 22):
    Runs pre-flight safety checklist before sending signal card to Telegram.
    Checks:
    - Data Fresh?
    - Macro Conflict?
    - News Conflict?
    - Enough Risk:Reward Ratio (>= 1:1.5)?
    - Confluence Score Threshold met?
    """
    checklist = {
        "Data Fresh (<60s)": "YES" if data_fresh and price_valid else "NO",
        "Macro Conflict": "NO" if not macro_conflict else "YES",
        "News Event Conflict": "NO" if not news_risk else "YES",
        "Enough R:R (>= 1.5)": "YES" if rr_ratio >= 1.5 else "NO",
        "Confluence Threshold (>= 85)": "YES" if confluence_score >= 85.0 else "NO"
    }

    all_passed = (
        data_fresh and
        price_valid and
        not macro_conflict and
        not news_risk and
        rr_ratio >= 1.5 and
        confluence_score >= 85.0
    )

    quality = "EXCELLENT (A+ APPROVED)" if all_passed else "WEAK / REJECTED"

    return {
        'approved': all_passed,
        'quality': quality,
        'checklist': checklist
    }

if __name__ == '__main__':
    audit = execute_pre_flight_self_audit(True, True, False, False, 2.5, 91.0)
    print("Self-audit result:", audit)
