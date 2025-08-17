import ee
import geemap

# Import vlastních modulů
from scripts.flow_accumulation import compute_flow_accumulation
from scripts.slope import compute_slope
from scripts.twi import compute_twi
from scripts.visualization import visualize_map
#from scripts.export import export_to_drive, export_to_asset

# !Inicializace GEE!
ee.Initialize(project = 'TADY zadat ID projektu')

# !Definice zájmového území!
geometry = ee.Geometry.Rectangle([14.2, 50.0, 14.6, 50.2])

# Získání středu polygonu a nastavení zoomu
center = geometry.centroid().coordinates().getInfo()

# Načtení DEM
dataset_MERIT = ee.Image("MERIT/Hydro/v1_0_1")
dem = dataset_MERIT.select("elv").clip(geometry)

# Výpočet jednotlivých vrstev
flow_accumulation = compute_flow_accumulation(dem)
slope = compute_slope(dem)
twi = compute_twi(flow_accumulation, slope)

# Kombinace vrstev
#out = dem.addBands(twi) #.addBands(flow_accumulation).addBands(slope)

# Vizualizace
vis_params_twi = {
    "bands": ["TWI_scaled"],
    "min": -529168144.8390943,
    "max": 2694030.111316502,
    "opacity": 1,
    "palette": ["#ff0000", "#ffa500", "#ffff00", "#90ee90", "#0000ff"]
}
#vis_params_slope = {
#    "bands": ["Slope"],
#    "min": 0,
#    "max": 90,
#    "palette": ["yellow", "red"]
#}
#vis_params_dem = {
#    "bands": ["elv"],
#    "min": 0,
#    "max": 3000,
#    "palette": ["black", "white"]
#}

# Vytvoření mapy
Map = visualize_map([
    (twi, vis_params_twi, "TWI") #,
   # (out.select("Slope"), vis_params_slope, "Slope"),
   # (out.select("elv"), vis_params_dem, "Elevation")
])

Map.setCenter(center[0], center[1], zoom=12)
