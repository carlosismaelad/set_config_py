import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTabWidget, QLineEdit, QTextEdit
from PySide6.QtGui import QIcon
from tabs.pdv_tab import PDVTab
from tabs.sincronizador_tab import SincronizadorTab
from tabs.integradoripos_tab import IntegradoriposTab
from tabs.webapi_tab import WebApiTab
from utils.xml_handler import XmlHundler
from exceptions.custom_exceptions import CustomExecption
from utils.show_messages import show_message
from exceptions.custom_exceptions import CustomExecption

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("IzzyConfig - By IzzyWay")
        self.setWindowIcon(QIcon("izzywaylogo.ico"))
        self.setGeometry(600, 300, 800, 600)

        self.xml_hundler = None

        # Layout principal
        main_layout = QVBoxLayout()

        # Definição dos inputs
        self.instance_input = QLineEdit()
        self.database_input = QLineEdit()
        self.user_input = QLineEdit()
        self.password_input = QLineEdit()
        self.pdv_tef_empresa_input = QLineEdit()  # Apenas para PDV
        self.pdv_cnpj_input = QLineEdit()      # Apenas para PDV

        # Layout de botões
        button_layout = QHBoxLayout()

        # Criação dos botões superiores
        self.pdv_button = QPushButton("PDV")
        self.pdv_button.clicked.connect(self.toggle_show_remove_pdv_tab)

        self.sincronizador_button = QPushButton("SINCRONIZADOR")
        self.sincronizador_button.clicked.connect(self.toggle_show_remove_sincronizador_tab)
        
        self.integradoripos_button = QPushButton("INTEGRADORIPOS")
        self.integradoripos_button.clicked.connect(self.toggle_show_remove_integradoripos_tab)
        
        self.webapi_button = QPushButton("WEBAPI")
        self.webapi_button.clicked.connect(self.toggle_show_remove_webapi_tab)

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
        # self.tabs.addTab(self.pdv_tab, "PDV")

        # Criar aba de logs
        self.log_tab = QWidget()
        self.log_layout = QVBoxLayout()
        self.log_widget = QTextEdit()  # Widget para mostrar logs
        self.log_widget.setReadOnly(True)  # Apenas leitura
        self.log_layout.addWidget(self.log_widget)
        self.log_tab.setLayout(self.log_layout)

        # Adicionar a aba de logs ao QTabWidget
        self.tabs.addTab(self.log_tab, "Logs")

        main_layout.addWidget(self.tabs)

        # Botão Executar
        self.execute_button = QPushButton("Executar")
        self.execute_button.setStyleSheet("background-color: green; color: white;")
        self.execute_button.clicked.connect(self.apply_connection_string)
        main_layout.addWidget(self.execute_button)

        self.setLayout(main_layout)


    def toggle_show_remove_pdv_tab(self):
        index = self.tabs.indexOf(self.pdv_tab)
        if index == -1:
            self.tabs.addTab(self.pdv_tab, "PDV")
        else:
            self.tabs.removeTab(index)
    
    def toggle_show_remove_sincronizador_tab(self):
        index = self.tabs.indexOf(self.sincronizador_tab)
        if index == -1:
            self.tabs.addTab(self.sincronizador_tab, "SINCRONIZADOR")
        else:
            self.tabs.removeTab(index)       

    def toggle_show_remove_integradoripos_tab(self):
        index = self.tabs.indexOf(self.integradoripos_tab)
        if index == -1:
            self.tabs.addTab(self.integradoripos_tab, "INTEGRADORIPOS")
        else:
            self.tabs.removeTab(index)       

    def toggle_show_remove_webapi_tab(self):
        index = self.tabs.indexOf(self.webapi_tab)
        if index == -1:
            self.tabs.addTab(self.webapi_tab, "WEBAPI")
        else:
            self.tabs.removeTab(index)


    def apply_connection_string(self):
        
        # Coletar dados da interface
        app_name = self.tabs.tabText(self.tabs.currentIndex())  # Nome da aba atual
        current_tab = self.tabs.currentWidget()

        instance = current_tab.instance_input.text().strip()
        database = current_tab.database_input.text().strip()
        user = current_tab.user_input.text().strip()
        password = current_tab.password_input.text().strip()

        empresa = None
        cnpj = None

        # Apenas para PDV, solicitar Empresa e CNPJ
        if app_name == "PDV":
            empresa = current_tab.pdv_tef_empresa_input.text().strip()
            cnpj = current_tab.pdv_cnpj_input.text().strip()

        # Criar uma nova instância de XmlHundler passando o app_name
        self.xml_hundler = XmlHundler(app_name)

        # Aplicar a connection string e modificar appSettings (se for o caso)
        try:
            if self.log_widget is not None and not isinstance(self.log_widget, QTextEdit):
                print(f"log_widget: {self.log_widget}, type: {type(self.log_widget)}")
                raise TypeError("log_widget deve ser uma instância de QTextEdit MAIN.PY.")
            self.xml_hundler.apply_connection_string(self.log_widget, instance, database, user, password, empresa, cnpj)
            show_message(self.log_widget, "Parâmetros de entrada repassados.")

        except CustomExecption as e:
            error_message = f"Erro no módulo de entrada da aplicação!"
            show_message(self.log_widget, error_message)
            raise CustomExecption(f"{error_message}: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
