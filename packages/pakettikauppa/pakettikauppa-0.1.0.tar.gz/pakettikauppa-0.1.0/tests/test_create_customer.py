# -*- coding: utf-8 -*-
import logging
import unittest
# from unittest import TestCase
from pakettikauppa.reseller import PkReseller

logging.basicConfig(
    level=logging.DEBUG,
)


class TestPkReseller(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._reseller = PkReseller(1)
        cls.logger = logging.getLogger(__name__)

    def tearDown(self):
        """
        This method is called after each test
        """
        pass

    def test_empty_parameter(self):
        with self.assertRaises(Exception) as e:
            self._reseller.create_customer(**{})
        self.logger.debug("Exception message = {}".format(e.exception))

    def test_too_short_parameter(self):
        with self.assertRaises(KeyError) as e:
            self._reseller.create_customer(**{
                'name': 'Vilkas Group Oy Test',
            })
        self.logger.debug("Exception message = {}".format(e.exception))

    def test_invalid_key(self):
        with self.assertRaises(KeyError) as e:
            self._reseller.create_customer(**{
                'name2': 'Vilkas Group Oy (Test)',
                'business_id': '12345678-9',
                'payment_service_provider': 'Invoice',
                'psp_merchant_id': '',
                'marketing_name': '',
                'street_address': 'Finlaysoninkuja 19',
                'post_office': 'Tampere',
                'postcode': '33210',
                'country': 'Finland',
                'phone': '+35812345A5',
                'email': 'tipi@vilkas.fi',
                'contact_person_name': 'Porntip Härkönen',
                'contact_person_phone': '0123456789',
                'contact_person_email': 'tipi+test@vilkas.fi',
                'customer_service_phone': '',
                'customer_service_email': '',
            })
        self.logger.debug("Exception message = {}".format(e.exception))

    def test_missing_mandatory_field(self):
        with self.assertRaises(ValueError) as e:
            self._reseller.create_customer(**{
                'name': 'Vilkas Group Oy (Test)',
                'business_id': '12345678-9',
                'payment_service_provider': None,
                'psp_merchant_id': '',
                'marketing_name': '',
                'street_address': 'Finlaysoninkuja 19',
                'post_office': 'Tampere',
                'postcode': '33210',
                'country': None,
                'phone': '+35812345A5',
                'email': 'tipi@vilkas.fi',
                'contact_person_name': 'Porntip Härkönen',
                'contact_person_phone': '0123456789',
                'contact_person_email': 'tipi+test@vilkas.fi',
                'customer_service_phone': '',
                'customer_service_email': '',
            })
        self.logger.debug("Exception message = {}".format(e.exception))

    def test_invalid_payment_service_provider(self):
        _req_data = {
            'name': 'Vilkas Group Oy (Test)',
            'business_id': '12345678-9',
            'payment_service_provider': 'Invoice',
            'psp_merchant_id': '',
            'marketing_name': '',
            'street_address': 'Finlaysoninkuja 19',
            'post_office': 'Tampere',
            'postcode': '33210',
            'country': 'Finland',
            'phone': '+35812345A5',
            'email': 'tipi@vilkas.fi',
            'contact_person_name': 'Porntip Härkönen',
            'contact_person_phone': '0123456789',
            'contact_person_email': 'tipi+test@vilkas.fi',
            'customer_service_phone': '',
            'customer_service_email': '',
        }
        # self.fail()
        with self.assertRaises(ValueError) as e:
            self._reseller.create_customer(**_req_data)
        self.logger.debug("Exception message = {}".format(e.exception))

    def test_missing_checkout_id(self):
        _req_data = {
            'name': 'Vilkas Group Oy (Test)',
            'business_id': '12345678-9',
            'payment_service_provider': 'CHECKOUT',
            'psp_merchant_id': '',
            'marketing_name': '',
            'street_address': 'Finlaysoninkuja 19',
            'post_office': 'Tampere',
            'postcode': '33210',
            'country': 'Finland',
            'phone': '+35812345A5',
            'email': 'tipi@vilkas.fi',
            'contact_person_name': 'Porntip Härkönen',
            'contact_person_phone': '0123456789',
            'contact_person_email': 'tipi+test@vilkas.fi',
            'customer_service_phone': '',
            'customer_service_email': '',
        }
        # self.fail()
        with self.assertRaises(ValueError) as e:
            self._reseller.create_customer(**_req_data)
        self.logger.debug("Exception message = {}".format(e.exception))

    def test_create_customer(self):
        _req_data = {
            'name': 'Vilkas Group Oy (Test)',
            'business_id': '12345678-9',
            'payment_service_provider': '',
            'psp_merchant_id': '',
            'marketing_name': '',
            'street_address': 'Finlaysoninkuja 19',
            'post_office': 'Tampere',
            'postcode': '33210',
            'country': 'Finland',
            'phone': '+35812345A5',
            'email': 'tipi@vilkas.fi',
            'contact_person_name': 'Porntip Härkönen',
            'contact_person_phone': '0123456789',
            'contact_person_email': 'tipi+test@vilkas.fi',
            'customer_service_phone': '',
            'customer_service_email': '',
        }
        res_data = self._reseller.create_customer(**_req_data)
        customer_id = res_data['customer_id']
        self.logger.debug("Created customer id={}".format(customer_id))

        self.assertIsNotNone(customer_id) and self.assertIsNot(customer_id, '')


if __name__ == '__main__':
    unittest.main(verbosity=2)
