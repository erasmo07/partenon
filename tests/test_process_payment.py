import mock
import pprint
import unittest
from partenon.process_payment import Card, Transaction


class TestTransaction(unittest.TestCase):

    def setUp(self):
        self.card = Card(
            number="4035874000424977", expiration='202012', cvc='977'
        )
        self.transaction = Transaction(card=self.card, amount='1000')

    def test_can_right_keys(self):
        keys = [
            'Channel', 'Store', 'CardNumber',
            'Expiration', 'CVC', 'PosInputMode', 'TrxType',
            'Amount', 'ITBIS', 'CurrencyPosCode', 'Payments',
            'Plan', 'AcquirerRefData', 'OrderNumber', 'SaveToDataVault'
        ]
        data = self.transaction.get_data()
        for key in keys:
            self.assertIn(key, data)

    def test_can_make_transaction_real(self):
        # WHEN
        transaction_response = self.transaction.commit()

        # THEN
        attrs = ['date_time', 'lot_number', 'authorization_code',
                 'ticket', 'response_message', 'iso_code',
                 'response_code', 'error_description',
                 'azul_order_id', 'iso_code',]
        for attr in attrs:
            self.assertIn(attr, transaction_response.__dict__)
        self.assertTrue(
            transaction_response.is_valid(),
            transaction_response.error_decription)


class TestCard(unittest.TestCase):

    def setUp(self):
        self.card = Card(
            number="4035874000424977", expiration='202012', cvc='977'
        )
    
    def test_can_save_on_azul(self):
        # WHEN
        self.card.validate('195', 'CODIGO-RAND')

        # THEN
        self.assertTrue(self.card.is_valid())
