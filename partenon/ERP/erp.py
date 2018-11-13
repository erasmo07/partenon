import os
from oraculo.gods.sap import APIClient
from ..base import BaseEntity


class ERPClient(BaseEntity):
    _client = APIClient()
    _info_url = 'api_portal_clie/datos_cliente'


class ERPAviso(BaseEntity):
    _client = APIClient
    _create_url = 'api_portal_clie/crear_aviso'
    _info_url = 'api_portal_clie/info_aviso'

    def create(
        self, client_sap, text, text_larg,
        service_name, email, type_service, language='S',
        required_cotization=None):
        body = {
            "I_CLIENTE": client_sap, "I_TXT_CORTO": text,
            "I_TXT_LARGO": text_larg, "I_IDIOMA": language,
            "I_TEXTO_SERVICIO": service_name,
            "I_ID_SERVICIO": type_service, "I_CORREO": email,
            "REQUIRED_COTIZATION": True if required_cotization else False}
        client = self._client()
        response = client.post(self._create_url, body)
        return ERPAviso(**response)
    
    def info(self, aviso=None, language="S"):
        body = {
            "I_AVISO" : aviso if aviso else self.aviso,
            "I_IDIOMA" : language}
        client = self._client()
        response = client.post(self._info_url, body) 
        return response