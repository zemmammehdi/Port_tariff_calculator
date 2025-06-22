import math

def calculate_port_dues(gross_tonnage: float, days_in_port: float, engaged_in_cargo_working: bool = True) -> float:
    """
    Calculates Port Dues based on gross tonnage and duration of stay.
    Reference: Tariff Book April 2024 - March 2025, Section 4.1.1 (Page 11).

    Args:
        gross_tonnage (float): The gross tonnage (GT) of the vessel.
        days_in_port (float): The total number of days the vessel is in port (can be fractional).
        engaged_in_cargo_working (bool): True if the vessel is engaged in cargo working, False otherwise.
                                          (This variable is included for future compliance if reductions
                                          become relevant, but does not affect the current example calculation).

    Returns:
        float: The calculated Port Dues (pre-VAT).
    """
    basic_fee_per_100_tons = 192.73
    incremental_fee_per_100_tons_per_24h = 57.79

    # Calculate the number of 100-ton units, rounded up.
    num_100_ton_units = math.ceil(gross_tonnage / 100)

    # Calculate the basic charge (one-time entry component based on tonnage).
    basic_charge = num_100_ton_units * basic_fee_per_100_tons

    # Calculate the incremental charge based on actual days in port (pro rata application).
    # The document specifies "a part of a 24 hour period being applied pro rata".
    incremental_charge = num_100_ton_units * incremental_fee_per_100_tons_per_24h * days_in_port

    total_port_dues = basic_charge + incremental_charge

    # Reductions or surcharges mentioned in Section 4.1.1 do not apply
    # to the example scenario (cargo working vessel, stay < 30 days, etc.).
    return total_port_dues