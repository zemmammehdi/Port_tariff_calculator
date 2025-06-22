import math

def calculate_towage_dues(gross_tonnage: float, port: str, num_services: int = 2) -> float:
    """
    Calculates Towage Dues based on gross tonnage and port.
    Assumes two services (entering and leaving).
    Reference: Tariff Book April 2024 - March 2025, Section 3.6 (Page 8).

    Args:
        gross_tonnage (float): The gross tonnage (GT) of the vessel.
        port (str): The port of call.
        num_services (int): Number of towage services (e.g., 2 for entering and leaving).

    Returns:
        float: The calculated Towage Dues (pre-VAT).
    """
    # Define rates per tonnage band for Durban.
    # Data is extracted from the "Durban" column in the table under Section 3.6.
    # GT bands are "Up to 2000", "2001 to 10000", "10001 to 50000",
    # "50001 to 100000", "Above 100000".
    towage_rates_durban = [
        {"min_gt": 0, "max_gt": 2000, "base_fee": 8140.00, "rate_per_100_tons": 0},
        {"min_gt": 2001, "max_gt": 10000, "base_fee": 12633.99, "rate_per_100_tons": 268.99},
        {"min_gt": 10001, "max_gt": 50000, "base_fee": 38494.51, "rate_per_100_tons": 84.95},
        {"min_gt": 50001, "max_gt": 100000, "base_fee": 73118.07, "rate_per_100_tons": 32.24},
        {"min_gt": 100001, "max_gt": float('inf'), "base_fee": 93548.13, "rate_per_100_tons": 23.65}
    ]

    port_lower = port.lower()

    # This function is currently optimized and verified only for Durban based on the provided example.
    # For other ports, their specific rate tables would need to be added.
    if port_lower != "durban":
        print(f"Warning: Towage Dues calculation is currently implemented only for Durban. Port '{port}' is not supported for verification.")
        return 0.0

    cost_per_service = 0.0
    for band in towage_rates_durban:
        # Find the correct tonnage band for the vessel.
        if band["min_gt"] <= gross_tonnage <= band["max_gt"]:
            cost_per_service = band["base_fee"]
            # Apply the incremental rate if applicable for this band.
            if band["rate_per_100_tons"] > 0:
                tons_for_incremental = 0
                # Calculate tons above the lower threshold of the band.
                if band["min_gt"] == 2001:
                    tons_for_incremental = gross_tonnage - 2000
                elif band["min_gt"] == 10001:
                    tons_for_incremental = gross_tonnage - 10000
                elif band["min_gt"] == 50001:
                    tons_for_incremental = gross_tonnage - 50000
                elif band["min_gt"] == 100001:
                    tons_for_incremental = gross_tonnage - 100000
                
                # Round up the number of 100-ton units for the incremental charge.
                num_100_ton_units_incremental = math.ceil(tons_for_incremental / 100)
                cost_per_service += num_100_ton_units_incremental * band["rate_per_100_tons"]
            break # The correct band has been found and processed.

    # Total towage dues for all services (e.g., entering and leaving).
    return cost_per_service * num_services