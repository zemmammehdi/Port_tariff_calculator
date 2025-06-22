import math

def calculate_vts_dues(gross_tonnage: float, port: str) -> float:
    """
    Calculates the Vehicle Traffic Services (VTS) Dues based on gross tonnage and port.
    Reference: Tariff Book April 2024 - March 2025, Section 2.1.1 (Page 6).

    Args:
        gross_tonnage (float): The gross tonnage (GT) of the vessel.
        port (str): The port of call (e.g., "Durban", "Saldanha", "Richards Bay", etc.).

    Returns:
        float: The calculated VTS Dues (pre-VAT).
    """
    vts_rate_durban_saldanha = 0.65 # Rate for Durban and Saldanha Bay
    vts_rate_other_ports = 0.54    # Rate for other ports
    minimum_fee = 235.52           # Minimum fee as per document

    port_lower = port.lower()

    if port_lower == "durban" or port_lower == "saldanha":
        rate_per_gt = vts_rate_durban_saldanha
    else:
        rate_per_gt = vts_rate_other_ports

    calculated_dues = gross_tonnage * rate_per_gt
    # Ensure the calculated amount is not less than the minimum fee
    return max(calculated_dues, minimum_fee)