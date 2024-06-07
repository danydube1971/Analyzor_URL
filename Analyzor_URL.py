import sys
import os
import requests
import urllib3
from bs4 import BeautifulSoup
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QPushButton, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QProgressBar, QHeaderView, QLabel
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QColor, QDesktopServices
from PyQt5.QtCore import QUrl

# Désactiver les avertissements InsecureRequestWarning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class LinkCheckerThread(QThread):
    progress_update = pyqtSignal(int)
    link_checked = pyqtSignal(str, str, bool)
    analysis_done = pyqtSignal()

    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path
        self.stop_requested = False
        self.problematic_domains = ["mediaradio.ca"]  # Liste des domaines à ignorer

    def run(self):
        session = requests.Session()
        session.max_redirects = 5
        with open(self.file_path, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file, 'html.parser')
            links = soup.find_all('a', href=True)
        
        total_links = len(links)
        for i, link in enumerate(links):
            if self.stop_requested:
                break

            url = link.get('href')
            description = link.text.strip() if link.text.strip() else "No Description"

            if any(domain in url for domain in self.problematic_domains):
                print(f"Ignoring problematic domain: {url}")
                continue

            is_valid = self.check_link(session, url)
            self.link_checked.emit(description, url, is_valid)
            self.progress_update.emit((i + 1) * 100 // total_links)
        
        self.analysis_done.emit()
    
    def check_link(self, session, url):
        try:
            response = session.head(url, timeout=5, allow_redirects=True, verify=False)
            return response.status_code == 200
        except requests.RequestException as e:
            print(f"Error checking {url}: {e}")
            return False

    def stop(self):
        self.stop_requested = True

class LinkChecker(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Vérificateur de liens HTML")
        self.setGeometry(300, 100, 800, 600)
        
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        
        self.layout = QVBoxLayout()
        self.main_widget.setLayout(self.layout)
        
        self.load_button = QPushButton("Charger un fichier HTML")
        self.load_button.clicked.connect(self.load_html_file)
        self.layout.addWidget(self.load_button)
        
        self.link_count_label = QLabel("Nombre de liens à analyser : 0")
        self.layout.addWidget(self.link_count_label)
        
        self.stop_button = QPushButton("Stop")
        self.stop_button.setEnabled(False)
        self.stop_button.clicked.connect(self.stop_analysis)
        self.layout.addWidget(self.stop_button)
        
        self.progress_bar = QProgressBar()
        self.layout.addWidget(self.progress_bar)
        
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(2)
        self.table_widget.setHorizontalHeaderLabels(["Description", "URL"])
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_widget.cellDoubleClicked.connect(self.open_link)
        self.layout.addWidget(self.table_widget)
        
        self.analysis_thread = None
        
    def load_html_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Sélectionner un fichier HTML", "", "HTML Files (*.html *.htm)")
        if file_path:
            self.table_widget.setRowCount(0)
            self.progress_bar.setValue(0)
            self.stop_button.setEnabled(True)
            self.analysis_thread = LinkCheckerThread(file_path)
            self.analysis_thread.progress_update.connect(self.update_progress)
            self.analysis_thread.link_checked.connect(self.display_link)
            self.analysis_thread.analysis_done.connect(self.analysis_complete)
            
            # Lire le fichier HTML et compter les liens
            with open(file_path, 'r', encoding='utf-8') as file:
                soup = BeautifulSoup(file, 'html.parser')
                links = soup.find_all('a', href=True)
                total_links = len(links)
            
            self.link_count_label.setText(f"Nombre de liens à analyser : {total_links}")
            self.analysis_thread.start()
    
    def stop_analysis(self):
        if self.analysis_thread:
            self.analysis_thread.stop()
            self.stop_button.setEnabled(False)
    
    def update_progress(self, value):
        self.progress_bar.setValue(value)
    
    def display_link(self, description, url, is_valid):
        row_position = self.table_widget.rowCount()
        self.table_widget.insertRow(row_position)
        if is_valid:
            description_item = QTableWidgetItem(description)
            link_item = QTableWidgetItem(url)
            link_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            link_item.setToolTip(url)
            link_item.setData(Qt.UserRole, QUrl(url))  # Store the URL for use on double click
        else:
            description_item = QTableWidgetItem(f"LIEN CASSÉ : {description}")
            link_item = QTableWidgetItem(url)
            link_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            link_item.setToolTip(url)
            link_item.setData(Qt.UserRole, QUrl(url))  # Store the URL for use on double click
            
            # Set background color to light red for broken links
            background_color = QColor(255, 182, 193)  # Light red color
            description_item.setBackground(background_color)
            link_item.setBackground(background_color)
        
        self.table_widget.setItem(row_position, 0, description_item)
        self.table_widget.setItem(row_position, 1, link_item)

    def open_link(self, row, column):
        if column == 1:
            url = self.table_widget.item(row, column).data(Qt.UserRole)
            if url:
                QDesktopServices.openUrl(url)

    def analysis_complete(self):
        self.stop_button.setEnabled(False)
        print("Analyse terminée.")
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = LinkChecker()
    mainWin.show()
    sys.exit(app.exec_())

