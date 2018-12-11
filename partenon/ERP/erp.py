import os
from oraculo.gods.sap import APIClient
from oraculo.gods.exceptions import NotFound
from ..base import BaseEntity
from partenon.ERP import exceptions


class ERPClient(BaseEntity):
    _client = APIClient
    _info_url = 'api_portal_clie/datos_cliente'
    client_number = None

    def info(self):
        client = self._client()
        body = {"I_CLIENTE": self.client_number}  
        return client.post(self._info_url, body)


class ERPAviso(BaseEntity):
    _client = APIClient
    _create_url = 'api_portal_clie/crear_aviso'
    _info_url = 'api_portal_clie/info_aviso'
    _create_quotation_url = 'api_portal_clie/create_quotatio' 
    _sap_customer = None
    aviso = None

    @property
    def responsable(self):
        if not hasattr(self, 'aviso'):
            raise AttributeError('Not has atribute aviso')

        body = {
            "I_AVISO" : self.aviso,
            "I_IDIOMA" : 'S'}
        client = self._client()
        response = client.post(self._info_url, body) 
        responsable = response.get('responsable')
        return BaseEntity(**responsable)
    
    @property
    def client(self):
        if not hasattr(self, 'aviso'):
            raise AttributeError('Not has atribute aviso ni cliente')
        
        if not self._sap_customer:
            raise AttributeError('Not has atribute sap_customer')

        client = ERPClient(client_number=self._sap_customer)
        return BaseEntity(**client.info())

    def create(
        self, client_sap, text, text_larg,
        service_name, email, type_service,
        require_quotation=None):

        self._sap_customer = client_sap 
        body = {
            "I_CLIENTE": client_sap,
            "I_TXT_CORTO": text,
            "I_TXT_LARGO": text_larg,
            "I_IDIOMA": "S",
            "I_TEXTO_SERVICIO": service_name,
            "I_ID_SERVICIO": type_service,
            "I_CORREO": email,
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
        client=APIClient,
        update_url='api_portal_clie/update_aviso'):
        client = client()
        body = {
            "I_AVISO": aviso,
            "I_STATUS": status,
            "I_IDIOMA": "S"}
        try:
            return client.post(update_url, body)
        except NotFound:
            message = 'The %s warning does not have a created order.' % aviso
            raise exceptions.NotHasOrder(message) 
    
    def create_quotation(self):
        if not hasattr(self, 'aviso'):
            raise AttributeError('Not has aviso set attribute')
        
        client = self._client()
        body = {"I_AVISO": self.aviso, "I_IDIOMA": "S"}
        response = client.post(self._create_quotation_url, body)
        return response.get('pdf')