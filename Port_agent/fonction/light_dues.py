import math

def calculate_light_dues(gross_tonnage: float) -> float:
    """
    Calculates the Light Dues based on gross tonnage.
    Assumes vessel is 'All other vessels' and stays less than 60 days for a single call.
    """
    rate_per_100_tons = 117.08
    num_100_ton_units = math.ceil(gross_tonnage / 100)
    return num_100_ton_units * rate_per_100_tons
