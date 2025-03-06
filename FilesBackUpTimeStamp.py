import sys
import time
import shutil
import os
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QListWidget, QPushButton, QVBoxLayout, QMessageBox, QFileDialog
from PyQt5.QtGui import QColor

class BackupApp(QWidget):
    def __init__(self):
        super().__init__()
        self.files = []
        self.outpath = 'C:/backup'  # Default backup destination
        self.initUI()
    
    def initUI(self):
        layout = QVBoxLayout()
        
        self.lbl = QLabel("Choose folder to backup files from:")
        self.btnSelectFolder = QPushButton("Select Folder")
        self.btnSelectFolder.clicked.connect(self.select_folder)
        
        self.lst = QListWidget()
        self.lst.setSelectionMode(QListWidget.MultiSelection)
        
        self.btnBck = QPushButton("Backup Selected")
        self.btnBck.clicked.connect(self.Backup_sel)
        
        self.btnBckAll = QPushButton("Backup All")
        self.btnBckAll.clicked.connect(self.Backup_all)
        
        self.lblStatus = QLabel("")
        
        layout.addWidget(self.lbl)
        layout.addWidget(self.btnSelectFolder)
        layout.addWidget(self.lst)
        layout.addWidget(self.btnBck)
        layout.addWidget(self.btnBckAll)
        layout.addWidget(self.lblStatus)
        
        self.setLayout(layout)
        self.setWindowTitle("Quick Backup")
        self.setGeometry(100, 100, 400, 400)
    
    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder to Backup")
        if folder:
            try:
                self.files = [os.path.join(folder, f) for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
                self.lst.clear()
                for file in self.files:
                    item = self.lst.addItem(os.path.basename(file))
                    self.set_item_color(file, item)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"An error occurred while selecting the folder: {str(e)}")
    
    def set_item_color(self, file, item):
        ext = file.split('.')[-1].lower()
        colors = {
            'txt': QColor("blue"),
            'pdf': QColor("red"),
            'doc': QColor("green"),
            'docx': QColor("green"),
            'csv': QColor("orange"),
            'xlsx': QColor("purple"),
            'png': QColor("cyan"),
            'jpg': QColor("magenta"),
            'jpeg': QColor("magenta"),
            'mp4': QColor("brown"),
        }
        
        if ext in colors:
            self.lst.item(self.lst.count() - 1).setForeground(colors[ext])
    
    def Backup_sel(self):
        if not self.files:
            QMessageBox.warning(self, "Warning", "No files selected for backup.")
            return
        
        if not os.path.exists(self.outpath):
            os.makedirs(self.outpath)
        
        selected_items = self.lst.selectedItems()
        t = time.strftime('%Y%m%d%H%M')
        
        try:
            for item in selected_items:
                filename = item.text()
                full_path = next(path for path in self.files if path.endswith(filename))
                backup_name = filename.rsplit('.', 1)[0] + '_' + t + '.' + filename.rsplit('.', 1)[1]
                shutil.copy(full_path, os.path.join(self.outpath, backup_name))
            
            self.lblStatus.setText("Backup Completed.")
            QMessageBox.information(self, "Backup", "Selected files have been backed up successfully.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred during backup: {str(e)}")
    
    def Backup_all(self):
        if not self.files:
            QMessageBox.warning(self, "Warning", "No files available for backup.")
            return
        
        if not os.path.exists(self.outpath):
            os.makedirs(self.outpath)
        
        t = time.strftime('%Y%m%d%H%M')
        
        try:
            for file in self.files:
                filename = os.path.basename(file)
                backup_name = filename.rsplit('.', 1)[0] + '_' + t + '.' + filename.rsplit('.', 1)[1]
                shutil.copy2(file, os.path.join(self.outpath, backup_name))
            
            self.lblStatus.setText("Backup Completed.")
            QMessageBox.information(self, "Backup", "All files have been backed up successfully.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred during backup: {str(e)}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = BackupApp()
    ex.show()
    sys.exit(app.exec_())
