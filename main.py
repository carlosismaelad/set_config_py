import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTabWidget
from tabs.pdv_tab import PDVTab
from tabs.integradoripos_tab import IntegradoriposTab
from tabs.webapi_tab import WebApiTab

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("SetConfig - By IzzyWay")
        self.setGeometry(600, 300, 800, 600)

        # Layout principal
        main_layout = QVBoxLayout()

        # Layout de botões
        button_layout = QHBoxLayout()

        # Botões superiores
        self.pdv_button = QPushButton("PDV SINCRONIZADOR")
        self.pdv_button.clicked.connect(self.show_pdv_tab)
        
        self.integradoripos_button = QPushButton("INTEGRADORIPOS")
        self.integradoripos_button.clicked.connect(self.show_integradoripos_tab)
        
        self.webapi_button = QPushButton("WEBAPI")
        self.webapi_button.clicked.connect(self.show_webapi_tab)

        # Adicionar botões ao layout
        button_layout.addWidget(self.pdv_button)
        button_layout.addWidget(self.integradoripos_button)
        button_layout.addWidget(self.webapi_button)
        
        main_layout.addLayout(button_layout)

        # TabControl (Widget com abas)
        self.tabs = QTabWidget()

        # Instanciar cada aba
        self.pdv_tab = PDVTab()
        self.integradoripos_tab = IntegradoriposTab()
        self.webapi_tab = WebApiTab()

        # Adicionar abas ao TabControl
        self.tabs.addTab(self.pdv_tab, "PDV")
        self.tabs.addTab(self.integradoripos_tab, "Integradoripos")
        self.tabs.addTab(self.webapi_tab, "WebAPI")

        main_layout.addWidget(self.tabs)
        self.setLayout(main_layout)

    def show_pdv_tab(self):
        self.tabs.setCurrentWidget(self.pdv_tab)

    def show_integradoripos_tab(self):
        self.tabs.setCurrentWidget(self.integradoripos_tab)

    def show_webapi_tab(self):
        self.tabs.setCurrentWidget(self.webapi_tab)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
