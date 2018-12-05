import requests
from mock import MagicMock
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


def test_can_update_aviso():
    client = MagicMock()
    kwargs = dict(
        aviso=1, status='TEST',
        client=client, update_url='test')

    ERPAviso.update(**kwargs)

    client.post.assert_called()
    client.post.assert_called_with(
        'test',
        {'I_AVISO': 1,
         "I_STATUS": 'TEST',
         "I_IDIOMA": "S"})


def test_can_update_aviso_real():
    kwargs = dict(
        client_sap="4259", text="TEXTO CORTO",
        text_larg="TEXTO LARGO", type_service="SM013",
        email="MHERRERA@PUNTACANA.COM",
        service_name='SERVICE NAME')

    erp_aviso = ERPAviso()

    aviso = erp_aviso.create(**kwargs)
    assert(hasattr(aviso, 'aviso'))
    
    client = MagicMock()
    client.post.return_value = None
    kwargs = dict(
        aviso=int(aviso.aviso),
        status='RACO', client=client)
    value = ERPAviso.update(**kwargs)
    assert(value == None)