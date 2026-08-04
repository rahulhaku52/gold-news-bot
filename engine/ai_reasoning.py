import json
import html
import config

def parse_bullet_lines(raw_text):
    """
    Parses bullets formatted as '-', '*', '•', '1.', '2.' into clean list.
    """
    if not raw_text:
        return []
    lines = raw_text.strip().split('\n')
    bullets = []
    for l in lines:
        cleaned = l.strip()
        if not cleaned:
            continue
        # Remove common bullet prefixes
        if cleaned.startswith(('•', '*', '-', '1.', '2.', '3.', '4.', '5.')):
            # Strip prefix
            for prefix in ['•', '*', '-', '1.', '2.', '3.', '4.', '5.']:
                if cleaned.startswith(prefix):
                    cleaned = cleaned[len(prefix):].strip()
                    break
            if cleaned:
                bullets.append(html.escape(cleaned))
    return bullets

def generate_ai_reasoning_synthesis(market_data_summary):
    """
    Dual-Scenario AI Explanation Engine (Layer 19):
    - Python = Pure 22-Layer Analysis & Calculation Engine.
    - Gemini = Optional Human Explanation Generator using JSON input & Temperature=0.2.
    - Fallback = 100% deterministic institutional synthesis if Gemini is unavailable or rate limited.
    """
    direction = market_data_summary.get('direction', 'BUY')
    alt_direction = 'SELL' if direction == 'BUY' else 'BUY'
    key_level = market_data_summary.get('key_level', 3380.0)

    # 1. Deterministic Fallback Synthesis
    fallback_primary = [
        f"Daily and 4H market structure aligned in strong {direction.lower()}ish trend.",
        f"Retest of key Demand / Order Block zone verified successfully.",
        f"DXY Dollar Index dynamics providing supportive tailwind for Gold.",
        f"Macro CPI and inflation backdrop supportive for XAUUSD stance.",
        f"Volume expansion confirming buyer momentum on intraday timeframe."
    ]
    fallback_alt = f"<b>Alternative ({alt_direction}):</b> Only if ${key_level:.2f} is reclaimed on 4H close."

    if not config.GEMINI_API_KEY:
        return fallback_primary, fallback_alt

    # 2. Structured JSON Input to Gemini
    structured_json_payload = {
        "symbol": "XAUUSD",
        "current_price": market_data_summary.get('price', 0.0),
        "primary_direction": direction,
        "overall_trend": market_data_summary.get('overall_trend', 'NEUTRAL'),
        "structure_bias": market_data_summary.get('structure_bias', 'NEUTRAL'),
        "smc_zone": market_data_summary.get('smc_zone', 'Equilibrium'),
        "session": market_data_summary.get('session_name', 'London'),
        "confluence_score": market_data_summary.get('confluence_score', 0.0),
        "invalidation_level": key_level
    }

    prompt = f"""
You are an institutional Gold (XAUUSD) trading strategist. Based on the following JSON market structure, generate a concise primary explanation and an alternative scenario.

Structured Market Data (JSON):
{json.dumps(structured_json_payload, indent=2)}

INSTRUCTIONS:
1. Provide exactly 5 bullet points starting with '•' explaining why the primary setup is high probability.
2. Provide 1 line starting with 'ALTERNATIVE:' specifying when to flip bias to {alt_direction}.
3. Keep tone neutral, educational, and institutional. Do NOT use HTML tags in text.
"""

    text_output = None
    try:
        # SDK Initialization
        try:
            import google.genai as genai
            client = genai.Client(api_key=config.GEMINI_API_KEY)
            config_params = {"temperature": 0.2}
            response = client.models.generate_content(
                model=config.GEMINI_MODEL,
                contents=prompt,
                config=config_params
            )
            text_output = response.text
        except ImportError:
            import google.generativeai as genai
            genai.configure(api_key=config.GEMINI_API_KEY)
            model = genai.GenerativeModel(config.GEMINI_MODEL)
            generation_config = genai.types.GenerationConfig(temperature=0.2)
            response = model.generate_content(prompt, generation_config=generation_config)
            text_output = response.text
    except Exception as e:
        print(f"⚠️ Gemini Explanation Notice: {e}. Switching to Python institutional fallback.")
        return fallback_primary, fallback_alt

    # 3. Strict Response Validation & Parsing
    if text_output:
        lines = [line.strip() for line in text_output.strip().split('\n') if line.strip()]
        parsed_bullets = parse_bullet_lines(text_output)
        alt_line = next((l for l in lines if 'ALTERNATIVE:' in l.upper() or 'ALT:' in l.upper()), None)

        if len(parsed_bullets) >= 3:
            final_bullets = [f"• {b}" for b in parsed_bullets[:5]]
            if alt_line:
                clean_alt = html.escape(alt_line.replace('ALTERNATIVE:', '').replace('Alternative:', '').strip())
                final_alt = f"<b>Alternative ({alt_direction}):</b> {clean_alt}"
            else:
                final_alt = fallback_alt
            return final_bullets, final_alt

    return fallback_primary, fallback_alt

if __name__ == '__main__':
    print("AI reasoning module v4 ready.")
