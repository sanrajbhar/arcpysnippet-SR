"""
SR_ArcpyDefinedFunc.py - GIS Helper Functions using ArcPy

This script provides utility functions for listing and processing 
Feature Classes (FCs) in a workspace (folder or geodatabase).
"""

import arcpy
import os
import csv


def list_fcs_in_folder(workspace):
    """
    Recursively list all shapefiles and feature classes in a folder and its subfolders.

    :param workspace: The root folder path containing GIS data.
    :return: A list of full paths to all feature classes found.
    """
    try:
        feature_classes = []
        walk = arcpy.da.Walk(workspace, datatype="FeatureClass")

        for dirpath, _, filenames in walk:
            for filename in filenames:
                feature_classes.append(os.path.join(dirpath, filename))

        return feature_classes

    except Exception as e:
        print(f"❌ Error listing feature classes: {e}")
        return []


def list_fcs_in_gdb(gdb_path):
    """
    List all Feature Classes in a Geodatabase (GDB), including inside Feature Datasets.

    :param gdb_path: Path to the Geodatabase.
    :return: A list of feature class names inside the GDB.
    """
    try:
        arcpy.env.workspace = gdb_path
        print(f"Processing GDB: {arcpy.env.workspace}")

        feature_classes = []
        for fds in arcpy.ListDatasets("", "feature") + [""]:
            for fc in arcpy.ListFeatureClasses("", "", fds):
                feature_classes.append(os.path.join(fds, fc))

        return feature_classes

    except Exception as e:
        print(f"❌ Error listing feature classes in GDB: {e}")
        return []


def add_folder_name_as_field(workspace):
    """
    Adds a field ('Folder') containing the name of the parent folder for each feature class.

    :param workspace: The folder containing feature classes.
    """
    try:
        fcs = list_fcs_in_folder(workspace)

        for fc in fcs:
            field_name = "Folder"
            if not arcpy.ListFields(fc, field_name):
                arcpy.AddField_management(fc, field_name, "TEXT", field_length=250)

            folder_name = os.path.basename(os.path.dirname(fc))

            with arcpy.da.UpdateCursor(fc, [field_name]) as cursor:
                for row in cursor:
                    row[0] = folder_name
                    cursor.updateRow(row)

            print(f"✅ Added folder name to {fc}")

    except Exception as e:
        print(f"❌ Error adding folder name as a field: {e}")


def add_fc_name_as_field(workspace):
    """
    Adds a field ('FILENAME') containing the feature class name.

    :param workspace: The workspace containing feature classes.
    """
    try:
        arcpy.env.workspace = workspace
        arcpy.env.overwriteOutput = True

        fc_list = arcpy.ListFeatureClasses()
        if not fc_list:
            print("⚠️ No feature classes found in the workspace.")
            return

        for fc in fc_list:
            field_name = "FILENAME"
            if not arcpy.ListFields(fc, field_name):
                arcpy.AddField_management(fc, field_name, "TEXT")

            with arcpy.da.UpdateCursor(fc, [field_name]) as cursor:
                for row in cursor:
                    row[0] = fc
                    cursor.updateRow(row)

            print(f"✅ Added feature class name to {fc}")

    except Exception as e:
        print(f"❌ Error adding feature class name: {e}")


def simple_data_inventory(output_csv, folder):
    """
    Extracts GIS data inventory information (shapefiles, GDBs, layers) and saves to a CSV file.

    :param output_csv: The output CSV file path.
    :param folder: The root folder to scan.
    """
    try:
        with open(output_csv, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Name", "Path", "Type"])

            for root, _, files in os.walk(folder):
                for f in files:
                    full_path = os.path.join(root, f)

                    if f.endswith('.shp'):
                        desc = arcpy.Describe(full_path)
                        writer.writerow([desc.name, desc.catalogPath, "Shapefile"])

                    elif f.endswith('.gdb'):
                        desc = arcpy.Describe(root)
                        for child in desc.children:
                            writer.writerow([child.name, child.path, "Geodatabase Feature Class"])

                    elif f.endswith('.lyr'):
                        desc = arcpy.Describe(full_path)
                        writer.writerow([desc.name, desc.catalogPath, "Layer File"])

                    elif f.endswith('.img'):
                        desc = arcpy.Describe(full_path)
                        writer.writerow([desc.name, desc.catalogPath, "Raster Image"])

        print(f"✅ GIS data inventory saved to {output_csv}")

    except Exception as e:
        print(f"❌ Error generating data inventory: {e}")


def data_inventory(output_csv, workspace):
    """
    Extracts feature class metadata (name, path, type) from a workspace and saves to a CSV.

    :param output_csv: The output CSV file path.
    :param workspace: The workspace (folder or geodatabase).
    """
    try:
        with open(output_csv, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Catalog Path", "Name", "Data Type"])

            for dirpath, _, filenames in arcpy.da.Walk(workspace):
                for filename in filenames:
                    desc = arcpy.Describe(os.path.join(dirpath, filename))
                    writer.writerow([desc.catalogPath, desc.name, desc.dataType])

        print(f"✅ Feature class metadata saved to {output_csv}")

    except Exception as e:
        print(f"❌ Error extracting data inventory: {e}")
