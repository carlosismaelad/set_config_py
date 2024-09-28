import xml.etree.ElementTree as ET
from utils.handlers.app_settings_handler import app_settings_handler
from utils.handlers.connection_string_updater import ConnectionStringUpdater as csu
from utils.show_messages import show_message
from exceptions.custom_exceptions import CustomExecption
from PySide6.QtWidgets import QTextEdit

class SincronizadorHandler:

    @staticmethod
    def modify_sincronizador_config(log_widget, config_path, connection_string, ):

        if log_widget is not None and not isinstance(log_widget, QTextEdit):
            print(f"log_widget: {log_widget}, type: {type(log_widget)}")
            raise TypeError("log_widget deve ser uma instância de QTextEdit SINC HANDLER.")
        tree = ET.parse(config_path)
        root = tree.getroot()

        # Atualiza a connectionString se fornecida
        try:
            if connection_string:
                csu.update_connection_string(root, log_widget, config_path, connection_string)
        except ET.ParseError as e:
            error_message = f"Erro ao ler o arquivo XML em {config_path}"
            show_message(log_widget, error_message)
            raise CustomExecption(f"{error_message}: {e}")
        
        try:
            app_settings_handler(root, log_widget=log_widget)
        except Exception as e:
            error_message = f"Erro ao enviar a connectionString de {config_path} para o atualizador"
            show_message(log_widget, error_message)
            raise CustomExecption(f"{error_message}: {e}")
        
        # Gravar as mudanças no arquivo XML
        try:
            tree.write(config_path, encoding="utf-8", xml_declaration=True)
        except Exception as e:
            error_message = f"Erro ao gravar as mudanças no arquivo XML da config em {config_path}"
            show_message(log_widget, error_message)
            raise CustomExecption(f"{error_message}: {e}")