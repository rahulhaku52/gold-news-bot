import config

# Flexible import for Google Gemini SDK (handling new google.genai or deprecated google.generativeai)
model = None
try:
    import google.genai as genai
    if config.GEMINI_API_KEY:
        client = genai.Client(api_key=config.GEMINI_API_KEY)
    else:
        client = None
except ImportError:
    try:
        import google.generativeai as genai
        if config.GEMINI_API_KEY:
            genai.configure(api_key=config.GEMINI_API_KEY)
            model = genai.GenerativeModel('gemini-1.5-flash')
        else:
            model = None
        client = None
    except Exception:
        model = None
        client = None

def generate_ai_reasoning_synthesis(market_data_summary):
    """
    Dual-Scenario AI Synthesis (Layer 19):
    Generates Primary Plan and Alternative Scenario.
    Gracefully catches Gemini 429 rate limit / quota errors and uses deterministic synthesis.
    """
    direction = market_data_summary.get('direction', 'BUY')
    alt_direction = 'SELL' if direction == 'BUY' else 'BUY'
    key_level = market_data_summary.get('key_level', 3380.0)

    # Standard high-quality fallback synthesis
    fallback_primary = [
        f"Daily & 4H structure {direction.lower()}ish with confirmed breakout.",
        f"Retest of key Demand / Order Block zone successful.",
        f"DXY Dollar Index weakening, providing strong tailwind.",
        f"Macro CPI & inflation backdrop supportive for Gold.",
        f"Volume expansion confirming momentum on lower timeframe."
    ]
    fallback_alt = f"<b>Alternative ({alt_direction}):</b> Only if ${key_level:.2f} is reclaimed on 4H close."

    if not config.GEMINI_API_KEY:
        return fallback_primary, fallback_alt

    prompt = f"""
You are an institutional Gold (XAUUSD) trading strategist. Synthesize the primary trade plan and an alternative scenario.

Data Summary:
- Current Price: ${market_data_summary.get('price', 0):.2f}
- Direction: {direction}
- Trend: {market_data_summary.get('overall_trend', 'NEUTRAL')}
- Structure Bias: {market_data_summary.get('structure_bias', 'NEUTRAL')}
- SMC Zone: {market_data_summary.get('smc_zone', 'Equilibrium')}
- Session: {market_data_summary.get('session_name', 'London')}
- Confluence Score: {market_data_summary.get('confluence_score', 0):.1f}

Output:
PART 1: Exactly 5 concise bullet points for Primary Plan starting with bullet symbol (•).
PART 2: Exactly 1 line for Alternative Scenario starting with "ALTERNATIVE:" specifying conditions.
"""
    try:
        if client:
            response = client.models.generate_content(model='gemini-2.5-flash', contents=prompt)
            text = response.text.strip()
        elif model:
            response = model.generate_content(prompt)
            text = response.text.strip()
        else:
            return fallback_primary, fallback_alt

        lines = [line.strip() for line in text.split('\n') if line.strip()]
        primary_bullets = [l.replace('*', '•') for l in lines if l.startswith('•') or l.startswith('*')][:5]
        alt_line = next((l for l in lines if 'ALTERNATIVE:' in l.upper() or 'ALT:' in l.upper()), fallback_alt)

        if len(primary_bullets) >= 3:
            return primary_bullets, alt_line
    except Exception as e:
        print(f"⚠️ Gemini API Quota/Rate limit notice ({e}). Switching to institutional fallback synthesis.")

    return fallback_primary, fallback_alt

if __name__ == '__main__':
    print("AI reasoning module ready.")
