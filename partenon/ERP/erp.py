import os
from oraculo.gods.sap import APIClient
from oraculo.gods.exceptions import NotFound
from ..base import BaseEntity
from . import exceptions


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
        require_quotation=None):
        body = {
            "I_CLIENTE": client_sap, "I_TXT_CORTO": text,
            "I_TXT_LARGO": text_larg, "I_IDIOMA": language,
            "I_TEXTO_SERVICIO": service_name,
            "I_ID_SERVICIO": type_service, "I_CORREO": email,
            "I_REQUIRE_QUOTATION": True if require_quotation else False}
        client = self._client()
        response = client.post(self._create_url, body)
        return ERPAviso(**response)
    
    def info(self, aviso, language="S"):
        body = {
            "I_AVISO" : aviso,
            "I_IDIOMA" : language}
        client = self._client()
        response = client.post(self._info_url, body) 
        return response
    
    @staticmethod
    def update(
        aviso, status,
        client=APIClient(),
        update_url='api_portal_clie/update_aviso'):
        body = {
            "I_AVISO": aviso,
            "I_STATUS": status,
            "I_IDIOMA": "S"}
        try:
            return client.post(update_url, body)
        except NotFound:
            message = 'The %s warning does not have a created order.' % aviso
            raise exceptions.NotHasOrder(message) 