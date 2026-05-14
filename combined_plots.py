import pandas as pd
import matplotlib.pyplot as plt
import datetime

def generate_combined_plots():
    master_file = "antarctic_areas_master.csv"
    try:
        df = pd.read_csv(master_file)
    except FileNotFoundError:
        print(f"Error: {master_file} not found. Please run generate_ice_plots.py first.")
        return

    if df.empty:
        print("Error: Master CSV is empty.")
        return

    # Create a proper datetime column for continuous timeline
    def calculate_date(row):
        return datetime.datetime(int(row['Year']), 1, 1) + datetime.timedelta(days=int(row['Day']) - 1)

    df['Date'] = df.apply(calculate_date, axis=1)
    df = df.sort_values('Date')

    plt.style.use('seaborn-v0_8-muted')

    # 1. Continuous Timeline Plot
    plt.figure(figsize=(20, 8))
    plt.plot(df['Date'], df['Area_km2'], color='tab:blue', linewidth=1.5, alpha=0.9)
    plt.fill_between(df['Date'], df['Area_km2'], color='tab:blue', alpha=0.1)
    
    plt.title("Antarctic Ice Area: Continuous 14-Year Timeline (2011-2025)", fontsize=18, pad=20)
    plt.xlabel("Year", fontsize=14)
    plt.ylabel("Ice Area (km²)", fontsize=14)
    plt.grid(True, which='both', linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.savefig("antarctic_ice_continuous_timeline.png", dpi=300)
    
    # 2. Refined Multi-Year Overlay (Seasonality)
    plt.figure(figsize=(15, 8))
    years = sorted(df['Year'].unique())
    colors = plt.cm.viridis(pd.Series(range(len(years))) / len(years))
    
    for i, year in enumerate(years):
        year_data = df[df['Year'] == year]
        plt.plot(year_data['Day'], year_data['Area_km2'], label=str(year), color=colors[i], alpha=0.8, linewidth=2)

    plt.title("Antarctic Ice Area: Multi-Year Seasonal Overlay", fontsize=18, pad=20)
    plt.xlabel("Day of Year", fontsize=14)
    plt.ylabel("Ice Area (km²)", fontsize=14)
    plt.legend(title="Year", bbox_to_anchor=(1.02, 1), loc='upper left', fontsize=10)
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.savefig("antarctic_ice_seasonal_overlay.png", dpi=300)

    print("Combined plots generated: antarctic_ice_continuous_timeline.png and antarctic_ice_seasonal_overlay.png")

if __name__ == "__main__":
    generate_combined_plots()
