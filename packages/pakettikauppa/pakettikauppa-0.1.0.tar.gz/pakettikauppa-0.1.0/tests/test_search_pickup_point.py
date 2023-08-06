# -*- coding: utf-8 -*-
import logging
from unittest import TestCase, main
from pakettikauppa.merchant import PkMerchant


class TestSearchPickupPoint(TestCase):
    @classmethod
    def setUpClass(cls):
        # Vilkas own key for customer id = 65 but end point must be in test mode
        cls.API_KEY = 'd4fb618f-1f44-4dc0-bdce-4993f4b91b77'
        cls.SECRET = 'b5c95243276d3ff398207f8dea3013fef001e6e5f51fb9cb2252f609608a81'

        cls._merchant = PkMerchant(1, cls.API_KEY, cls.SECRET)
        cls.logger = logging.getLogger(__name__)

    def test_empty_parameter(self):
        with self.assertRaises(Exception) as e:
            self._merchant.search_pickup_points(**{})
        self.logger.debug("Exception message = {}".format(e.exception))

    def test_empty_postal_code(self):
        with self.assertRaises(ValueError) as e:
            self._merchant.search_pickup_points(**{
                'postal_code': ''
            })
        self.logger.debug("Exception message = {}".format(e.exception))
        self.assertEqual(str(e.exception), "Require postal code data")

    def test_search_pickup_points_with_postal_code_only(self):
        input_params = {
            'postal_code': '33210',
            'country_code2': '',
            'street_address': '',
            'service_provider': None,
            'max_result': None
        }
        list_data = self._merchant.search_pickup_points(**input_params)
        self.assertIsNotNone(list_data)

    def test_search_pickup_points_with_street_address(self):
        input_params = {
            'postal_code': '33580',
            'country_code2': 'FI',
            'street_address': 'Nikinväylä 3 B 12',
            'service_provider': None,
            'max_result': None
        }
        list_data = self._merchant.search_pickup_points(**input_params)
        self.assertIsNotNone(list_data)

if __name__ == '__main__':
    main(verbosity=2)
