from components.tab_base import TabBase
from PySide6.QtWidgets import QLabel, QLineEdit


class SincronizadorTab(TabBase):
    def __init__(self):
        super().__init__()

        self.sincronizador_disable_info_machine_input = QLineEdit()
        self.sincronizador_disable_info_machine_input.setPlaceholderText("'true' ou 'false'")
        self.layout.addWidget(QLabel("Desabilitar informações da máquina"))
        self.layout.addWidget(self.sincronizador_disable_info_machine_input)