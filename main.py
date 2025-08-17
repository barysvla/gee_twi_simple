import ee
import geemap

# Import custom modules
from scripts.flow_accumulation import compute_flow_accumulation
from scripts.slope import compute_slope
from scripts.twi import compute_twi
from scripts.visualization import visualize_map
# from scripts.export import export_to_drive, export_to_asset

# !GEE initialization!
ee.Initialize(project = 'Enter the GEE project ID here')

# !Define area of interest (AOI)!
geometry = ee.Geometry.Rectangle([14.2, 50.0, 14.6, 50.2])

# Get polygon centroid and configure zoom
center = geometry.centroid().coordinates().getInfo()

# Load DEM
dataset_MERIT = ee.Image("MERIT/Hydro/v1_0_1")
dem = dataset_MERIT.select("elv").clip(geometry)

# Compute individual layers
flow_accumulation = compute_flow_accumulation(dem)
slope = compute_slope(dem)
twi = compute_twi(flow_accumulation, slope)

# Combine layers
# out = dem.addBands(twi)  # .addBands(flow_accumulation).addBands(slope)

# Visualization
vis_params_twi = {
    "bands": ["TWI_scaled"],
    "min": -529168144.8390943,
    "max": 2694030.111316502,
    "opacity": 1,
    "palette": ["#ff0000", "#ffa500", "#ffff00", "#90ee90", "#0000ff"]
}
# vis_params_slope = {
#     "bands": ["Slope"],
#     "min": 0,
#     "max": 90,
#     "palette": ["yellow", "red"]
# }
# vis_params_dem = {
#     "bands": ["elv"],
#     "min": 0,
#     "max": 3000,
#     "palette": ["black", "white"]
# }

# Create the map
Map = visualize_map([
    (twi, vis_params_twi, "TWI")  # ,
    # (out.select("Slope"), vis_params_slope, "Slope"),
    # (out.select("elv"), vis_params_dem, "Elevation")
])

Map.setCenter(center[0], center[1], zoom=12)
