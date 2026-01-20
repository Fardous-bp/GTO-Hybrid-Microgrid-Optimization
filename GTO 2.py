import numpy as np
import matplotlib.pyplot as plt

# --- 1. DEFINE WINNING SYSTEM (GTO HYBRID) ---
# Capital Costs
capex_total = 103760709
npc_total = 103760709 # Assuming O&M is low for simplicity in this check, or use your full NPC calculation
# Generation Data (Annual)
solar_capacity_kw = 66785
biogas_capacity_kw = 11876
battery_capacity_kwh = 46325

# Annual Production (Approximate based on capacity)
# Solar: 66.8 MW * 4.6 hours * 365 days
annual_solar_kwh = 66785 * 4.6 * 365 
# Biogas: Runs during blackouts (Assume 500 hours/year for emergency)
annual_biogas_kwh = 11876 * 500 
# Total Load Served
total_load_served_kwh = 450000 * 365 # 450MWh/day * 365

# --- 2. CALCULATE LCOE (Levelized Cost of Energy) ---
# Simple LCOE = Total NPC / (Annual Energy * 20 Years)
# This is a simplified metric for comparison
lcoe = npc_total / (total_load_served_kwh * 20)

print("="*50)
print(f"LCOE ANALYSIS")
print("="*50)
print(f"Total Annual Generation: {total_load_served_kwh/1e6:,.2f} GWh")
print(f"Levelized Cost of Energy (LCOE): ${lcoe:.4f} / kWh")
print(f"Current Grid Price: $0.1050 / kWh")
print(f"Savings per kWh: ${0.105 - lcoe:.4f} / kWh")

# --- 3. CARBON EMISSION ANALYSIS ---
# Grid Emission Factor (Bangladesh): ~0.6 kg CO2/kWh (Gas heavy grid)
# Diesel Emission Factor: ~0.8 kg CO2/kWh
grid_emissions_factor = 0.6
diesel_emissions_factor = 0.8
renewable_emissions_factor = 0.0 # Solar is 0

# Scenario A: Business as Usual (Grid + Diesel Backup)
# Assume 10% outage covered by Diesel, 90% by Grid
bau_emissions = (total_load_served_kwh * 0.90 * grid_emissions_factor) + \
                (total_load_served_kwh * 0.10 * diesel_emissions_factor)

# Scenario B: Your GTO System (Solar + Biogas)
# Solar (0 CO2)
# Biogas (Considered Carbon Neutral or very low emission relative to diesel)
# Let's assume Biogas emits 0.05 kg/kWh (processing)
gto_emissions = (annual_biogas_kwh * 0.05) 

co2_saved_kg = bau_emissions - gto_emissions
co2_saved_tons = co2_saved_kg / 1000

print("\n" + "="*50)
print(f"ENVIRONMENTAL IMPACT (Annual)")
print("="*50)
print(f"BAU Emissions (Grid/Diesel): {bau_emissions/1000:,.0f} tons CO2")
print(f"GTO System Emissions:        {gto_emissions/1000:,.0f} tons CO2")
print(f"Net CO2 Avoided:             {co2_saved_tons:,.0f} tons/year")
print(f"Equivalent Cars Taken off Road: {co2_saved_tons/4.6:,.0f} cars")

# --- 4. SENSITIVITY ANALYSIS (The "High IF" Requirement) ---
# We test: What happens to NPC if Battery Price changes?
# Range: -20% to +20% price change
battery_prices = np.linspace(250, 400, 10) # $250 to $400
# Calculate NPC for HOMER (Pure Battery) vs GTO (Hybrid) at these prices

# HOMER (75 MWh Battery)
homer_base_capex_no_batt = 111000000 - (75000 * 320) # Remove battery cost
homer_npcs = [homer_base_capex_no_batt + (75000 * p) for p in battery_prices]

# GTO (46.3 MWh Battery)
gto_base_capex_no_batt = 103760709 - (46325 * 320) # Remove battery cost
gto_npcs = [gto_base_capex_no_batt + (46325 * p) for p in battery_prices]

# Plotting Sensitivity
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman']
plt.rcParams['font.size'] = 12

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(battery_prices, np.array(homer_npcs)/1e6, label='HOMER Pro (Pure Storage)', marker='o', linewidth=2, color='#ff7f0e')
ax.plot(battery_prices, np.array(gto_npcs)/1e6, label='GTO (Hybrid)', marker='s', linewidth=2, color='#1f77b4')

ax.set_xlabel('Battery Unit Price ($/kWh)')
ax.set_ylabel('Total System NPC ($ Million)')
ax.set_title('Sensitivity Analysis: Impact of Battery Cost on System Feasibility')
ax.grid(True, linestyle='--', alpha=0.6)
ax.legend()

plt.tight_layout()
plt.savefig('Fig7_Sensitivity.png', dpi=300)
plt.show()