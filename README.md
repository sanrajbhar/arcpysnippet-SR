
# arcpysnippet-SR
please check Util folder that contain classes and function to re-use the code in your main script file. I upload list of functions.
## SR_ArcpyDefinedFunc.py - GIS Helper Functions using ArcPy

This script provides utility functions for working with Geographic Information System (GIS) data using ArcPy. It allows users to list and process feature classes (FCs) in a workspace (folder or geodatabase), extract metadata, and update feature class attributes.

## Prerequisites
- **ArcPy** (Requires ArcGIS Pro or ArcMap with an installed Python environment)
- **Python 3.x** (compatible with ArcGIS Pro)
- **Access to GIS data** (shapefiles, geodatabases, feature classes, etc.)

## Installation
Ensure that ArcGIS Pro or ArcMap is installed with ArcPy available. The script can be run in the Python environment that comes with ArcGIS.

## Functions

Add this at start of your script

`import arcpy`
`from Utils.SR_ArcpyDefinedFunc import *`

### 1. `list_fcs_in_folder(workspace)`
**Description:** Recursively lists all shapefiles and feature classes in a folder and its subdirectories.
- **Parameters:** `workspace` (str) - The root folder path containing GIS data.
- **Returns:** List of full paths to all feature classes found.
- `import arcpy`
`from Utils.SR_ArcpyDefinedFunc import *`

**Example Usage**
`workspace = "C:/GIS/Data"`

**List feature classes**
`print(list_fcs_in_folder(workspace))`

### 2. `list_fcs_in_gdb(gdb_path)`
**Description:** Lists all feature classes in a Geodatabase (GDB), including those inside feature datasets.
- **Parameters:** `gdb_path` (str) - Path to the geodatabase.
- **Returns:** List of feature class names inside the GDB.

### 3. `add_folder_name_as_field(workspace)`
**Description:** Adds a field (`Folder`) to each feature class, storing the name of its parent folder.
- **Parameters:** `workspace` (str) - The folder containing feature classes.

### 4. `add_fc_name_as_field(workspace)`
**Description:** Adds a field (`FILENAME`) to each feature class, storing its own name.
- **Parameters:** `workspace` (str) - The workspace containing feature classes.

### 5. `simple_data_inventory(output_csv, folder)`
**Description:** Extracts GIS data inventory information (shapefiles, GDBs, layers) and saves it to a CSV file.
- **Parameters:**
  - `output_csv` (str) - Path to the output CSV file.
  - `folder` (str) - The root folder to scan.

### 6. `data_inventory(output_csv, workspace)`
**Description:** Extracts metadata from feature classes in a workspace and saves it to a CSV file.
- **Parameters:**
  - `output_csv` (str) - Path to the output CSV file.
  - `workspace` (str) - The workspace (folder or geodatabase).

## Usage

```python
import arcpy
from Utils.SR_ArcpyDefinedFunc import *

# Example Usage
workspace = "C:/GIS/Data"
gdb_path = "C:/GIS/Data/MyGeodatabase.gdb"
output_csv = "C:/GIS/Inventory.csv"

# List feature classes
print(list_fcs_in_folder(workspace))
print(list_fcs_in_gdb(gdb_path))

# Add fields
add_folder_name_as_field(workspace)
add_fc_name_as_field(gdb_path)

# Generate inventory
simple_data_inventory(output_csv, workspace)
data_inventory(output_csv, workspace)
```

## Error Handling
The script includes exception handling to catch errors and display messages if issues arise while processing data.

## License
This script is free to use and modify for GIS-related tasks. Ensure compliance with any organizational policies regarding GIS data processing.

## Author
Sanjaykumar Rajbhar  
sanrajbhar@gmail.com 
04-March-2025




## shapefile viewer
![alt text](https://github.com/sanrajbhar/arcpysnippet-testing/blob/main/img_shapefileViewer.png)
