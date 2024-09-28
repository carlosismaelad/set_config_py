from utils.show_messages import show_message
from exceptions.custom_exceptions import CustomExecption
from PySide6.QtWidgets import QTextEdit

class ConnectionStringUpdater:
    @staticmethod
    def update_connection_string(root, log_widget, config_path, connection_string):
        if log_widget is not None and not isinstance(log_widget, QTextEdit):
            print(f"log_widget: {log_widget}, type: {type(log_widget)}")
            raise TypeError("log_widget deve ser uma instância de QTextEdit CONNECTIOn STRING UPDATER.")
        try:
            if connection_string:
                for add_element in root.findall(".//connectionStrings/add"):
                    if "connectionString" in add_element.attrib:
                        add_element.attrib["connectionString"] = connection_string
            show_message(log_widget, f"connectionString de {config_path} alterada com sucesso!")
        except CustomExecption as e:
                error_message = f"Erro do atualizador ao atualizar a connection string em {config_path}"
                show_message(log_widget, error_message)
                raise CustomExecption(f"{error_message}: {e}")
