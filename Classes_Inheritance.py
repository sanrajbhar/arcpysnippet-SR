import arcpy

# Parent class (General feature class)
class FeatureClass:
    def __init__(self, path):
        self.path = path  # Store path
    
    def describe(self):
        """Get info about the feature class"""
        desc = arcpy.Describe(self.path)
        return f"Shape Type: {desc.shapeType}"

# Child class (Specialized for point feature classes)
class PointFeatureClass(FeatureClass):
    def count_points(self):
        """Count the number of points"""
        count = arcpy.GetCount_management(self.path)
        return f"Total Points: {count[0]}"

# Using the classes
fc = FeatureClass(r"C:\Users\sri00571\Downloads\england-latest-free.shp\gis_osm_railways_free_1.shp")
print(fc.describe())  # Just gets description

point_fc = PointFeatureClass(r"C:\Users\sri00571\Downloads\england-latest-free.shp\gis_osm_places_a_free_1.shp")
print(point_fc.describe())  # Inherited from FeatureClass
print(point_fc.count_points())  # New method in PointFeatureClass
