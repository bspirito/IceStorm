import os
import pandas as pd
import matplotlib.pyplot as plt
from processKMLData import processKMLData
from tqdm import tqdm

def generate_plots():
    base_data_dir = "antarctic"
    if not os.path.exists(base_data_dir):
        print(f"Error: Directory {base_data_dir} not found.")
        return

    # Find all year directories
    years = [d for d in os.listdir(base_data_dir) if os.path.isdir(os.path.join(base_data_dir, d)) and d.isdigit()]
    years.sort()
    
    all_results = []

    for year in years:
        year_dir = os.path.join(base_data_dir, year)
        files = [f for f in os.listdir(year_dir) if f.endswith(".kmz")]
        files.sort()

        if not files:
            continue

        print(f"\nProcessing Year {year} ({len(files)} files)...")
        year_results = []
        
        # Initialize/Overwrite CSV for this specific year
        year_csv = f"antarctic_areas_{year}.csv"
        with open(year_csv, "w") as f:
            f.write("Day,Area_km2\n")

        for filename in tqdm(files):
            filepath = os.path.join(year_dir, filename)
            try:
                area_km2 = processKMLData(filepath)
                
                # Extract day - handle both "antarctic_2011XXX" and "antarctic_line_2012XXX"
                # Find the 3 digits at the end before .kmz
                day_match = re.search(r"(\d{3})\.kmz$", filename)
                if day_match:
                    day = int(day_match.group(1))
                else:
                    # Fallback
                    day_str = "".join(filter(str.isdigit, filename))[-3:]
                    day = int(day_str)
                
                # Save result immediately to year CSV
                with open(year_csv, "a") as f:
                    f.write(f"{day},{area_km2}\n")
                
                result = {"Year": int(year), "Day": day, "Area_km2": area_km2}
                year_results.append(result)
                all_results.append(result)
            except Exception as e:
                print(f"Error processing {filename}: {e}")

        # Generate plot for this year
        if year_results:
            df_year = pd.DataFrame(year_results)
            plt.figure(figsize=(12, 6))
            plt.plot(df_year["Day"], df_year["Area_km2"], marker='o', linestyle='-', markersize=2)
            plt.title(f"Antarctic Ice Area - {year}")
            plt.xlabel("Day of Year")
            plt.ylabel("Area (km²)")
            plt.grid(True)
            plt.savefig(f"antarctic_ice_trend_{year}.png")
            plt.close()

    # Save master CSV
    if all_results:
        master_df = pd.DataFrame(all_results)
        master_df.to_csv("antarctic_areas_master.csv", index=False)
        
        # Multi-year comparison plot
        plt.figure(figsize=(15, 8))
        for year in years:
            year_data = master_df[master_df["Year"] == int(year)]
            if not year_data.empty:
                plt.plot(year_data["Day"], year_data["Area_km2"], label=str(year), alpha=0.7)
        
        plt.title("Antarctic Ice Area Comparison (Multi-Year)")
        plt.xlabel("Day of Year")
        plt.ylabel("Area (km²)")
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.grid(True)
        plt.tight_layout()
        plt.savefig("antarctic_ice_multi_year_comparison.png")
        print("\nAll years processed. Master results and comparison plot saved.")

if __name__ == "__main__":
    import re
    generate_plots()
