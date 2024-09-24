import xml.etree.ElementTree as ET

def app_settings_handler(root, additional_settings=None):
    """
    Atualiza ou cria campos em appSettings.

    Esta função verifica se o campo 'DisableInfoMachine' existe no nó 'appSettings' do XML.
    Se existir, atualiza seu valor para 'true'. Se não existir, cria o campo.
    Além disso, atualiza ou cria outros campos especificados no dicionário 'additional_settings'.

    :param root: Elemento raiz do XML.
    :param additional_settings: Dicionário de configurações adicionais para atualizar ou criar.
                                As chaves são os nomes dos campos e os valores são os valores a serem atribuídos.
                            Exemplo: {'Tef_Empresa': 'Empresa XYZ', 'Tef_EmpresaCnpj': '12345678901234'}
    """

    if additional_settings is None:
        additional_settings = {}
    
    app_settings = root.find(".//appSettings")
    if app_settings is not None:
        disable_info_machine_exists = False
        for add_element in app_settings.findall("add"):
            if add_element.attrib.get('key') == "NaoTocarSom":
                add_element.attrib['value'] = 'true'
            if add_element.attrib.get('key') == "DisableInfoMachine":
                add_element.attrib['value'] = 'true'
                disable_info_machine_exists = True
            # Atualizar outras configurações adicionais
            for key, value in additional_settings.items():
                if add_element.attrib.get('key') == key:
                    add_element.attrib['value'] = value

        # Se DisableInfoMachine não existir, cria o elemento
        if not disable_info_machine_exists:
            new_element = ET.Element("add", key="DisableInfoMachine", value="true")
            app_settings.append(new_element)
        
        # Criar outras configurações adicionais se não existirem
        for key, value in additional_settings.items():
            if not any(add_element.attrib.get('key') == key for add_element in app_settings.findall("add")):
                new_element = ET.Element("add", key=key, value=value)
                app_settings.append(new_element)