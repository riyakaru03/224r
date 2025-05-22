import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Set style
plt.style.use('seaborn')
sns.set_palette("husl")

# Read the data
df_18 = pd.read_parquet('data/simulation_data_SP18.parquet')
df_22 = pd.read_parquet('data/simulation_data_SP22.parquet')
df_25 = pd.read_parquet('data/simulation_data_SP25.parquet')
df_rl = pd.read_parquet('data/PPO_baseline_data.parquet')

# Create a figure with subplots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
fig.suptitle('Data Center Simulation Results Comparison', fontsize=16)

# Plot 1: Temperature Distribution
temp_cols = [col for col in df_18.columns if col.startswith('Temp_Z_')]
temp_data = pd.DataFrame({
    '18°C Setpoint': df_18[temp_cols].mean(axis=1),
    '22°C Setpoint': df_22[temp_cols].mean(axis=1),
    '25°C Setpoint': df_25[temp_cols].mean(axis=1),
    'RL Control': df_rl[temp_cols].mean(axis=1)
})

temp_data.plot(ax=ax1)
ax1.set_title('Average Zone Temperatures Over Time')
ax1.set_xlabel('Time Step')
ax1.set_ylabel('Temperature (°C)')
ax1.legend(title='Control Strategy')
ax1.grid(True)

# Plot 2: Energy Consumption
energy_data = pd.DataFrame({
    '18°C Setpoint': df_18['Facility_Total_Electricity_Demand_Rate'],
    '22°C Setpoint': df_22['Facility_Total_Electricity_Demand_Rate'],
    '25°C Setpoint': df_25['Facility_Total_Electricity_Demand_Rate'],
    'RL Control': df_rl['Facility_Total_Electricity_Demand_Rate']
})

energy_data.plot(ax=ax2)
ax2.set_title('Total Electricity Demand Over Time')
ax2.set_xlabel('Time Step')
ax2.set_ylabel('Power Demand (W)')
ax2.legend(title='Control Strategy')
ax2.grid(True)

# Adjust layout and save
plt.tight_layout()
plt.savefig('simulation_results.png', dpi=300, bbox_inches='tight')
plt.close()

# Print summary statistics
print("\nSummary Statistics:")
print("\nAverage Temperature by Control Strategy:")
print(temp_data.mean())
print("\nTotal Energy Consumption by Control Strategy (kWh):")
print(energy_data.sum() / 1000)  # Convert to kWh 