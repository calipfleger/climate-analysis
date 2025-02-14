import os
import xarray as xr
import cartopy.feature as cfeature
import cartopy.crs as ccrs
import matplotlib.pyplot as plt

def plot_trend_with_region(trend, var_name: str, time_info, var_units="Unknown", start_year=None, end_year=None, cmap="coolwarm"):
    """Plot the linear trend of climate data with proper land and ocean representation."""
    print(f"🖼️ Creating plot for {var_name} trend...")

    time_start, time_end, time_units = time_info
    print(f"📆 Time Info: Start = {time_start}, End = {time_end}, Units = {time_units}")

    fig, ax = plt.subplots(subplot_kw={"projection": ccrs.PlateCarree()})

    # ✅ Debugging dataset structure
    print("📊 DEBUG: NetCDF Dataset Structure Before Plotting:")
    print(trend)
    print(f"📏 Dataset Dimensions: {trend.dims}")
    print(f"📊 Dataset Shape: {trend.shape}")

    # ✅ Ensure trend is an xarray DataArray
    if not isinstance(trend, xr.DataArray):
        print(f"❌ ERROR: 'trend' is not an xarray.DataArray! Got type: {type(trend)}")
        return None

    # ✅ Ensure `lat` and `lon` dimensions exist before plotting
    if "lat" not in trend.dims or "lon" not in trend.dims:
        print(f"⚠️ Warning: Trend data does not have 'lat' and 'lon' dimensions!")
        print(f"📊 Trend dimensions: {trend.dims}")
        return None

    # ✅ Select a single ensemble member if needed
    if "ensemble" in trend.dims:
        print(f"⏳ Selecting the first ensemble member for plotting. Original shape: {trend.shape}")
        trend = trend.isel(ensemble=0)  # Selects first ensemble member
        print(f"✅ Updated shape after selecting ensemble member: {trend.shape}")

    # ✅ Handle NaN values
    print("🔍 Checking for NaN values in trend data...")
    missing_values = trend.isnull().sum().item()
    print(f"📉 Missing values found: {missing_values}")

    trend = trend.fillna(0)  # Replace NaNs with 0
    print("✅ Replaced NaN values with 0.")

    # ✅ Add land first to prevent ocean from masking it
    ax.add_feature(cfeature.LAND, facecolor="none", edgecolor="black")  # Draw land outlines
    ax.coastlines()
    ax.add_feature(cfeature.BORDERS, linestyle=":")
    ax.add_feature(cfeature.OCEAN, facecolor="lightblue")  # Keep ocean blue

    # ✅ Use pcolormesh for gridded data
    img = ax.pcolormesh(trend.lon, trend.lat, trend, transform=ccrs.PlateCarree(), cmap=cmap, shading="auto")
    cbar = plt.colorbar(img, ax=ax, orientation="vertical", label=f"{var_name} Trend ({var_units})")

    # ✅ Add regional analysis box (example coordinates)
    region_box = [(-30, 90), (-30, 270), (30, 270), (30, 90), (-30, 90)]
    region_lats, region_lons = zip(*region_box)
    ax.plot(region_lons, region_lats, transform=ccrs.PlateCarree(), color="red", linewidth=2, linestyle="--")
    print("📍 Added regional analysis box on the map.")

    # ✅ Generate and print figure caption
    caption = (
        f"📊 Figure Caption:\n"
        f"{var_name} Linear Trend ({start_year:.0f}-{end_year:.0f}).\n"
        f"Units: {var_units}.\n"
        f"Red box shows the regional analysis area."
    )
    print(f"🖼️ Figure Caption:\n{caption}\n")

    # ✅ Add caption to plot
    plt.figtext(0.5, -0.05, caption, wrap=True, horizontalalignment="center", fontsize=10)
    plt.title(f"{var_name} Trend ({start_year:.0f}-{end_year:.0f})")

    return fig

def save_figure(fig, var_name: str, dataset_name: str, file_type: str, file_format: str = "png"):
    """Save the generated climate visualization."""
    os.makedirs(SAVE_DIR, exist_ok=True)
    file_name = f"{var_name}_{dataset_name}_{file_type}.{file_format}"
    file_path = os.path.join(SAVE_DIR, file_name)

    fig.savefig(file_path, dpi=300, bbox_inches="tight")
    print(f"📁 Figure saved: {file_path} ✅\n")

