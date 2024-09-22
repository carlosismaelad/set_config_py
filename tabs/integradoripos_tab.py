from components.tab_base import TabBase
from PySide6.QtWidgets import QLabel, QLineEdit


class IntegradoriposTab(TabBase):
    def __init__(self):
        super().__init__()

        self.integradoripos_disable_notifications_sounds = QLineEdit()
        self.integradoripos_disable_notifications_sounds.setPlaceholderText("'true' ou 'false'")
        self.layout.addWidget(QLabel("Desabilitar sons de notificações"))
        self.layout.addWidget(self.integradoripos_disable_notifications_sounds)