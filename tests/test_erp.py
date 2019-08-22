import requests
from mock import MagicMock
from partenon.base import BaseEntity
from partenon.ERP import ERPAviso, ERPClient


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
    client.post.return_value = []
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


def test_can_update_client_aviso():
    client = MagicMock()
    client.post.return_value = []
    kwargs = dict(
        aviso=1, client_number=1,
        api_client=client, api_url='test')

    ERPAviso.update_client(**kwargs)

    body_expect = {'AVISO': 1, "CLIENT": 1}
    client.post.assert_called()
    client.post.assert_called_with('test', body_expect)


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
    client.post.return_value = {}
    kwargs = dict(
        aviso=int(aviso.aviso),
        status='RACO', client=client)
    value = ERPAviso.update(**kwargs)
    assert(value == {})


def test_can_search_responsable():
    aviso = ERPAviso(aviso=514958)

    assert(isinstance(aviso.responsable, BaseEntity))
    assert(hasattr(aviso.responsable, 'codigo'))
    assert(hasattr(aviso.responsable, 'nombre'))
    assert(hasattr(aviso.responsable, 'nombre'))


def test_can_seach_client():
    kwargs = dict(client_code=4259)
    client = ERPClient(**kwargs)

    response = client.search()

    assert(isinstance(response, list))
    assert(len(response) == 1)
    assert('codigo' in response[0])
    assert('nombre' in response[0])