"""
trend_analysis.py

Functions for processing climate model data, computing trends, and handling time conversion.

Features:
✅ Converts CFTime to numeric values (fixes CESM month shift)
✅ Computes linear trends with statistical significance
✅ Computes regional time series

Author: [Your Name]
Last Updated: [Date]
"""

import numpy as np
import cftime
import xarray as xr
from scipy.stats import linregress

def convert_time_to_numeric(ds):
    """Convert CESM CFTime objects to numeric years, correcting for 1-month offset."""
    if "time" not in ds:
        print("❌ ERROR: No 'time' variable found in dataset!")
        return None

    time_var = ds["time"]
    
    if isinstance(time_var.values[0], cftime.datetime):
        print("⏳ Converting CFTime to numeric values (correcting CESM month shift)...")
        numeric_time = np.array([t.year + (t.month) / 12 for t in time_var.values])  # ✅ Fix: No (-1) to keep months correct
        
        # ✅ Print Start, End Date, and Frequency
        start_year = numeric_time[0]
        end_year = numeric_time[-1]
        frequency = round((numeric_time[1] - numeric_time[0]) * 12)  # Convert to months
        print(f"📆 Time Range: {start_year:.2f} - {end_year:.2f} ({frequency} months per step)")
        
        return numeric_time
    else:
        return time_var.values.astype(float)

def compute_regional_timeseries(ds, var_name: str):
    """Compute a regional mean time series for climate data."""
    if var_name not in ds:
        print(f"❌ ERROR: Variable {var_name} not found in dataset!")
        return None

    regional_mean = ds[var_name].mean(dim=["lat", "lon"])
    print(f"✅ Computed regional mean time series for {var_name} 🌍\n")
    return regional_mean

def compute_linear_trend(ds, var_name: str):
    """Compute a linear trend and statistical significance."""
    print(f"🔍 Computing trend for {var_name}...")

    if var_name not in ds:
        print(f"❌ ERROR: Variable {var_name} not found in dataset!")
        return None, None

    if "time" not in ds:
        print(f"❌ ERROR: No 'time' dimension found in dataset!")
        return None, None

    # ✅ Convert CFTime to numeric before using it
    time_values = convert_time_to_numeric(ds)
    if time_values is None:
        print("❌ ERROR: Time conversion failed!")
        return None, None

    var_data = ds[var_name]

    if len(time_values) < 2:
        print(f"❌ ERROR: Not enough time points to compute trend!")
        return None, None

    def linreg(y):
        """Helper function for computing linear regression for each grid point."""
        slope, intercept, r_value, p_value, std_err = linregress(time_values, y)
        return slope, p_value

    try:
        slope, p_value = xr.apply_ufunc(
            linreg, var_data,
            input_core_dims=[["time"]],
            output_core_dims=[[], []],
            vectorize=True
        )
        print(f"📉 Trend computed successfully for {var_name}!")
    except Exception as e:
        print(f"❌ Trend computation failed: {e}")
        return None, None

    return slope, p_value

