# Import Libraries
import os
import sys
sys.path.append(os.path.dirname(__file__))  # Append the current file path to system path
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QFileDialog, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5.uic import loadUiType

FormClass, _ = loadUiType(os.path.join(os.path.dirname(__file__), 'dashboard.ui'))

# Apply QSS file for styling
def apply_stylesheet(app, qss_file):
    if os.path.exists(qss_file):
        with open(qss_file, "r") as file:
            app.setStyleSheet(file.read())

from Pneumonia import predictPneumonia

# Dashboard Class
class Dashboard(QMainWindow, FormClass):
    def __init__(self, role):
        super().__init__()
        self.setupUi(self)
        self.role = role
        self.disease = None
        self.disease_image = None

        # Dashboard Buttons
        self.stackedWidget.setCurrentIndex(0)
        self.dashboard_btn.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.patient_btn.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        self.disease_detection_btn.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(2))
        self.report_btn.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(3))
        self.chatbot_btn.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(5))
        self.logout_btn.clicked.connect(self.logout)

        # Permissions configuration based on role
        self.configure_permissions()

        # Disease Detection Tab
        self.uploadImage.clicked.connect(self.upload_image)
        self.analyzeImage.clicked.connect(lambda: self.analyze_image(self.file_path))
        self.createReportPage.clicked.connect(lambda: self.create_report_dd(self.disease, self.disease_image))

        # Show the window
        self.show()

    # Permissions Configuration
    def configure_permissions(self):
        if self.role == "Assistant":
            self.disease_detection_btn.hide()
            self.chatbot_btn.hide()

        if self.role == "Doctor" and hasattr(self, "patients"):
            self.patients.removeTab(1)

    # Logout Function
    def logout(self):
        self.close()
        from main import MainApp
        self.login_window = MainApp()
        self.login_window.show()

    # Disease Detection Tab
    def upload_image(self):
        if self.stackedWidget.currentIndex() == 2: 
            file_path, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Image Files (*.png *.jpg *.jpeg *.bmp)")
            if file_path:
                print(f"Selected file: {file_path}")
                pixmap = QPixmap(file_path)
                self.image.setPixmap(pixmap)
                self.image.setScaledContents(True)
                self.image.show()
                self.file_path = file_path  # Store the file path
                self.analyzeImage.clicked.connect(lambda: self.detection.setCurrentIndex(3))  # Switch to the next tab
            else:
                print("No file selected")
        else:
            QMessageBox.warning(self, "Input Error", "Please navigate to Disease Detection tab to upload an image")

    def analyze_image(self, file_path):
        if self.image.pixmap() is None:
            QMessageBox.warning(self, "Input Error", "Please upload an image first")
        else:
            path = file_path
            self.disease_image = self.image.pixmap().toImage()
            pixmap = QPixmap(self.disease_image)
            self.image_2.setPixmap(pixmap)
            self.image_2.setScaledContents(True)
            self.image_2.show()
            self.disease = predictPneumonia(path)
            self.diseaseName.setText(self.disease)
            self.createReportPage.clicked.connect(lambda: self.detection.setCurrentIndex(4))  # Switch to the next tab

    def create_report_dd(self, disease_name, upload_image):
        self.diseaseName_2.setText(disease_name)
        pixmap = QPixmap(upload_image)  # Convert QImage to QPixmap
        pixmap = pixmap.scaled(self.image_3.size())  # Resize the image to fit the QLabel
        self.image_3.setPixmap(pixmap)
        self.image_3.setScaledContents(True)

        # Link with database and save the report


    # Patients Tab
    def show_all_patients(self):
        pass
    def add_patient(self):
        pass
    def edit_patient(self):
        pass
    def delete_patient(self):
        pass
    def show_patient(self):
        pass
    
    # Reports Tab
    def show_all_reports(self):
        pass
    def show_report(self):
        pass


# Main Function
if __name__ == "__main__":
    app = QApplication(sys.argv)

    qss_file_path = os.path.join(os.path.dirname(__file__), 'app_style.qss')
    apply_stylesheet(app, qss_file_path)

    window = Dashboard("Doctor")
    window.show()
    sys.exit(app.exec_())