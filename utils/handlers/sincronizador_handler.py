import xml.etree.ElementTree as ET
from utils.handlers.app_settings_handler import app_settings_handler
from utils.handlers.connection_string_updater import ConnectionStringUpdater as csu

class SincronizadorHandler:

    @staticmethod
    def modify_sincronizador_config(config_path, connection_string):
        tree = ET.parse(config_path)
        root = tree.getroot()

        # Atualiza a connectionString se fornecida
        if connection_string:
            csu.update_connection_string(root, connection_string)

        app_settings_handler(root)

        tree.write(config_path, encoding="utf-8", xml_declaration=True)