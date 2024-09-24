from components.tab_base import TabBase
from PySide6.QtWidgets import QLabel, QLineEdit


class PDVTab(TabBase):
    def __init__(self):
        super().__init__()

        self.pdv_cnpj_input = QLineEdit()
        self.pdv_cnpj_input.setPlaceholderText("Ex: 00612785000153 (sem pontos e sem barras)")
        self.layout.addWidget(QLabel("CNPJ"))
        self.layout.addWidget(self.pdv_cnpj_input)

        self.pdv_tef_empresa_input = QLineEdit()
        self.pdv_tef_empresa_input.setPlaceholderText("Digite o código Tef da empresa")
        self.layout.addWidget(QLabel("Tef Empresa"))
        self.layout.addWidget(self.pdv_tef_empresa_input)