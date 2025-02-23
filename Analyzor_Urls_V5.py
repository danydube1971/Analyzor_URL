import sys
import requests
import urllib3
from bs4 import BeautifulSoup
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QFileDialog, QPushButton,
    QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget,
    QProgressBar, QHeaderView, QLabel, QMessageBox, QCheckBox, QLineEdit
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QColor, QDesktopServices
from PyQt5.QtCore import QUrl
import concurrent.futures
import logging
from urllib.parse import urljoin, urlparse
import threading
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Désactiver les avertissements InsecureRequestWarning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class LinkChecker:
    def __init__(self, problematic_domains=None, max_workers=10, verify_ssl=False, stop_event=None):
        self.problematic_domains = problematic_domains or []
        self.max_workers = max_workers
        self.session = requests.Session()
        self.session.max_redirects = 5
        self.verify_ssl = verify_ssl
        self.stop_event = stop_event

    def validate_and_resolve_url(self, url, base_url=None):
        if self.stop_event and self.stop_event.is_set():
            return None
        parsed = urlparse(url)
        if not parsed.scheme:
            if base_url:
                resolved_url = urljoin(base_url, url)
                if self.is_valid_url(resolved_url):
                    return resolved_url
                else:
                    logging.warning(f"URL invalidée après résolution : {resolved_url}")
                    return None
            else:
                logging.warning(f"URL relative ignorée sans base URL : {url}")
                return None
        if self.is_valid_url(url):
            return url
        logging.warning(f"URL invalide : {url}")
        return None

    def is_valid_url(self, url):
        parsed = urlparse(url)
        return all([parsed.scheme, parsed.netloc])

    def check_link(self, url):
        if self.stop_event and self.stop_event.is_set():
            return False, None, None
        try:
            response = self.session.head(url, timeout=10, allow_redirects=True, verify=self.verify_ssl)
            if self.stop_event and self.stop_event.is_set():
                return False, None, None
            redirect_chain = [r.url for r in response.history] + [response.url] if response.history else [url]
            if (200 <= response.status_code < 400) or response.status_code == 403:
                return True, response.status_code, redirect_chain
            else:
                logging.info(f"HEAD request returned status {response.status_code} for URL: {url}")
                response = self.session.get(url, timeout=10, allow_redirects=True, verify=self.verify_ssl)
                if self.stop_event and self.stop_event.is_set():
                    return False, None, None
                redirect_chain = [r.url for r in response.history] + [response.url] if response.history else [url]
                if (200 <= response.status_code < 400) or response.status_code == 403:
                    return True, response.status_code, redirect_chain
                else:
                    logging.info(f"GET request returned status {response.status_code} for URL: {url}")
                    return False, response.status_code, redirect_chain
        except requests.RequestException as e:
            logging.warning(f"HEAD request failed for {url}: {e}")
            try:
                response = self.session.get(url, timeout=10, allow_redirects=True, verify=self.verify_ssl)
                if self.stop_event and self.stop_event.is_set():
                    return False, None, None
                redirect_chain = [r.url for r in response.history] + [response.url] if response.history else [url]
                if (200 <= response.status_code < 400) or response.status_code == 403:
                    return True, response.status_code, redirect_chain
                else:
                    logging.info(f"GET request returned status {response.status_code} for URL: {url}")
                    return False, response.status_code, redirect_chain
            except requests.RequestException as e_get:
                logging.error(f"GET request failed for {url}: {e_get}")
                return False, None, [url]

    def run_checks(self, links, base_url=None, progress_callback=None, result_callback=None):
        total_links = len(links)
        logging.info(f"Total de liens à analyser : {total_links}")

        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_link = {}
            for i, link in enumerate(links):
                if self.stop_event and self.stop_event.is_set():
                    logging.info("Analyse interrompue par l'utilisateur lors de la soumission des tâches.")
                    break

                url = link.get('href').strip()
                description = link.text.strip() if link.text.strip() else "No Description"

                if any(domain in url for domain in self.problematic_domains):
                    logging.info(f"Ignorant le domaine problématique : {url}")
                    if progress_callback:
                        progress_callback((i + 1) * 100 // total_links)
                    continue

                if not url:
                    logging.warning(f"URL vide trouvée pour la description : {description}")
                    if result_callback:
                        result_callback(description, "URL manquante", False, None, None)
                    if progress_callback:
                        progress_callback((i + 1) * 100 // total_links)
                    continue

                resolved_url = self.validate_and_resolve_url(url, base_url)
                if not resolved_url:
                    if result_callback:
                        result_callback(description, "URL invalide", False, None, None)
                    if progress_callback:
                        progress_callback((i + 1) * 100 // total_links)
                    continue

                future = executor.submit(self.check_link, resolved_url)
                future_to_link[future] = (description, resolved_url)

            processed = 0
            for future in concurrent.futures.as_completed(future_to_link):
                if self.stop_event and self.stop_event.is_set():
                    logging.info("Analyse interrompue par l'utilisateur lors du traitement des résultats.")
                    break
                description, url = future_to_link[future]
                try:
                    is_valid, status_code, redirect_chain = future.result()
                except Exception as exc:
                    logging.error(f"Erreur lors de la vérification du lien {url} : {exc}")
                    is_valid, status_code, redirect_chain = False, None, [url]
                if not self.stop_event.is_set():
                    if result_callback:
                        result_callback(description, url, is_valid, status_code, redirect_chain)
                    processed += 1
                    if progress_callback:
                        progress_callback(min(processed * 100 // total_links, 100))
                else:
                    logging.info("Arrêt de l'analyse. Ignorer les résultats restants.")
                    break

class LinkCheckerThread(QThread):
    progress_update = pyqtSignal(int)
    link_checked = pyqtSignal(str, str, bool, int, list)
    analysis_done = pyqtSignal()

    def __init__(self, file_path, problematic_domains=None, verify_ssl=False):
        super().__init__()
        self.file_path = file_path
        self.problematic_domains = problematic_domains or []
        self.verify_ssl = verify_ssl
        self.stop_event = threading.Event()

    def run(self):
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                soup = BeautifulSoup(file, 'html.parser')
                links = soup.find_all('a', href=True)
        except Exception as e:
            logging.error(f"Erreur lors de la lecture du fichier HTML : {e}")
            self.analysis_done.emit()
            return

        link_checker = LinkChecker(
            problematic_domains=self.problematic_domains,
            verify_ssl=self.verify_ssl,
            stop_event=self.stop_event
        )

        link_checker.run_checks(
            links=links,
            base_url=None,
            progress_callback=self.progress_update.emit,
            result_callback=lambda desc, url, valid, status, chain: self.link_checked.emit(desc, url, valid, status, chain)
        )

        self.analysis_done.emit()

    def stop(self):
        self.stop_event.set()

class LinkCheckerGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Vérificateur de liens HTML")
        self.setGeometry(300, 100, 1000, 700)

        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)

        self.layout = QVBoxLayout()
        self.main_widget.setLayout(self.layout)

        self.load_button = QPushButton("Charger un fichier HTML")
        self.load_button.clicked.connect(self.load_html_file)
        self.layout.addWidget(self.load_button)

        self.export_button = QPushButton("Exporter en CSV")
        self.export_button.clicked.connect(self.export_results)
        self.export_button.setEnabled(False)
        self.layout.addWidget(self.export_button)

        self.export_html_button = QPushButton("Exporter en HTML")
        self.export_html_button.clicked.connect(self.export_to_html)
        self.export_html_button.setEnabled(False)
        self.layout.addWidget(self.export_html_button)

        self.link_count_label = QLabel("Nombre de liens à analyser : 0")
        self.layout.addWidget(self.link_count_label)

        self.broken_links_label = QLabel("Nombre de liens cassés : 0")
        self.layout.addWidget(self.broken_links_label)

        self.show_only_broken_checkbox = QCheckBox("Afficher seulement les liens cassés")
        self.show_only_broken_checkbox.setChecked(False)
        self.show_only_broken_checkbox.stateChanged.connect(self.filter_broken_links)
        self.layout.addWidget(self.show_only_broken_checkbox)

        self.ssl_checkbox = QCheckBox("Vérifier les certificats SSL")
        self.ssl_checkbox.setChecked(True)
        self.layout.addWidget(self.ssl_checkbox)

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Rechercher...")
        self.search_bar.textChanged.connect(self.filter_links)
        self.layout.addWidget(self.search_bar)

        self.stop_button = QPushButton("Stop")
        self.stop_button.setEnabled(False)
        self.stop_button.clicked.connect(self.stop_analysis)
        self.layout.addWidget(self.stop_button)

        self.progress_bar = QProgressBar()
        self.layout.addWidget(self.progress_bar)

        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(4)
        self.table_widget.setHorizontalHeaderLabels(["Description", "URL", "Statut", "Redirections"])
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_widget.cellDoubleClicked.connect(self.open_link)
        self.layout.addWidget(self.table_widget)

        self.analysis_thread = None
        self.broken_links_count = 0

        self.table_widget.setSortingEnabled(True)
        self.table_widget.horizontalHeader().sectionClicked.connect(self.handle_header_clicked)
        self.sort_order = Qt.AscendingOrder
        self.sort_column = -1

    def load_html_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Sélectionner un fichier HTML",
            "",
            "HTML Files (*.html *.htm)"
        )
        if file_path:
            self.table_widget.setRowCount(0)
            self.progress_bar.setValue(0)
            self.export_button.setEnabled(False)
            self.export_html_button.setEnabled(False)
            self.stop_button.setEnabled(True)

            self.broken_links_count = 0
            self.broken_links_label.setText("Nombre de liens cassés : 0")

            if self.show_only_broken_checkbox.isChecked():
                self.show_only_broken_checkbox.setChecked(False)

            verify_ssl = self.ssl_checkbox.isChecked()
            self.analysis_thread = LinkCheckerThread(
                file_path,
                verify_ssl=verify_ssl
            )
            self.analysis_thread.progress_update.connect(self.update_progress)
            self.analysis_thread.link_checked.connect(self.display_link)
            self.analysis_thread.analysis_done.connect(self.analysis_complete)
            self.analysis_thread.start()

            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    soup = BeautifulSoup(file, 'html.parser')
                    links = soup.find_all('a', href=True)
                    total_links = len(links)
                self.link_count_label.setText(f"Nombre de liens à analyser : {total_links}")
            except Exception as e:
                logging.error(f"Erreur lors de la lecture du fichier HTML : {e}")
                self.link_count_label.setText("Nombre de liens à analyser : 0")

    def stop_analysis(self):
        if self.analysis_thread:
            self.analysis_thread.stop()
            self.stop_button.setEnabled(False)
            QMessageBox.information(self, "Stop", "Analyse interrompue.")

    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def display_link(self, description, url, is_valid, status_code, redirect_chain):
        if self.analysis_thread and self.analysis_thread.stop_event.is_set():
            return

        row_position = self.table_widget.rowCount()
        self.table_widget.insertRow(row_position)

        description_item = QTableWidgetItem(description)
        if not is_valid and status_code != 403:
            description_item.setText(f"LIEN CASSÉ : {description}")
            description_item.setBackground(QColor(255, 182, 193))
        self.table_widget.setItem(row_position, 0, description_item)

        link_item = QTableWidgetItem(url if url else "URL manquante")
        link_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        link_item.setToolTip(url if url else "URL manquante")
        link_item.setData(Qt.UserRole, url if url else "")
        if url in ["URL manquante", "URL invalide"]:
            link_item.setBackground(QColor(255, 182, 193))
        self.table_widget.setItem(row_position, 1, link_item)

        status_text = f"{status_code} - {'Valide' if is_valid else 'Cassé'}" if status_code else "Cassé"
        if status_code == 403:
            status_text = f"{status_code} - Valide (403)"
        status_item = QTableWidgetItem(status_text)
        if not is_valid and status_code != 403:
            status_item.setForeground(QColor(255, 0, 0))
        self.table_widget.setItem(row_position, 2, status_item)

        redirect_text = "Aucune" if len(redirect_chain) == 1 else " -> ".join(redirect_chain)
        redirect_item = QTableWidgetItem(redirect_text)
        redirect_item.setToolTip(redirect_text)
        if len(redirect_chain) > 1:
            redirect_item.setForeground(QColor(0, 0, 255))
        self.table_widget.setItem(row_position, 3, redirect_item)

        if not is_valid and status_code != 403:
            self.broken_links_count += 1
            self.broken_links_label.setText(f"Nombre de liens cassés : {self.broken_links_count}")

        self.export_button.setEnabled(True)
        self.export_html_button.setEnabled(True)

        if self.show_only_broken_checkbox.isChecked():
            self.table_widget.setRowHidden(row_position, is_valid or status_code == 403)

    def open_link(self, row, column):
        if column == 1:
            item = self.table_widget.item(row, column)
            if item:
                url = item.data(Qt.UserRole)
                if url and isinstance(url, str) and url.startswith(('http://', 'https://')):
                    QDesktopServices.openUrl(QUrl(url))
                else:
                    QMessageBox.warning(self, "URL Invalide", f"URL invalide ou manquante pour la ligne {row + 1}")
            else:
                QMessageBox.warning(self, "Erreur", f"Aucune URL trouvée pour la ligne {row + 1}")

    def analysis_complete(self):
        self.stop_button.setEnabled(False)
        QMessageBox.information(self, "Terminé", "Analyse terminée.")

    def handle_header_clicked(self, logicalIndex):
        if self.sort_column == logicalIndex:
            self.sort_order = Qt.DescendingOrder if self.sort_order == Qt.AscendingOrder else Qt.AscendingOrder
        else:
            self.sort_order = Qt.AscendingOrder
            self.sort_column = logicalIndex
        self.table_widget.sortItems(logicalIndex, self.sort_order)

    def filter_links(self, text):
        for row in range(self.table_widget.rowCount()):
            match = False
            for column in range(self.table_widget.columnCount()):
                item = self.table_widget.item(row, column)
                if text.lower() in item.text().lower():
                    match = True
                    break
            if self.show_only_broken_checkbox.isChecked():
                status_item = self.table_widget.item(row, 2)
                if status_item:
                    status_text = status_item.text()
                    is_broken = "Cassé" in status_text and "403" not in status_text
                    match = match and is_broken
            self.table_widget.setRowHidden(row, not match)

    def filter_broken_links(self):
        show_only_broken = self.show_only_broken_checkbox.isChecked()
        for row in range(self.table_widget.rowCount()):
            status_item = self.table_widget.item(row, 2)
            if status_item:
                status_text = status_item.text()
                is_broken = "Cassé" in status_text and "403" not in status_text
                if show_only_broken:
                    self.table_widget.setRowHidden(row, not is_broken)
                else:
                    self.table_widget.setRowHidden(row, False)

    def export_results(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Exporter les résultats en .csv",
            "",
            "CSV Files (*.csv)"
        )
        if file_path:
            if not file_path.lower().endswith('.csv'):
                file_path += '.csv'
            try:
                with open(file_path, 'w', encoding='utf-8-sig') as f:
                    headers = ["Description", "URL", "Statut", "Redirections"]
                    f.write(','.join(headers) + '\n')
                    for row in range(self.table_widget.rowCount()):
                        if self.show_only_broken_checkbox.isChecked() and self.table_widget.isRowHidden(row):
                            continue
                        description = self.table_widget.item(row, 0).text()
                        url = self.table_widget.item(row, 1).text()
                        status = self.table_widget.item(row, 2).text()
                        redirect = self.table_widget.item(row, 3).text()
                        description = description.replace('"', '""')
                        url = url.replace('"', '""')
                        status = status.replace('"', '""')
                        redirect = redirect.replace('"', '""')
                        f.write(f'"{description}","{url}","{status}","{redirect}"\n')
                QMessageBox.information(self, "Exporté", f"Résultats exportés avec succès vers {file_path}")
            except Exception as e:
                logging.error(f"Erreur lors de l'exportation des résultats : {e}")
                QMessageBox.critical(self, "Erreur", f"Erreur lors de l'exportation des résultats : {e}")

    def export_to_html(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Exporter les résultats en .html",
            "",
            "HTML Files (*.html)"
        )
        if file_path:
            if not file_path.lower().endswith('.html'):
                file_path += '.html'
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    html_content = """
                    <!DOCTYPE html>
                    <html lang="fr">
                    <head>
                        <meta charset="UTF-8">
                        <title>Résultats de l'analyse des liens</title>
                        <style>
                            table {
                                width: 100%;
                                border-collapse: collapse;
                            }
                            th, td {
                                border: 1px solid black;
                                padding: 8px;
                                text-align: left;
                            }
                            th {
                                background-color: #f2f2f2;
                            }
                            .broken {
                                color: red;
                            }
                            .redirect {
                                color: blue;
                            }
                        </style>
                    </head>
                    <body>
                        <h1>Résultats de l'analyse des liens</h1>
                        <table>
                            <tr>
                                <th>Description</th>
                                <th>URL</th>
                                <th>Statut</th>
                                <th>Redirections</th>
                            </tr>
                    """
                    for row in range(self.table_widget.rowCount()):
                        if self.show_only_broken_checkbox.isChecked() and self.table_widget.isRowHidden(row):
                            continue
                        description = self.table_widget.item(row, 0).text()
                        url = self.table_widget.item(row, 1).text()
                        status = self.table_widget.item(row, 2).text()
                        redirect = self.table_widget.item(row, 3).text()
                        description = description.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                        url_text = url.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                        status = status.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                        redirect = redirect.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                        if url.startswith(('http://', 'https://')):
                            url_display = f'<a href="{url}">{url_text}</a>'
                        else:
                            url_display = url_text
                        status_class = ' class="broken"' if "Cassé" in status and "403" not in status else ''
                        redirect_class = ' class="redirect"' if redirect != "Aucune" else ''
                        html_content += f"""
                            <tr>
                                <td>{description}</td>
                                <td>{url_display}</td>
                                <td{status_class}>{status}</td>
                                <td{redirect_class}>{redirect}</td>
                            </tr>
                        """
                    html_content += """
                        </table>
                    </body>
                    </html>
                    """
                    f.write(html_content)
                QMessageBox.information(self, "Exporté", f"Résultats exportés avec succès vers {file_path}")
            except Exception as e:
                logging.error(f"Erreur lors de l'exportation en HTML : {e}")
                QMessageBox.critical(self, "Erreur", f"Erreur lors de l'exportation en HTML : {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = LinkCheckerGUI()
    mainWin.show()
    sys.exit(app.exec_())
