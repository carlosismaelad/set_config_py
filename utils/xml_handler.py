import os
import xml.etree.ElementTree as ET
from utils.handlers.pdv_handler import PDVHandler
from utils.handlers.sincronizador_handler import SincronizadorHandler
from utils.handlers.integradoripos_handler import IntegradoriposHandler
from utils.handlers.webapi_handler import WebApiHandler

class XmlHundler:

    def find_izzyway_folder(self):
        parent_directory = "C:/"
        folder_name_variants = ["IZZYWAY", "IzzyWay", "Izzyway", "izzyway"]

        izzyway_folder = None

        for folder in os.listdir(parent_directory):
            if folder.lower() in [name.lower() for name in folder_name_variants]:
                izzyway_folder = os.path.join(parent_directory, folder)
                break

        if not izzyway_folder:
            raise FileNotFoundError("Pasta IzzyWay não localizada!")
        
        return izzyway_folder
    
    
    def find_program_folder(self, izzyway_folder, app_name):
        folder_variants = {
            "PDV": ["PDV", "pdv", "Pdv"],
            "SINCRONIZADOR": ["SINCRONIZADOR", "Sincronizador"],
            "INTEGRADORIPOS": ["INTEGRADOR", "INTEGRADORIPOS", "Integradoripos", "IntegradorIpos"],
            "WEBAPI": ["WEBAPI", "Webapi", "WebAPI", "WebApi"]
        }

        for folder in os.listdir(izzyway_folder):
            if folder in folder_variants.get(app_name, []):
                return os.path.join(izzyway_folder, folder)
        
        raise FileNotFoundError(f"Pasta do programa {app_name} não localizada dentro de {izzyway_folder}!")
    

    def get_config_file(self, program_folder, app_name):
        app_config_files = {
            "PDV": "PDVDesktop.exe.config",
            "SINCRONIZADOR": "Sincronizador.exe.config",
            "INTEGRADORIPOS": "IntegradorIPOS.exe.config",
            "WEBAPI": "Web.config"
        }
        return os.path.join(program_folder, app_config_files.get(app_name, ""))


    def apply_connection_string(self, app_name, instance, database, user, password, tef_empresa=None, cnpj=None):
        izzyway_folder = self.find_izzyway_folder()
        program_folder = self.find_program_folder(izzyway_folder, app_name)
        config_file = self.get_config_file(program_folder, app_name)
        config_path = os.path.join(program_folder, config_file)

        connection_string = (
            f"Server={instance};Database={database};user id={user};password={password};"
            "Connection Timeout=600;MultipleActiveResultSets=True;Asynchronous Processing=True;"
        )

        try:
            if app_name == "PDV":
                PDVHandler.modify_pdv_config(config_path, connection_string, tef_empresa, cnpj)
            elif app_name == "SINCRONIZADOR":
                SincronizadorHandler.modify_sincronizador_config(config_path, connection_string)
            elif app_name == "INTEGRADORIPOS":
                IntegradoriposHandler.modify_integradoripos_config(config_path, connection_string)
            elif app_name == "WEBAPI":
                WebApiHandler.modify_webapi_config(config_path, connection_string)
        except Exception as e:
            print(f"Erro ao tentar modificar o arquivo {config_path}: {e}")

