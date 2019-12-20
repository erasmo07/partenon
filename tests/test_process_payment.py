import mock
import pprint
import unittest
from partenon.process_payment import Card, Transaction


class TestTransaction(unittest.TestCase):

    def setUp(self):
        self.card = Card(
            number="4035874000424977", expiration='202012', cvc='977'
        )
        self.transaction = Transaction(card=self.card, amount='100')

        self.keys = [
            'Channel', 'Store', 'CardNumber',
            'Expiration', 'CVC', 'PosInputMode', 'TrxType',
            'Amount', 'ITBIS', 'CurrencyPosCode', 'Payments',
            'Plan', 'AcquirerRefData', 'OrderNumber',
        ]

        self.attrs = [
            'date_time', 'lot_number', 'authorization_code',
            'ticket', 'response_message', 'iso_code',
            'response_code', 'error_description',
            'azul_order_id', 'iso_code']

    def test_can_right_keys(self):
        data = self.transaction.get_data()
        for key in self.keys:
            self.assertIn(key, data)

    def test_success_real_transaction(self):
        # WHEN
        transaction_response = self.transaction.commit()

        # THEN
        for attr in self.attrs:
            self.assertIn(attr, transaction_response.__dict__)
        self.assertTrue(
            transaction_response.is_valid(),
            transaction_response.error_description)

    def test_declinate_real_transaction(self):
        # WHEN
        transaction = Transaction(card=self.card, amount='100000000')
        transaction_response = transaction.commit()

        # THEN
        for attr in self.attrs:
            self.assertIn(attr, transaction_response.__dict__)
        self.assertFalse(
            transaction_response.is_valid(),
            transaction_response.error_description)


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

    def test_can_delete_on_azul(self):
        # GIVE
        self.card.validate('195', 'CODIGO-RAND')
        self.assertTrue(self.card.is_valid())

        # WHEN
        transaction_response = self.card.delete()

        # THEN
        self.assertTrue(transaction_response.is_valid())