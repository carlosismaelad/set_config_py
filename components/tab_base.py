from PySide6.QtWidgets import QLabel, QLineEdit, QVBoxLayout, QWidget

class TabBase(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()

        # Campos comuns a todas as abas
        self.instance_input = QLineEdit()
        self.instance_input.setPlaceholderText("Nome da instância do banco de dados (ex: DESKTOP/SQLEXPRESS)")
        self.layout.addWidget(QLabel("Instância:"))
        self.layout.addWidget(self.instance_input)

        self.database_input = QLineEdit()
        self.database_input.setPlaceholderText("Nome do banco de dados")
        self.layout.addWidget(QLabel("Banco de Dados:"))
        self.layout.addWidget(self.database_input)

        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Usuário")
        self.layout.addWidget(QLabel("Usuário:"))
        self.layout.addWidget(self.user_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Senha")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.layout.addWidget(QLabel("Senha:"))
        self.layout.addWidget(self.password_input)

        self.setLayout(self.layout)
