import xml.etree.ElementTree as ET
from utils.handlers.app_settings_handler import app_settings_handler
from utils.handlers.connection_string_updater import ConnectionStringUpdater as csu
from utils.show_messages import show_message
from exceptions.custom_exceptions import CustomExecption


class WebApiHandler:

    @staticmethod
    def modify_webapi_config(log_widget, config_path, connection_string):

        try:
            try:
                tree = ET.parse(config_path)
                root = tree.getroot()
            except ET.ParseError as e:
                error_message = f"Erro ao ler o arquivo XML em {config_path}"
                show_message(log_widget, error_message)
                raise CustomExecption(f"{error_message}: {e}")

        # Atualiza a connectionString se fornecida
                    
            try:
                if connection_string:
                    csu.update_connection_string(root, log_widget, config_path,  connection_string)
                show_message(log_widget, f"ConnectioString atualizada com sucesso em {config_path}")
            
            except ET.ParseError as e:
                error_message = f"Erro ao ler o arquivo XML em {config_path}"
                show_message(log_widget, error_message)
                raise CustomExecption(f"{error_message}: {e}")
            
            except CustomExecption as e:
                error_message = f"Erro ao ler o arquivo XML em {config_path}"
                show_message(log_widget, error_message)
                raise CustomExecption(f"{error_message}: {e}")
            
            # Gravar as mudanças no arquivo XML  
            try:
                tree.write(config_path, encoding="utf-8", xml_declaration=True)
                show_message(log_widget, f"Config do arquivo {config_path} gravada com sucesso.")
            except Exception as e:
                error_message = f"Erro ao gravar as mudanças no arquivo XML da config em {config_path}"
                show_message(log_widget, error_message)
                raise CustomExecption(f"{error_message}: {e}")
        
        except Exception as e:
            # Lidar com erros gerais que possam ter escapado
            error_message = f"Erro inesperado ao modificar o arquivo {config_path}"
            show_message(log_widget, error_message)
            raise CustomExecption(f"{error_message}: {e}")