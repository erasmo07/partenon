import requests
from mock import MagicMock
from partenon.base import BaseEntity
from partenon.ERP import ERPAviso, ERPClient, ERPResidents


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


def test_can_seach_client_by_sap_code():
    kwargs = dict(name='RUBEN DARIO TINEO MORONTA')
    client = ERPResidents(**kwargs)

    response = client.search()

    assert(isinstance(response, list))
    assert(len(response) == 1)

    assert('codigo_sap' in response[0])
    assert(2935 == response[0].get('codigo_sap'))

    assert('nombre' in response[0])
    assert(kwargs.get('name') == response[0].get('nombre'))

    assert('cliente_sap' in response[0])


def test_can_seach_residente_principal_email():
    email = 'miguel@correo.com'
    response = ERPResidents.get_principal_email(email)

    assert(isinstance(response, dict))
    assert('correo' in response)


def test_can_add_email_to_client():
    kwargs = dict(client_code=4259)
    client = ERPClient(**kwargs)
    response = client.add_email('aplicaciones@puntacana.com')
    assert("Correo agregado" == response)


def test_can_check_client_has_credit():
    kwargs = dict(client_code=4259)
    client = ERPClient(**kwargs)

    response = client.has_credit()
    assert(isinstance(response, object))
    assert(len(response) == 1)
    assert('puede_consumir' in response)


def test_can_search_invoices():
    kwargs = dict(client_code=4635)
    client = ERPClient(**kwargs)

    invoices = client.invoices(merchant='349052692')
    assert isinstance(invoices, list)


def test_can_search_invoice_pdf():
    kwargs = dict(client_code=4635)
    client = ERPClient(**kwargs)

    invoice_pdf = client.invoice_pdf(
        document_number='900191818',
        merchant='349052692')

    assert hasattr(invoice_pdf, 'data')
    assert hasattr(invoice_pdf, 'success')


def test_can_list_advance_payment():
    kwargs = dict(client_code=4635)
    client = ERPClient(**kwargs)

    advance_payments = client.advance_payment(
        merchant='349052692', language='E')

    assert isinstance(advance_payments, list)

    for entity in advance_payments:
        assert hasattr(entity, 'bukrs')
        assert hasattr(entity, 'description')
        assert hasattr(entity, 'status')
        assert hasattr(entity, 'id')
        assert hasattr(entity, 'concept_id')
        assert hasattr(entity, 'spras')
