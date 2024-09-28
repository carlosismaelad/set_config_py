import os
import xml.etree.ElementTree as ET
from utils.handlers.pdv_handler import PDVHandler
from utils.handlers.sincronizador_handler import SincronizadorHandler
from utils.handlers.integradoripos_handler import IntegradoriposHandler
from utils.handlers.webapi_handler import WebApiHandler
from utils.show_messages import show_message
from exceptions.custom_exceptions import CustomExecption
from PySide6.QtWidgets import QTextEdit


class XmlHundler:

    def __init__(self, app_name):
        self.app_name = app_name


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
    
    
    def find_program_folder(self, izzyway_folder):
        folder_variants = {
            "PDV": ["PDV", "pdv", "Pdv"],
            "SINCRONIZADOR": ["SINCRONIZADOR", "Sincronizador"],
            "INTEGRADORIPOS": ["INTEGRADOR", "INTEGRADORIPOS", "Integradoripos", "IntegradorIpos"],
            "WEBAPI": ["WEBAPI", "Webapi", "WebAPI", "WebApi"]
        }

        for folder in os.listdir(izzyway_folder):
            if folder in folder_variants.get(self.app_name, []):
                return os.path.join(izzyway_folder, folder)
        
        raise FileNotFoundError(f"Pasta do programa {self.app_name} não localizada dentro de {izzyway_folder}!")
    

    def get_config_file(self, program_folder):
        app_config_files = {
            "PDV": "PDVDesktop.exe.config",
            "SINCRONIZADOR": "Sincronizador.exe.config",
            "INTEGRADORIPOS": "IntegradorIPOS.exe.config",
            "WEBAPI": "Web.config"
        }
        return os.path.join(program_folder, app_config_files.get(self.app_name, ""))


    def apply_connection_string(self, log_widget, instance, database, user, password, tef_empresa=00000000, cnpj=11111111111111):

        print("log_widget type XML HANDLER:", type(log_widget))
        if log_widget is not None and not isinstance(log_widget, QTextEdit):
            print(f"log_widget: {log_widget}, type: {type(log_widget)}")
            raise TypeError("log_widget deve ser uma instância de QTextEdit XML HANDLER.")

    
        izzyway_folder = self.find_izzyway_folder()
        program_folder = self.find_program_folder(izzyway_folder)
        config_file = self.get_config_file(program_folder)
        config_path = os.path.join(program_folder, config_file)

        connection_string = (
            f"Server={instance};Database={database};user id={user};password={password};"
            "Connection Timeout=600;MultipleActiveResultSets=True;Asynchronous Processing=True;"
        )

        try:
            if self.app_name == "PDV":
                PDVHandler.modify_pdv_config(log_widget, config_path, connection_string, tef_empresa, cnpj)
            elif self.app_name == "SINCRONIZADOR":
                SincronizadorHandler.modify_sincronizador_config(log_widget, config_path, connection_string)
            elif self.app_name == "INTEGRADORIPOS":
                IntegradoriposHandler.modify_integradoripos_config(log_widget, config_path, connection_string)
            elif self.app_name == "WEBAPI":
                WebApiHandler.modify_webapi_config(log_widget, config_path, connection_string)
        except Exception as e:
            error_message = f"Erro ao repassar os parâmetros para os métodos de alteração."
            show_message(log_widget, error_message)
            raise CustomExecption(f"{error_message}: {e}")

