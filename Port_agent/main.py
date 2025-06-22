from agent.parser import extract_vessel_data
from agent.planner import calculate_all_tariffs

def main():
    print("🚢 South African Port Tariff Calculator\n")

    user_input = """
Calculate the different tariffs payable by the following vessel berthing at the port of Durban:

Vessel Details:
General
Vessel Name: SUDESTADA
Built: 2010
Flag: MLT - Malta
Classification Society: Registro Italiano Navale

Main Details
Type: Bulk Carrier
DWT: 93,274
GT / NT: 51,300 / 31,192
LOA (m): 229.2
Beam (m): 38
Drafts SW S / W / T (m): 14.9 / 0 / 0

Cargo Details
Cargo Quantity: 40,000 MT
Days Alongside: 3.39 days

Activity/Operations
Activity: Exporting Iron Ore
Number of Operations: 2
"""

    print("🔍 Extracting vessel data using Gemini...")
    vessel_data = extract_vessel_data(user_input)

    if not vessel_data:
        print("❌ Failed to extract vessel information.")
        return

    print("\n✅ Vessel Information:")
    for key, value in vessel_data.items():
        print(f"  {key}: {value}")

    print("\n🧮 Calculating tariffs...\n")
    tariff_results = calculate_all_tariffs(vessel_data)

    if not tariff_results:
        print("❌ No tariffs calculated.")
        return

    print("📊 Tariff Breakdown:")
    total = 0.0
    for k, v in tariff_results.items():
        label = k.replace("_", " ").capitalize()

        if isinstance(v, (int, float)):
            print(f"  {label}: R {v:,.2f}")
            total += v
        else:
            print(f"  {label}: {v} ⚠️")

    print(f"\n💰 Total (pre-VAT): R {total:,.2f}")
    print("\n✅ Done.")

if __name__ == "__main__":
    main()
