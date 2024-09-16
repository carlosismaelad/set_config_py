import sys
import xml.etree.ElementTree as ET
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTabWidget, QListWidget
)
from PySide6.QtCore import Qt

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Gerenciador de Connection Strings - IzzyWay")
        self.setGeometry(300, 300, 400, 300)

        # Layout Principal
        layout = QVBoxLayout()
        
        # Tabs (Aplicação e Configuração)
        self.tabs = QTabWidget()
        
        # Aba Aplicação
        self.applications_tab = QWidget()
        self.setup_applications_tab()
        
        # Aba Configuração
        self.configuration_tab = QWidget()
        self.setup_configuration_tab()
        
        self.tabs.addTab(self.applications_tab, "Aplicação")
        self.tabs.addTab(self.configuration_tab, "Configuração")
        
        layout.addWidget(self.tabs)
        self.setLayout(layout)

    def setup_applications_tab(self):
        layout = QVBoxLayout()

        # Campo para adicionar aplicação
        self.application_input = QLineEdit()
        self.application_input.setPlaceholderText("Digite o nome da aplicação (ex: PDV)")
        layout.addWidget(QLabel("Adicionar Aplicação (padrão: C:/IzzyWay/)"))
        layout.addWidget(self.application_input)

        # Botão para adicionar aplicação
        add_button = QPushButton("+")
        add_button.clicked.connect(self.add_application)
        layout.addWidget(add_button)

        # Lista de Aplicações
        self.applications_list = QListWidget()
        layout.addWidget(self.applications_list)

        self.applications_tab.setLayout(layout)

    def add_application(self):
        app_name = self.application_input.text().strip()
        if app_name:
            full_path = f"C:/IzzyWay/{app_name}"
            self.applications_list.addItem(full_path)
            self.application_input.clear()

    def setup_configuration_tab(self):
        layout = QVBoxLayout()

        # Campos de configuração
        self.instance_input = QLineEdit()
        self.instance_input.setPlaceholderText("Nome da instância do banco de dados (ex: DESKTOP/SQLEXPRESS)")
        layout.addWidget(QLabel("Nome da instância:"))
        layout.addWidget(self.instance_input)
        
        self.database_input = QLineEdit()
        self.database_input.setPlaceholderText("Nome do banco de dados")
        layout.addWidget(QLabel("Nome do banco de dados:"))
        layout.addWidget(self.database_input)

        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Usuário")
        layout.addWidget(QLabel("Usuário:"))
        layout.addWidget(self.user_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Senha")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(QLabel("Senha:"))
        layout.addWidget(self.password_input)

        # Botão Executar
        execute_button = QPushButton("Executar")
        execute_button.clicked.connect(self.apply_connection_string)
        layout.addWidget(execute_button)

        self.configuration_tab.setLayout(layout)

    def apply_connection_string(self):
        instance = self.instance_input.text().strip()
        database = self.database_input.text().strip()
        user = self.user_input.text().strip()
        password = self.password_input.text().strip()

        if not instance or not database or not user or not password:
            print("Preencha todos os campos.")
            return

        connection_string = f"Server={instance};Database={database};user id={user};password={password};Connection Timeout=600;MultipleActiveResultSets=True;Asynchronous Processing=True;"

        # Modificar o connection string em cada aplicação listada
        for i in range(self.applications_list.count()):
            app_path = self.applications_list.item(i).text()
            config_path = f"{app_path}/exe.config"  # Ajuste o caminho conforme o arquivo config

            # Tentar abrir e modificar o arquivo XML
            try:
                self.modify_connection_string(config_path, connection_string)
                print(f"Connection string aplicada com sucesso em: {config_path}")
            except Exception as e:
                print(f"Erro ao modificar o arquivo {config_path}: {e}")

    def modify_connection_string(self, config_path, new_connection_string):
        # Ler o arquivo XML
        tree = ET.parse(config_path)
        root = tree.getroot()

        # Encontrar o nó <connectionStrings> e a connection string específica
        for add_element in root.findall(".//connectionStrings/add"):
            if "connectionString" in add_element.attrib:
                # Substituir a connection string
                add_element.attrib['connectionString'] = new_connection_string

        # Escrever as mudanças no arquivo
        tree.write(config_path, encoding="utf-8", xml_declaration=True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
