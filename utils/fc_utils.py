import arcpy
import os

class FeatureClassProcessor:
    def __init__(self, gdb_path):
        """Initialize with the geodatabase path"""
        self.gdb_path = gdb_path

    def add_fc_name_field(self, fc_path, field_name="FC_NAME"):
        """Adds a field and populates it with the feature class name"""
        try:
            fc_name = os.path.basename(fc_path)  # Extract feature class name

            # Check if the field already exists
            fields = [f.name for f in arcpy.ListFields(fc_path)]
            if field_name not in fields:
                arcpy.AddField_management(fc_path, field_name, "TEXT", field_length=100)
                print(f"Field '{field_name}' added to {fc_name}.")

            # Update field values with the feature class name
            with arcpy.da.UpdateCursor(fc_path, [field_name]) as cursor:
                for row in cursor:
                    row[0] = fc_name
                    cursor.updateRow(row)

            print(f"Field '{field_name}' updated with feature class name '{fc_name}' in {fc_name}.")

        except Exception as e:
            print(f"Error processing {fc_name}: {e}")

    def process_all_feature_classes(self):
        """Iterates through all feature classes in the geodatabase"""
        arcpy.env.workspace = self.gdb_path  # Set the workspace
        feature_classes = arcpy.ListFeatureClasses()  # Get all feature classes

        if not feature_classes:
            print("No feature classes found in the geodatabase.")
            return

        print(f"Processing {len(feature_classes)} feature classes in {self.gdb_path}...")

        for fc in feature_classes:
            fc_path = os.path.join(self.gdb_path, fc)  # Get full path
            self.add_fc_name_field(fc_path)  # Call function to add field

        print("Processing complete for all feature classes.")
