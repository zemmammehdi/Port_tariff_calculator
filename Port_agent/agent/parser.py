import json
import google.generativeai as genai

API_KEY = "Yourapikey"
genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")

def extract_vessel_data(text_prompt: str) -> dict:
    """
    Extracts structured vessel data from raw input using Gemini.
    """
    prompt = f"""
You are a maritime assistant.

Extract the following structured vessel information from the input text and return it as a JSON object with clear field names and values.

Required fields:
- vessel_name
- port
- gross_tonnage
- dwt
- loa
- beam
- draft
- days_alongside
- cargo_quantity
- activity

Input:
{text_prompt}
"""

    try:
        response = model.generate_content(prompt)
        raw_text = response.text.strip().replace("```json", "").replace("```", "").strip()
        start = raw_text.find('{')
        end = raw_text.rfind('}') + 1
        json_string = raw_text[start:end]
        return json.loads(json_string)
    except Exception as e:
        print("❌ Error parsing Gemini response:", e)
        return {}
