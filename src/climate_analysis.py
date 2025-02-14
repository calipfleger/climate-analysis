"""
climate_analysis.py

A modular script for analyzing climate model data from NetCDF files.

Author: [Your Name]
Last Updated: [Date]
"""

import os
from data_loader import load_netcdf, detect_time_format
from trend_analysis import compute_linear_trend, convert_time_to_numeric
from plotting import plot_trend_with_region, save_figure

print("🚀 climate_analysis.py is running!")

# ====== CONFIGURATION ======
DATA_DIR = "data"  
SCENARIOS = ["cesmlme_PRECTvolc"]  
SAVE_DIR = "output_figures"

# ====== MAIN EXECUTION ======
if __name__ == "__main__":
    print("🚀 Starting climate analysis script!")

    for dataset_name in SCENARIOS:
        file_path = os.path.join(DATA_DIR, f"{dataset_name}.nc")
        print(f"📂 Checking file: {file_path}")

        dataset = load_netcdf(file_path)
        if dataset:
            print(f"✅ Dataset loaded: {dataset_name}")

            # Select first available variable
            variable_name = list(dataset.data_vars.keys())[0]
            print(f"📊 Using variable: {variable_name}")

            # Get variable units
            var_units = dataset[variable_name].attrs.get("units", "Unknown")
            print(f"📏 Variable Units: {var_units}")

            # Convert time
            numeric_time = convert_time_to_numeric(dataset)
            if numeric_time is not None:
                start_year, end_year = numeric_time[0], numeric_time[-1]
                print(f"📆 Time Range: {start_year:.2f} - {end_year:.2f}")

            # Compute trend
            trend_map, p_value_map = compute_linear_trend(dataset, variable_name)
            if trend_map is None:
                print(f"❌ ERROR: Trend computation failed for {variable_name}!")
            else:
                print(f"✅ Trend computed for {variable_name}")

            # Detect time format
            time_info = detect_time_format(dataset)

            # Plot trend
            print(f"🖼️ Plotting trend for {variable_name}...")
            fig_trend = plot_trend_with_region(
                trend=trend_map,
                var_name=variable_name,
                time_info=time_info,
                var_units=var_units,
                start_year=start_year,
                end_year=end_year
            )

            # Save figure
            if fig_trend:
                print("📁 Saving figure...")
                save_figure(fig_trend, variable_name, dataset_name, "trend", "png")
                print("✅ Figure saved successfully!")
            else:
                print("❌ No figure to save!")

