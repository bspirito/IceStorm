# IceStorm: Antarctic Ice Area Analysis

IceStorm is a geospatial analysis tool designed to process Antarctic ice sheet data from KMZ/KML format and calculate accurate ice area coverage over time. The project focuses on high-precision mathematical modeling and automated batch processing of large multi-year datasets.

## 🔬 Mathematical Approach

Calculating the area of ice sheets from satellite-derived KML data requires addressing several geometric challenges:

1.  **Spherical Area Calculation**: Since the data is represented in longitude and latitude on a globe, simple Euclidean geometry is insufficient. We utilize the `area` library to calculate the surface area of polygons on a sphere with a radius of $6,378,137$ meters.
2.  **Handling Polygons with Holes**: Ice sheets often contain internal "melt ponds" or land masses. The algorithm identifies and processes both `outerBoundaryIs` and `innerBoundaryIs` tags, subtracting the area of internal holes from the total outer boundary to ensure net accuracy.
3.  **Geometric Integrity (Closed Polygons)**: Many KML datasets contain unclosed ring structures. Our processing pipeline detects these and automatically closes polygons (matching the last vertex to the first) to satisfy the strict topological requirements of the GeoJSON area calculation standard.
4.  **Unit Conversion**: Results are converted from square meters ($m^2$) to square kilometers ($km^2$) using a $10^{-6}$ scaling factor.

## 🛠️ Data Pipeline

The project consists of several specialized Python scripts:

*   `processKMLData.py`: The core engine that parses KMZ files using `BeautifulSoup` (XML), extracts coordinate strings, and performs the geometric calculations.
*   `generate_ice_plots.py`: A batch processing script that traverses organized yearly folders, extracts daily ice areas, and generates yearly trend reports.
*   `advanced_visualizations.py`: Generates comparative analytics, including multi-year overlays and seasonal polar plots.

## 📊 Visualizations & Insights

We provide several ways to view the Antarctic ice lifecycle:

### 📍 Daily Trend Plots
Standard time-series graphs showing the growth and retreat of ice throughout a single calendar year. These are useful for identifying specific events like sudden calving or rapid melt seasons.

### ❄️ Multi-Year Comparison
Overlaying data from 2011 through 2025 on a single graph allows for easy identification of year-over-year anomalies and long-term climate trends.

### 🌀 Seasonal Polar Plots
By mapping the 366 days of the year to a $360^\circ$ circle, we create a "clock" visualization of the ice cycle. This highlights the extreme seasonality of the Antarctic:
*   **The Winter Expansion**: Ice reaching its maximum radius towards the "South" (late Q3).
*   **The Summer Retreat**: Significant area loss as the plot pulls back toward the center (Q1).

## 📁 Repository Structure
*   `antarctic/`: Organized subdirectories for each year (2011-2025) containing thousands of `.kmz` data files.
*   `results/`: CSV data exports and PNG visualizations.

---
*Note: Due to the large size of the raw geospatial data (~5.6 GB), the `.kmz` files are managed locally and are not tracked in the main Git repository to maintain performance.*
