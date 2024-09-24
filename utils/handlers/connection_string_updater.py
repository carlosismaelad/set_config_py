class ConnectionStringUpdater:
    @staticmethod
    def update_connection_string(root, connection_string):
        if connection_string:
            for add_element in root.findall(".//connectionStrings/add"):
                if "connectionString" in add_element.attrib:
                    add_element.attrib["connectionString"] = connection_string
