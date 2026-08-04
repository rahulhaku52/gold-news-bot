def compute_confluence_score(
    structure_res,
    technical_res,
    smc_res,
    pa_res,
    macro_res,
    news_res,
    corr_res,
    weights
):
    """
    Calculates weighted Confluence Score (0 - 100) based on current Market Regime weights.
    Returns breakdown dictionary and final weighted score.
    """
    struct_score = structure_res.get('structure_score', 50.0)
    tech_score = technical_res.get('technical_score', 50.0)
    smc_score = smc_res.get('smc_score', 50.0)
    pa_score = pa_res.get('pa_score', 50.0)
    macro_score = macro_res.get('macro_score', 50.0)
    news_score = news_res.get('news_score', 50.0)
    corr_score = corr_res.get('correlation_score', 50.0)

    # Combined technical momentum
    tech_momentum_combined = (tech_score * 0.6) + (pa_score * 0.4)
    # Combined market structure
    structure_combined = (struct_score * 0.6) + (smc_score * 0.4)

    w_struct = weights.get('market_structure', 25) / 100.0
    w_macro = weights.get('macro', 20) / 100.0
    w_tech = weights.get('momentum_technical', 15) / 100.0
    w_pa = weights.get('price_action', 15) / 100.0
    w_corr = weights.get('correlation', 10) / 100.0
    w_news = weights.get('news', 10) / 100.0
    w_risk = weights.get('risk_volatility', 5) / 100.0

    final_score = (
        (structure_combined * w_struct) +
        (macro_score * w_macro) +
        (tech_score * w_tech) +
        (pa_score * w_pa) +
        (corr_score * w_corr) +
        (news_score * w_news) +
        (85.0 * w_risk) # Default good risk environment score
    )

    final_score = round(max(0.0, min(100.0, final_score)), 1)

    # Determine Direction & Setup Grade
    if final_score >= 85.0:
        grade = "A+"
        direction = "BUY" if structure_res.get('structure_bias') == "BULLISH" else "SELL"
    elif final_score >= 75.0:
        grade = "A"
        direction = "BUY" if structure_res.get('structure_bias') == "BULLISH" else "SELL"
    else:
        grade = "NEUTRAL"
        direction = "NONE"

    details = {
        'structure': round(structure_combined, 1),
        'momentum': round(tech_score, 1),
        'macro': round(macro_score, 1),
        'news': round(news_score, 1),
        'volume': round(tech_momentum_combined, 1),
        'trend': round(struct_score, 1)
    }

    return {
        'final_score': final_score,
        'grade': grade,
        'direction': direction,
        'details': details
    }

if __name__ == '__main__':
    print("Confluence engine module ready.")
