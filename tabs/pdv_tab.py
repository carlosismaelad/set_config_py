from components.tab_base import TabBase
from PySide6 import QLabel, QLineEdit

class PDVTab(TabBase):
    def __init__(self):
        super().__init__()

        self.pdv_especifi_input = QLineEdit()
        self.pdv_especifi_input.setPlaceholderText("Digite o código Tef da empresa")
        self.layout.addWidget(QLabel("Tef Empresa"))
        self.layout.addWidget(self.pdv_especifi_input)