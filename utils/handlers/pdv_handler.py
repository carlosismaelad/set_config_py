import xml.etree.ElementTree as ET
from utils.handlers.app_settings_handler import app_settings_handler
from utils.handlers.connection_string_updater import ConnectionStringUpdater as csu

class PDVHandler:

    @staticmethod
    def modify_pdv_config(config_path, connection_string, empresa, cnpj, log_widget=None):
        
        
        # Ler o arquivo XML
        tree = ET.parse(config_path)
        root = tree.getroot()

        # Atualizar a connection string se fornecida
        if connection_string:

            csu.update_connection_string(root, connection_string)

        additional_settings = {}
        if empresa:
            additional_settings["Tef_Empresa"] = empresa
        if cnpj:
            additional_settings["Tef_EmpresaCnpj"] = cnpj

        app_settings_handler(root, additional_settings, log_widget=log_widget)

        # Escrever as mudanças no arquivo
        tree.write(config_path, encoding="utf-8", xml_declaration=True)

