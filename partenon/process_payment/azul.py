import os
import re
from oraculo.gods.azul import APIClient


def convert(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


class TransactionResponse:
    response_code = None
    error_decription = None
    data_vault_token = None
    data_vault_expiration = None
    data_vault_brand = None

    def __init__(self, **kwargs):
        self.kwargs = kwargs
        for key, value in kwargs.items():
            self.__dict__.update({convert(key): value})

    def is_valid(self):
        return False if self.response_code == 'Error' else True


class Transaction:
    _path_csr = os.environ.get('AZUL_PATH_CSR')
    _currency_post_code = os.environ.get('AZUL_CURRENCYPOSTCODE')
    _customer_service_phone = os.environ.get('AZUL_CUSTOMER_SERVICE_PHONE', '')
    _ecommerce_url = os.environ.get('AZUL_ECOMMERCE_URL')
    _store = os.environ.get('AZUL_STORE')
    _channel = os.environ.get('AZUL_CHANNEL')
    _pos_inpu_mode = os.environ.get('AZUL_POSINPUMODE', "E-Commerce")
    merchan_name = os.environ.get("AZUL_MERCHAN_NAME")
    amount = None
    api_client = APIClient
    card = None
    _url = '/webservices/JSON/Default.aspx'

    def __init__(
            self, card,
            amount,
            itbis=None,
            type_transaction='Sale',
            order_number=None,
            merchan_name=None,
            save_to_data_vault=None):
        self.amount = amount
        self.card = card
        self.itbis = itbis if itbis else ''
        self.merchan_name = merchan_name if merchan_name else self.merchan_name
        self.order_number = order_number if order_number else ""
        self.save_to_data_vault = save_to_data_vault
        self.type_transaction = type_transaction

    def get_data(self):
        data = dict()
        data.update(self.get_default_keys())
        data['SaveToDataVault'] = self.save_to_data_vault if self.save_to_data_vault else ''

        if self.card.token is None:
            data.update({
                "CardNumber": self.card.number,
                "CVC": self.card.cvc,
                "Expiration": self.card.expiration
            })
        else:
            data.update({
                "DataVaultToken": self.card.token,
                "CardNumber": '', "Expiration": '' })
        return data

    def get_default_keys(self):
        return {
            'AcquirerRefData': '1', 'Channel': self._channel,
            'CurrencyPosCode': self._currency_post_code,
            'CustomerServicePhone': self._customer_service_phone,
            'ECommerceURL': self._ecommerce_url,
            'OrderNumber': self.order_number, 'Payments': '1', 'Plan': '0',
            'PosInputMode': self._pos_inpu_mode, 'Store': self._store,
            'TrxType': self.type_transaction, 'Amount': self.amount,
            'ITBIS': self.itbis
        }

    def commit(self):
        response = self.api_client().post(self._url, self.get_data())
        return TransactionResponse(**response)


class Card:
    merchan_name = os.environ.get("AZUL_MERCHAN_NAME")
    _is_valid = False
    transaction_class = Transaction
    token_expiration = None
    branch = None
    number = None
    expiration = None
    cvc = None

    def __init__(self, token=None, number=None, expiration=None, cvc=None):
        self.token = token
        self.number = number
        self.expiration = expiration
        self.cvc = cvc
    
    def is_valid(self):
        return self._is_valid

    def validate(self, amount, code):
        merchan_name = code = "%s-%s" % (self.merchan_name, code)
        transaction = self.transaction_class(
            self,
            amount=amount,
            merchan_name=merchan_name,
            save_to_data_vault="1"
        ).commit()

        if transaction.is_valid():
            self._is_valid = True

            self.token = transaction.data_vault_token
            self.token_expiration = transaction.data_vault_expiration
            self.brand = transaction.data_vault_brand
            return (self.token, self.token_expiration, self.brand)
