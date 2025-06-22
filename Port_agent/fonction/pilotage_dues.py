import math

def calculate_pilotage_dues(gross_tonnage: float, port: str, num_services: int = 2) -> float:
    """
    Calculates Pilotage Dues based on gross tonnage and port.
    Assumes normal entering and leaving services (2 services).
    Reference: Tariff Book April 2024 - March 2025, Section 3.3 (Page 7).

    Args:
        gross_tonnage (float): The gross tonnage (GT) of the vessel.
        port (str): The port of call.
        num_services (int): Number of pilotage services (e.g., 2 for entering and leaving).

    Returns:
        float: The calculated Pilotage Dues (pre-VAT).
    """
    # Pilotage rates per port, extracted from the table on Page 7.
    pilotage_rates = {
        "richards bay": {"basic_fee": 30960.46, "rate_per_100_tons": 10.93},
        "durban": {"basic_fee": 18608.61, "rate_per_100_tons": 9.72},
        "port elizabeth": {"basic_fee": 8970.00, "rate_per_100_tons": 14.33}, # Includes Ngqura
        "ngqura": {"basic_fee": 8970.00, "rate_per_100_tons": 14.33},
        "cape town": {"basic_fee": 6342.39, "rate_per_100_tons": 10.20},
        "saldanha": {"basic_fee": 9673.57, "rate_per_100_tons": 13.66},
        "other ports": {"basic_fee": 6547.45, "rate_per_100_tons": 10.49}, # For Mossel Bay, East London, etc.
    }

    port_lower = port.lower()
    
    # Map the port to the correct dictionary key for rates.
    if port_lower in ["port elizabeth", "ngqura"]:
        port_key = "port elizabeth"
    elif port_lower == "richards bay":
        port_key = "richards bay"
    elif port_lower == "durban":
        port_key = "durban"
    elif port_lower == "cape town":
        port_key = "cape town"
    elif port_lower == "saldanha":
        port_key = "saldanha"
    else:
        port_key = "other ports" # Fallback for ports not explicitly listed.

    rates = pilotage_rates.get(port_key)
    if not rates:
        raise ValueError(f"Pilotage rates for port '{port}' not found.")

    basic_fee = rates["basic_fee"]
    rate_per_100_tons = rates["rate_per_100_tons"]

    # Calculate the number of 100-ton units, rounded up.
    num_100_ton_units = math.ceil(gross_tonnage / 100)

    # Calculate the cost per service (e.g., entering or leaving the port).
    cost_per_service = basic_fee + (num_100_ton_units * rate_per_100_tons)

    # Total pilotage dues for all services (e.g., entering and leaving).
    return cost_per_service * num_services