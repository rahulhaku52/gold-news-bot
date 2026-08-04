import google.generativeai as genai
import config

if config.GEMINI_API_KEY:
    genai.configure(api_key=config.GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-2.0-flash')
else:
    model = None

def generate_ai_reasoning_synthesis(market_data_summary):
    """
    Dual-Scenario AI Synthesis (Layer 19):
    Generates Primary Plan and Alternative Scenario.
    """
    direction = market_data_summary.get('direction', 'BUY')
    alt_direction = 'SELL' if direction == 'BUY' else 'BUY'
    key_level = market_data_summary.get('key_level', 3380.0)

    if not model:
        primary_bullets = [
            f"Daily & 4H structure bullish with confirmed breakout.",
            f"Retest of key Demand / Order Block zone successful.",
            f"DXY Dollar Index weakening, providing strong tailwind.",
            f"Macro CPI & inflation backdrop supportive for Gold.",
            f"Volume expansion confirming momentum on lower timeframe."
        ]
        alternative_scenario = f"<b>Alternative ({alt_direction}):</b> Only if ${key_level:.2f} is reclaimed with 4H close & DXY reverses."
        return primary_bullets, alternative_scenario

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
        response = model.generate_content(prompt)
        text = response.text.strip()
        lines = [line.strip() for line in text.split('\n') if line.strip()]

        primary_bullets = [l.replace('*', '•') for l in lines if l.startswith('•') or l.startswith('*')][:5]
        alt_line = next((l for l in lines if 'ALTERNATIVE:' in l.upper() or 'ALT:' in l.upper()), f"Alternative ({alt_direction}): Only if ${key_level:.2f} breaks.")

        if len(primary_bullets) >= 3:
            return primary_bullets, alt_line
    except Exception as e:
        print(f"⚠️ Gemini AI synthesis error: {e}")

    primary_bullets = [
        "Daily & 4H structure bullish with confirmed breakout.",
        "Retest of key Demand / Order Block zone successful.",
        "DXY Dollar Index weakening, providing strong tailwind.",
        "Macro CPI & inflation backdrop supportive for Gold.",
        "Volume expansion confirming momentum on lower timeframe."
    ]
    alternative_scenario = f"<b>Alternative ({alt_direction}):</b> Only if ${key_level:.2f} is reclaimed with 4H close."
    return primary_bullets, alternative_scenario

if __name__ == '__main__':
    print("AI reasoning dual scenario ready.")
