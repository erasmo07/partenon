import os
from oraculo.gods.sap import APIClient
from ..base import BaseEntity


class ERPAviso(BaseEntity):
    _client = APIClient()
    _create_url = '/api_portal_clie/crear_aviso'

    def create(
        self, client_sap, text, text_larg,
        email, id_service, language='S'):

        body = {
            "I_CLIENTE": client_sap, "I_TXT_CORTO": text,
            "I_TXT_LARGO": text_larg, "I_IDIOMA": language,
            "I_ID_SERVICIO": id_service, "I_CORREO": email 
        } 

        response = self._client.post(self._create_url, body)
        return ERPAviso(**response) 