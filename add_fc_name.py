import arcpy
from utils.fc_utils import FeatureClassProcessor  # Import the class


r""" 
If VS Code or Python doesn't detect the module, you can manually add the folder to Python's path:

Modify add_fc_name.py like this:
sys.path.append(r"C:\GIS\Project\utils")  # Add utils folder to sys.path

import arcpy
from fc_utils import FeatureClassProcessor  # Now it works!

Set geodatabase path (Modify this path as needed)

"""

gdb_path = r"C:\Users\sri00571\OneDrive - ARCADIS\Documents\ArcGIS\Projects\MyProject7\test\working.gdb"

# Create an instance of the FeatureClassProcessor
fc_processor = FeatureClassProcessor(gdb_path) #class name to initilisation

# Process all feature classes in the geodatabase
fc_processor.process_all_feature_classes() #function within class to run task
#