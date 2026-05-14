import os
import pandas as pd
import matplotlib.pyplot as plt
from processKMLData import processKMLData
from tqdm import tqdm

def generate_plots():
    data_dir = os.path.join("antarctic", "2011")
    if not os.path.exists(data_dir):
        print(f"Error: Directory {data_dir} not found.")
        return

    results = []
    files = [f for f in os.listdir(data_dir) if f.endswith(".kmz")]
    files.sort()

    print(f"Processing {len(files)} files...")
    
    # Initialize CSV with header
    with open("antarctic_areas_2011.csv", "w") as f:
        f.write("Day,Area_km2\n")

    for filename in tqdm(files):
        filepath = os.path.join(data_dir, filename)
        try:
            area_km2 = processKMLData(filepath)
            # Extract day from filename antarctic_2011XXX.kmz
            day_str = filename.replace("antarctic_2011", "").replace(".kmz", "")
            day = int(day_str)
            
            # Save result immediately
            with open("antarctic_areas_2011.csv", "a") as f:
                f.write(f"{day},{area_km2}\n")
            
            results.append({"Day": day, "Area_km2": area_km2})
        except Exception as e:
            print(f"Error processing {filename}: {e}")

    df = pd.DataFrame(results)
    
    # Plotting
    plt.figure(figsize=(12, 6))
    plt.plot(df["Day"], df["Area_km2"], marker='o', linestyle='-', color='b')
    plt.title("Antarctic Ice Area - 2011")
    plt.xlabel("Day of Year")
    plt.ylabel("Area (km²)")
    plt.grid(True)
    plt.savefig("antarctic_ice_trend_2011.png")
    print("Plot saved as antarctic_ice_trend_2011.png")

if __name__ == "__main__":
    generate_plots()
