import geemap
import ee
from IPython.display import display

def visualize_map(layers):
    """
    Create an interactive map with layers.
    :param layers: List of tuples (image, vis_params, name) to visualize.
    """
    Map = geemap.Map()
    
    for layer in layers:
        image, vis_params, name = layer
        if isinstance(image, ee.Image):  # Verify the object is an ee.Image
            Map.addLayer(image, vis_params, name)
        else:
            print(f"⚠ Warning: Layer '{name}' is not an ee.Image and will not be displayed!")
    
    return Map
