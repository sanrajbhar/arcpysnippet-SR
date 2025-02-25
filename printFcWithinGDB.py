import arcpy
import os

# Set geodatabase
input_gdb = r"C:\Users\sri00571\OneDrive - ARCADIS\Documents\ArcGIS\Projects\MyProject7\MyProject7.gdb"# path to geodatabase""

# Get list of polygon feature classes in GDB
walk = arcpy.da.Walk(input_gdb, datatype="FeatureClass")
fc_list = [
    os.path.join(root, feature_class)
    for root, data_sets, feature_classes in walk
    for feature_class in feature_classes
]

print(*fc_list, sep="\n")