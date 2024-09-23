import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTabWidget, QLineEdit
from tabs.pdv_tab import PDVTab
from tabs.sincronizador_tab import SincronizadorTab
from tabs.integradoripos_tab import IntegradoriposTab
from tabs.webapi_tab import WebApiTab
from utils.xml_hundler import XmlHundler

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("SetConfig - By IzzyWay")
        self.setGeometry(600, 300, 800, 600)

        self.xml_hundler = XmlHundler()

        # Layout principal
        main_layout = QVBoxLayout()

        # Definição dos inputs
        self.instance_input = QLineEdit()
        self.database_input = QLineEdit()
        self.user_input = QLineEdit()
        self.password_input = QLineEdit()
        self.empresa_input = QLineEdit()  # Apenas para PDV
        self.cnpj_input = QLineEdit()      # Apenas para PDV

        # Layout de botões
        button_layout = QHBoxLayout()

        # Criação dos botões superiores
        self.pdv_button = QPushButton("PDV")
        self.pdv_button.clicked.connect(self.show_pdv_tab)

        self.sincronizador_button = QPushButton("SINCRONIZADOR")
        self.sincronizador_button.clicked.connect(self.show_sincronizador_tab)
        
        self.integradoripos_button = QPushButton("INTEGRADORIPOS")
        self.integradoripos_button.clicked.connect(self.show_integradoripos_tab)
        
        self.webapi_button = QPushButton("WEBAPI")
        self.webapi_button.clicked.connect(self.show_webapi_tab)

        # Adicionar botões ao layout
        button_layout.addWidget(self.pdv_button)
        button_layout.addWidget(self.sincronizador_button)
        button_layout.addWidget(self.integradoripos_button)
        button_layout.addWidget(self.webapi_button)        
        main_layout.addLayout(button_layout)

        # TabControl (Widget com abas)
        self.tabs = QTabWidget()

        # Instanciar as  abas
        self.pdv_tab = PDVTab()
        self.sincronizador_tab = SincronizadorTab()
        self.integradoripos_tab = IntegradoriposTab()
        self.webapi_tab = WebApiTab()

        # Adiciona uma aba padrão (inicialmente vazia ou apenas uma)
        self.tabs.addTab(self.pdv_tab, "PDV")
        main_layout.addWidget(self.tabs)

        # Botão Executar
        self.execute_button = QPushButton("Executar")
        self.execute_button.setStyleSheet("background-color: green; color: white;")
        self.execute_button.clicked.connect(self.apply_connection_string)
        main_layout.addWidget(self.execute_button)

        self.setLayout(main_layout)

    

    def show_pdv_tab(self):
        if self.tabs.indexOf(self.pdv_tab) == -1:
            self.tabs.addTab(self.pdv_tab, "PDV")
            self.tabs.setCurrentIndex(self.tabs.indexOf(self.pdv_tab))
        # current_index = self.tabs.currentIndex()
        # if self.tabs.widget(current_index) != self.pdv_tab:
        #     self.tabs.removeTab(current_index)
        #     self.tabs.addTab(self.pdv_tab, "PDV")
        #     self.tabs.setCurrentIndex(self.pdv_tab)
    
    def show_sincronizador_tab(self):
        if self.tabs.indexOf(self.sincronizador_tab) == -1:
            self.tabs.addTab(self.sincronizador_tab, "SINCRONIZADOR")
            self.tabs.setCurrentIndex(self.tabs.indexOf(self.sincronizador_tab))

    def show_integradoripos_tab(self):
        if self.tabs.indexOf(self.integradoripos_tab) == -1:
            self.tabs.addTab(self.integradoripos_tab, "INTEGRADORIPOS")
            self.tabs.setCurrentIndex(self.tabs.indexOf(self.integradoripos_tab))
        # current_index = self.tabs.currentIndex()
        # if self.tabs.widget(current_index) != self.integradoripos_tab:
        #     self.tabs.removeTab(current_index)
        #     self.tabs.addTab(self.integradoripos_tab, "INTEGRADORIPOS")
        #     self.tabs.setCurrentIndex(self.integradoripos_tab)

    def show_webapi_tab(self):
        if self.tabs.indexOf(self.webapi_tab) == -1:
            self.tabs.addTab(self.webapi_tab, "WEBAPI")
            self.tabs.setCurrentIndex(self.tabs.indexOf(self.webapi_tab))
        # current_index = self.tabs.currentIndex()
        # if self.tabs.widget(current_index) != self.webapi_tab:
        #     self.tabs.removeTab(current_index)
        #     self.tabs.addTab(self.webapi_tab, "WEBAPI")
        #     self.tabs.setCurrentIndex(self.webapi_tab)

    def apply_connection_string(self):
        # Coletar dados da interface
        app_name = self.tabs.tabText(self.tabs.currentIndex())  # Nome da aba atual
        instance = self.tabs.currentWidget().instance_input.text().strip()
        database = self.tabs.currentWidget().database_input.text().strip()
        user = self.tabs.currentWidget().user_input.text().strip()
        password = self.tabs.currentWidget().password_input.text().strip()

        print(f"Debug: Instance: '{instance}', Database: '{database}', User: '{user}', Password: '{password}'")
        

        empresa = None
        cnpj = None

        # Apenas para PDV, solicitar Empresa e CNPJ
        if app_name == "PDV":
            empresa = self.pdv_tab.pdv_tef_input.text().strip()
            cnpj = self.pdv_tab.pdv_cnpj_input.text().strip()

        # Aplicar a connection string e modificar appSettings (se for o caso)
        self.xml_hundler.apply_connection_string(app_name, instance, database, user, password, empresa, cnpj)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
