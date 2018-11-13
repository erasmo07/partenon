import requests
from partenon.ERP import ERPAviso 


def test_can_create_aviso():
    kwargs = dict(
        client_sap="4259", text="TEXTO CORTO",
        text_larg="TEXTO LARGO", type_service="SM013",
        email="MHERRERA@PUNTACANA.COM",
        service_name='SERVICE NAME')

    erp_aviso = ERPAviso()
    aviso = erp_aviso.create(**kwargs)
    assert(hasattr(aviso, 'aviso'))