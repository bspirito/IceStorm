import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import glob
import os
import re

def generate_advanced_plots():
    csv_files = glob.glob("antarctic_areas_*.csv")
    csv_files = [f for f in csv_files if "master" not in f]
    
    if not csv_files:
        print("No CSV files found to plot.")
        return

    plt.style.use('ggplot')

    # 1. Polar Plot (Seasonality)
    fig_polar = plt.figure(figsize=(10, 10))
    ax_polar = fig_polar.add_subplot(111, projection='polar')
    
    # 2. Multi-year comparison
    fig_multi, ax_multi = plt.subplots(figsize=(14, 7))

    for file in sorted(csv_files):
        year_match = re.search(r"(\d{4})", file)
        if not year_match: continue
        year = year_match.group(1)
        
        df = pd.read_csv(file)
        if df.empty or df['Area_km2'].max() == 0:
            continue
            
        df = df.sort_values('Day')
        
        # Polar data
        # Days 1-366 mapped to 0 to 2*pi
        theta = (df['Day'] / 366) * 2 * np.pi
        radii = df['Area_km2']
        
        ax_polar.plot(theta, radii, label=year, alpha=0.8)
        ax_multi.plot(df['Day'], df['Area_km2'], label=year, alpha=0.8)

    # Finalize Polar Plot
    ax_polar.set_theta_zero_location('N')
    ax_polar.set_theta_direction(-1)
    ax_polar.set_xticks(np.linspace(0, 2*np.pi, 12, endpoint=False))
    ax_polar.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    ax_polar.set_title("Antarctic Ice Area Seasonal Cycle (Polar)", va='bottom', fontsize=15)
    ax_polar.legend(loc='upper right', bbox_to_anchor=(1.2, 1.1))
    fig_polar.savefig("antarctic_ice_polar_seasonal.png", bbox_inches='tight')
    
    # Finalize Multi-year Plot
    ax_multi.set_title("Antarctic Ice Area Comparison (Multi-Year)", fontsize=15)
    ax_multi.set_xlabel("Day of Year")
    ax_multi.set_ylabel("Area (km²)")
    ax_multi.legend(loc='upper left', bbox_to_anchor=(1, 1))
    ax_multi.grid(True)
    fig_multi.tight_layout()
    fig_multi.savefig("antarctic_ice_multi_year_trend.png", bbox_inches='tight')

    print("Advanced plots saved: antarctic_ice_polar_seasonal.png, antarctic_ice_multi_year_trend.png")

if __name__ == "__main__":
    generate_advanced_plots()
