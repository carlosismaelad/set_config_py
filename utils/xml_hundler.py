import os
import xml.etree.ElementTree as ET

class XmlHundler:

    def find_izzyway_folder(self):
        parent_directory = "C:/"
        folder_name_variants = ["IZZYWAY", "IzzyWay", "Izzyway", "izzyway"]

        # Vamos listas as pastas no diretório pai
        for folder in os.listdir(parent_directory):
            if folder.lower() in [name.lower() for name in folder_name_variants]:
                return os.path.join(parent_directory, folder)
        
        raise FileNotFoundError("Pasta IzzyWay não localizada!")

    def apply_connection_string(self, app_name, instance, database, user, password, tef_empresa=None, cnpj=None ):

        base_path = self.find_izzyway_folder()
        config_file = self.get_config_file(base_path, app_name)
        config_path = os.path.join(base_path, config_file)

        print(f"Tentando modificar o arquivo: {config_path}")

        connection_string = (
            f"Server={instance};Database={database};user id={user};password={password};"
            "Connection Timeout=600;MultipleActiveResultSets=True;Asynchronous Processing=True;"
        )

        # Tentar abrir e modificar o XML
        try:
            if app_name == "PDV":
                self.modify_pdv_config(config_path, connection_string, tef_empresa, cnpj)
            else:
                self.modify_generic_config(config_path, connection_string)
        except Exception as e:
            print(f"Erro ao tentar modificar o arquivo {config_path}: {e}")
                  

    def get_config_file(self, base_path, app_name):
        app_config_files = {
            "PDV": "PDVDesktop.exe.config",
            "SINCRONIZADOR": "Sincronizador.exe.config",
            "INTEGRADORIPOS": "IntegradorIPOS.exe.config",
            "WEBAPI": "Web.config"
        }
        app_folder = app_name.upper()  # Converte o nome do aplicativo para maiúsculas para corresponder
        app_path = os.path.join(base_path, app_folder)
        return os.path.join(app_path, app_config_files.get(app_name, ""))
    

    # Modifica apenas a connectionstring de aplicações que precisam de alteração somente em: server, database, user id e password
    def modify_generic_config(self, config_path, connection_string):

        # Ler o XML
        tree = ET.parse(config_path)
        root = tree.getroot()

        # Encontrar o nó <connectionStrings> e modificar
        for add_element in root.findall(".//connectionStrings/add"):
            if connection_string in add_element.attrib:
                add_element.attrib["connectionString"] = connection_string
        
        # Escrever as alterações no arquivo
        tree.write(config_path, encoding="utf-8", xml_declaration=True)


    # modificação exclusiva para PDV
    def modify_pdv_config(self, config_path, connection_string, empresa, cnpj):
        """Modifica tanto a connection string quanto as chaves appSettings para PDV"""
        # Ler o arquivo XML
        tree = ET.parse(config_path)
        root = tree.getroot()

        # Atualizar a connection string
        for add_element in root.findall(".//connectionStrings/add"):
            if "connectionString" in add_element.attrib:
                add_element.attrib['connectionString'] = connection_string

        # Atualizar appSettings
        for add_element in root.findall(".//appSettings/add"):
            if add_element.attrib.get('key') == 'Tef_Empresa':
                add_element.attrib['value'] = empresa
            elif add_element.attrib.get('key') == 'Tef_EmpresaCnpj':
                add_element.attrib['value'] = cnpj

        # Escrever as mudanças no arquivo
        tree.write(config_path, encoding="utf-8", xml_declaration=True)
    
    # Atualiza ou gera o campo DisableInfoMachine em todas as aplicações
    def update_disable_info_machine(self, root):
       
        app_settings = root.find(".//appSettings")
        if app_settings is not None:
            for add_element in app_settings.findall("add"):
                if add_element.attrib.get('key') == 'DisableInfoMachine':
                    add_element.attrib['value'] = 'true'
                    return
            
            # Se DisableInfoMachine não existir, cria o elemento
            new_element = ET.Element("add", key="DisableInfoMachine", value="true")
            app_settings.append(new_element)