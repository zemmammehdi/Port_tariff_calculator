from fastapi import FastAPI, HTTPException, Request
from agent.parser import extract_vessel_data
from agent.planner import calculate_all_tariffs

app = FastAPI()

@app.post("/calculate")
def calculate_tariffs(request: dict):
    user_input = request.get("input_text", "")
    if not user_input:
        raise HTTPException(status_code=400, detail="input_text is required")

    vessel_data = extract_vessel_data(user_input)
    if not vessel_data:
        raise HTTPException(status_code=422, detail="Failed to extract vessel data")

    results = calculate_all_tariffs(vessel_data)
    return {
        "vessel_data": vessel_data,
        "tariffs": results
    }
