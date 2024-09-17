import sys
import os
import xml.etree.ElementTree as ET
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTabWidget, QListWidget, QMessageBox
)
from PySide6.QtCore import Qt

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("SetConfig - By IzzyWay")
        self.setGeometry(600, 300, 800, 600)

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

        # Botão para remover aplicação
        remove_button = QPushButton("-")
        remove_button.clicked.connect(self.remove_aplicacao)
        layout.addWidget(remove_button)

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

    def remove_aplicacao(self):
        selected_items = self.applications_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Aviso", "Selecione um item para remover.")
            return

        for item in selected_items:
            self.applications_list.takeItem(self.applications_list.row(item))

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

        # Lista de mensagens (para mostrar sucessos ou erros)
        self.log_list = QListWidget()
        layout.addWidget(self.log_list)

        # Botão Executar
        execute_button = QPushButton("Executar")
        execute_button.clicked.connect(self.aplicar_na_connectionstring)
        layout.addWidget(execute_button)

        self.configuration_tab.setLayout(layout)

    def aplicar_na_connectionstring(self):
        # Limpar a lista de log antes de cada execução
        self.log_list.clear()

        instance = self.instance_input.text().strip()
        database = self.database_input.text().strip()
        user = self.user_input.text().strip()
        password = self.password_input.text().strip()

        if not instance or not database or not user or not password:
            self.log_list.addItem("Preencha todos os campos.")
            return

        connection_string = f"Server={instance};Database={database};user id={user};password={password};Connection Timeout=600;MultipleActiveResultSets=True;Asynchronous Processing=True;"

        # Modificar o connection string em cada aplicação listada
        for i in range(self.applications_list.count()):
            app_path = self.applications_list.item(i).text()

            # Verificação se o caminho existe
            if not os.path.exists(app_path):
                self.log_list.addItem(f"O caminho {app_path} não existe.")
                continue

            # Verificar se o caminho é um diretório
            if not os.path.isdir(app_path):
                self.log_list.addItem(f"O caminho {app_path} não é um diretório válido.")
                continue

            # Procurar pelo arquivo .exe na pasta da aplicação
            try:
                exe_files = [f for f in os.listdir(app_path) if f.endswith(".exe")]
                if not exe_files:
                    self.log_list.addItem(f"Nenhum arquivo .exe encontrado no caminho {app_path}")
                    continue

                exe_file = exe_files[0]
                config_path = os.path.join(app_path, f"{exe_file}.config")

                # Tentar abrir e modificar o arquivo XML
                try:
                    self.modifica_connectionstring(config_path, connection_string)
                    self.log_list.addItem(f"Connection string aplicada com sucesso em: {config_path}")
                except Exception as e:
                    self.log_list.addItem(f"Erro ao modificar o arquivo {config_path}: {e}")

            except Exception as e:
                self.log_list.addItem(f"Erro ao acessar o caminho {app_path}: {e}")

    def modifica_connectionstring(self, config_path, new_connection_string):
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
