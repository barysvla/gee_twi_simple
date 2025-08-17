import ee
import geemap
import numpy as np

def compute_slope(dem, region, scale=90):
    """
    Výpočet sklonu terénu na základě DEM.
    """
    slope = ee.Terrain.slope(dem).rename("Slope")
    # Geom for region in ee_to_numpy
    #geom = slope.geometry() 
    slope_array = geemap.ee_to_numpy(slope, region=region, bands=['Slope'], scale=90)
    slope_array = np.squeeze(slope_array).astype(np.float64)
    return slope_array
