import json
import google.generativeai as genai

API_KEY = "AIzaSyBQLAn_h8eSVyCXeaTBDbdDbg3nd67jjI0"
genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")

from fonction.light_dues import calculate_light_dues
from fonction.vts_dues import calculate_vts_dues
from fonction.pilotage_dues import calculate_pilotage_dues
from fonction.port_dues import calculate_port_dues
from fonction.towage_dues import calculate_towage_dues
from fonction.running_line_dues import calculate_running_lines_dues

CALCULATION_FUNCTIONS = {
    "light_dues": calculate_light_dues,
    "vts_dues": calculate_vts_dues,
    "pilotage_dues": calculate_pilotage_dues,
    "port_dues": calculate_port_dues,
    "towage_dues": calculate_towage_dues,
    "running_lines_dues": calculate_running_lines_dues,
}

def clean_number(value):
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        try:
            return float(value.replace(",", "").replace(" MT", "").strip())
        except:
            return 0.0
    return 0.0

def run_agent(parsed: dict) -> dict:
    gt = clean_number(parsed.get("gross_tonnage") or parsed.get("GT"))
    port = parsed.get("port_name") or parsed.get("port", "").strip()
    days = clean_number(parsed.get("duration_days") or parsed.get("Days Alongside"))
    ops = int(parsed.get("number_of_operations") or parsed.get("Number of Operations") or 2)

    results = {}
    if gt and port and days:
        results["light_dues"] = calculate_light_dues(gt)
        results["port_dues"] = calculate_port_dues(gt, days)
        results["towage_dues"] = calculate_towage_dues(gt, port)
        results["vts_dues"] = calculate_vts_dues(gt, port)
        results["pilotage_dues"] = calculate_pilotage_dues(gt, port)
        results["running_lines_dues"] = calculate_running_lines_dues(port, ops)
    else:
        print("⚠️ Missing required fields: GT, port, or duration")
    return results

def ask_gemini_for_tariff_plan(vessel_data: dict) -> dict:
    prompt = f"""
You are a smart port tariff agent.

Based on the following vessel data, return a JSON object that specifies which tariff functions to apply and any needed parameters.

Supported tariffs:
- light_dues(gt)
- vts_dues(gt, port)
- pilotage_dues(gt, port, movements)
- port_dues(gt, duration_days)
- towage_dues(gt, port)
- running_lines_dues(port)

Format:
{{
  "light_dues": {{"apply": true}},
  "vts_dues": {{"apply": true}},
  "pilotage_dues": {{"apply": true, "movements": 2}},
  "port_dues": {{"apply": true, "duration_days": 3.39}},
  "towage_dues": {{"apply": true}},
  "running_lines_dues": {{"apply": true}}
}}

Vessel:
{json.dumps(vessel_data, indent=2)}
"""
    try:
        response = model.generate_content(prompt)
        raw_text = response.text.strip().replace("```json", "").replace("```", "").strip()
        start = raw_text.find('{')
        end = raw_text.rfind('}') + 1
        json_plan = raw_text[start:end]
        return json.loads(json_plan)
    except Exception as e:
        print("❌ Gemini plan generation failed:", e)
        return {}

def calculate_all_tariffs(vessel_data: dict) -> dict:
    port = vessel_data.get("port", "").strip()
    gt = clean_number(vessel_data.get("gross_tonnage", 0))
    stay = clean_number(vessel_data.get("days_alongside", 1.0))

    print("🧠 Asking Gemini for tariff plan...")
    plan = ask_gemini_for_tariff_plan(vessel_data)

    if not plan:
        print("⚠️ Falling back to rule-based agent...")
        return run_agent(vessel_data)

    results = {}

    for tariff, config in plan.items():
        if not config.get("apply"):
            continue

        func = CALCULATION_FUNCTIONS.get(tariff)
        if not func:
            results[tariff] = "❌ Unknown tariff"
            continue

        try:
            if tariff == "light_dues":
                results[tariff] = func(gt)
            elif tariff == "vts_dues":
                results[tariff] = func(gt, port)
            elif tariff == "pilotage_dues":
                movements = config.get("movements", 2)
                results[tariff] = func(gt, port, movements)
            elif tariff == "port_dues":
                duration = config.get("duration_days", stay)
                results[tariff] = func(gt, duration)
            elif tariff == "towage_dues":
                results[tariff] = func(gt, port)
            elif tariff == "running_lines_dues":
                ops = int(vessel_data.get("number_of_operations") or config.get("ops") or 2)
                results[tariff] = func(port, ops)
        except Exception as e:
            results[tariff] = f"❌ Error: {e}"

    return results
