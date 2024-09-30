from utils.show_messages import show_message
from exceptions.custom_exceptions import CustomExecption

class ConnectionStringUpdater:
    @staticmethod
    def update_connection_string(root, log_widget, config_path, connection_string):

        try:
            if connection_string:
                for add_element in root.findall(".//connectionStrings/add"):
                    if "connectionString" in add_element.attrib:
                        add_element.attrib["connectionString"] = connection_string
                        
        except CustomExecption as e:
            error_message = f"Erro do atualizador ao atualizar a connection string em {config_path}"
            show_message(log_widget, error_message)
            raise CustomExecption(f"{error_message}: {e}")
        
        except Exception as e:
            # Captura e trata qualquer outro erro genérico
            error_message = f"Ocorreu um erro ao processar o arquivo XML em {config_path}"
            show_message(log_widget, error_message)
            raise CustomExecption(f"{error_message}: {e}")

