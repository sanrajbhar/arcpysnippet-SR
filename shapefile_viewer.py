import sys
import os
import geopandas as gpd
import matplotlib.pyplot as plt

from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog,
    QListWidget, QTableWidget, QTableWidgetItem, QLabel, QSplitter, QMenu, QMessageBox
)
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class ShapefileViewer(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Shapefile Browser & Visualizer")
        self.setGeometry(100, 100, 1200, 700)

        # Main Layout
        layout = QVBoxLayout()

        # Browse Button
        self.browse_button = QPushButton("Browse Folder")
        self.browse_button.clicked.connect(self.browse_folder)
        layout.addWidget(self.browse_button)

        # Folder Path Label
        self.folder_label = QLabel("Selected Folder: None")
        layout.addWidget(self.folder_label)

        # Splitter for Sidebar & Right Panel
        main_splitter = QSplitter(Qt.Horizontal)

        # Left Panel - Shapefile List
        left_panel = QWidget()
        left_layout = QVBoxLayout()

        self.list_widget = QListWidget()
        self.list_widget.itemClicked.connect(self.load_shapefile)
        self.list_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.list_widget.customContextMenuRequested.connect(self.show_context_menu)
        left_layout.addWidget(self.list_widget)

        left_panel.setLayout(left_layout)
        main_splitter.addWidget(left_panel)

        # Right Panel - Table & Map Splitter
        right_splitter = QSplitter(Qt.Vertical)

        # Attribute Table
        self.table_widget = QTableWidget()
        right_splitter.addWidget(self.table_widget)

        # Matplotlib Figure for Geometry Visualization
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        right_splitter.addWidget(self.canvas)

        # Info Section: Shapefile Details
        self.info_label = QLabel("Shapefile: None\nFeatures: 0\nCRS: Not Loaded")
        right_splitter.addWidget(self.info_label)

        main_splitter.addWidget(right_splitter)

        # Set Stretch Factors for Better Layout
        main_splitter.setStretchFactor(0, 1)  # Left Panel (Shapefile List)
        main_splitter.setStretchFactor(1, 3)  # Right Panel (Table + Map)
        right_splitter.setStretchFactor(0, 2)  # Table
        right_splitter.setStretchFactor(1, 4)  # Map
        right_splitter.setStretchFactor(2, 1)  # Info Panel

        layout.addWidget(main_splitter)
        self.setLayout(layout)

        self.shapefile_paths = {}  # Dictionary to store full shapefile paths

    def browse_folder(self):
        """Open file dialog to select a folder and list all shapefiles, including subfolders."""
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.folder_label.setText(f"Selected Folder: {folder}")
            self.list_shapefiles(folder)

    def list_shapefiles(self, folder):
        """Recursively find and list all shapefiles in the folder and subfolders."""
        self.list_widget.clear()
        self.shapefile_paths.clear()

        for root, _, files in os.walk(folder):  # Recursively scan directories
            for file in files:
                if file.endswith(".shp"):
                    full_path = os.path.join(root, file)
                    self.shapefile_paths[file] = full_path  # Store full path
                    self.list_widget.addItem(file)  # Show only shapefile name

    def load_shapefile(self, item):
        """Load shapefile and display attributes & geometry visualization."""
        shapefile_name = item.text()
        shapefile_path = self.shapefile_paths.get(shapefile_name)

        if shapefile_path:
            try:
                gdf = gpd.read_file(shapefile_path)
                self.display_table(gdf)
                self.plot_geometry(gdf)

                # Update Info Section
                crs_info = gdf.crs if gdf.crs else "Unknown"
                self.info_label.setText(f"Shapefile: {shapefile_name}\nFeatures: {len(gdf)}\nCRS: {crs_info}")

            except Exception as e:
                self.show_error_dialog(f"Error loading shapefile '{shapefile_name}': {e}")

    def display_table(self, gdf):
        """Display GeoDataFrame in QTableWidget."""
        self.table_widget.setRowCount(gdf.shape[0])
        self.table_widget.setColumnCount(gdf.shape[1])
        self.table_widget.setHorizontalHeaderLabels(gdf.columns)

        for row in range(gdf.shape[0]):
            for col in range(gdf.shape[1]):
                value = str(gdf.iat[row, col])
                self.table_widget.setItem(row, col, QTableWidgetItem(value))

    def plot_geometry(self, gdf):
        """Plot the shapefile's geometries using Matplotlib."""
        self.ax.clear()
        gdf.plot(ax=self.ax, edgecolor="black", facecolor="lightblue", markersize=10)
        self.ax.set_title("Shapefile Geometry")
        self.ax.set_xlabel("Longitude")
        self.ax.set_ylabel("Latitude")
        self.canvas.draw()

    def show_context_menu(self, position):
        """Show right-click menu to copy shapefile path."""
        menu = QMenu()
        copy_action = menu.addAction("Copy Path")

        action = menu.exec_(self.list_widget.mapToGlobal(position))
        if action == copy_action:
            selected_item = self.list_widget.currentItem()
            if selected_item:
                shapefile_name = selected_item.text()
                shapefile_path = self.shapefile_paths.get(shapefile_name)
                if shapefile_path:
                    QApplication.clipboard().setText(shapefile_path)
                    print(f"Copied to clipboard: {shapefile_path}")

    def show_error_dialog(self, message):
        """Display an error pop-up dialog."""
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setText("Shapefile Load Error")
        msg_box.setInformativeText(message)
        msg_box.setWindowTitle("Error")
        msg_box.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = ShapefileViewer()
    viewer.show()
    sys.exit(app.exec_())
