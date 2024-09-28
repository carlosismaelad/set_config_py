import xml.etree.ElementTree as ET
from utils.handlers.app_settings_handler import app_settings_handler
from utils.handlers.connection_string_updater import ConnectionStringUpdater as csu
from utils.show_messages import show_message
from exceptions.custom_exceptions import CustomExecption
from PySide6.QtWidgets import QTextEdit
class IntegradoriposHandler:

    @staticmethod
    def modify_integradoripos_config(log_widget, config_path, connection_string):
        if log_widget is not None and not isinstance(log_widget, QTextEdit):
            print(f"log_widget: {log_widget}, type: {type(log_widget)}")
            raise TypeError("log_widget deve ser uma instância de QTextEdit INTEGRADORIPOS HANDLER.")
        try:
            # Ler o arquivo XML
            try:
                tree = ET.parse(config_path)
                root = tree.getroot()
            except ET.ParseError as e:
                error_message = f"Erro ao ler o arquivo XML em {config_path}"
                show_message(log_widget, error_message)
                raise CustomExecption(f"{error_message}: {e}")

            # Atualizar a connection string, se fornecida
            try:
                if connection_string:
                    csu.update_connection_string(root, log_widget, config_path, connection_string)
            except Exception as e:
                error_message = f"Erro ao enviar a connectionString de {config_path} para o atualizador"
                show_message(log_widget, error_message)
                raise CustomExecption(f"{error_message}: {e}")

            # Modificar appSettings usando app_settings_handler
            try:
                app_settings_handler(root, config_path=config_path, log_widget=log_widget)
            except Exception as e:
                error_message = f"Erro ao modificar as appSettings em {config_path}"
                show_message(log_widget, error_message)
                raise CustomExecption(f"{error_message}: {e}")

            # Gravar as mudanças no arquivo XML
            try:
                tree.write(config_path, encoding="utf-8", xml_declaration=True)
                show_message(log_widget, f"Config do arquivo {config_path} modificado com sucesso.")
            except Exception as e:
                error_message = f"Erro ao gravar as mudanças no arquivo XML da config em {config_path}"
                show_message(log_widget, error_message)
                raise CustomExecption(f"{error_message}: {e}")

        except Exception as e:
            # Lidar com erros gerais que possam ter escapado
            error_message = f"Erro inesperado ao modificar o arquivo {config_path}"
            show_message(log_widget, error_message)
            raise CustomExecption(f"{error_message}: {e}")
