import xarray as xr
import numpy as np
import cftime

def load_netcdf(file_path: str):
    """Load a NetCDF dataset using xarray."""
    try:
        ds = xr.open_dataset(file_path)
        print(f"✅ Successfully loaded dataset: {file_path}")
        print(f"📊 Available variables: {list(ds.data_vars.keys())}\n")
        return ds
    except Exception as e:
        print(f"❌ Error loading file: {e}\n")
        return None

def detect_time_format(ds):
    """Detect and log the time dimension format in a dataset."""
    if "time" not in ds:
        print("⚠️ No time dimension found in dataset!\n")
        return None

    time_dim = ds["time"]
    time_units = time_dim.attrs.get("units", "Unknown")

    # ✅ Fix: Convert CFTime to NumPy datetime before extracting min/max
    time_values = time_dim.values
    if isinstance(time_values[0], cftime.datetime):
        print("⏳ Converting CFTime to NumPy datetime format...")
        time_values = np.array([np.datetime64(t.isoformat()) for t in time_values])  # Convert to NumPy datetime64

    time_start = np.datetime_as_string(time_values.min(), unit="D")
    time_end = np.datetime_as_string(time_values.max(), unit="D")

    print(f"📆 Time detected: {time_start} to {time_end} ({time_units})\n")
    return time_start, time_end, time_units

