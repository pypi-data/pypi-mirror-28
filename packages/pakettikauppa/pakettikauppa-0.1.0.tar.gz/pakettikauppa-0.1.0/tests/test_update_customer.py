import logging
import unittest
from pakettikauppa.reseller import PkReseller

logging.basicConfig(
    level=logging.DEBUG,
)


class TestPkReseller(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls._reseller = PkReseller(1)
        cls.logger = logging.getLogger(__name__)
        cls.customer_id = 128

    def test_missed_passing_customer_id(self):
        with self.assertRaises(Exception) as e:
            self._reseller.update_customer(**{})
        self.logger.debug("Exception message = {}".format(e.exception))

    def test_empty_customer_id(self):
        with self.assertRaises(Exception) as e:
            self._reseller.update_customer('', **{})
        self.logger.debug("Exception message = {}".format(e.exception))

    def test_empty_parameter(self):
        self.assertIsNone(self._reseller.update_customer(self.customer_id, **{}))

    def test_invalid_key(self):
        with self.assertRaises(Exception) as e:
            self._reseller.update_customer(self.customer_id, **{
                'name2': 'Vilkas Group Oy Test',
            })
        self.logger.debug("Exception message = {}".format(e.exception))

    def test_invalid_customer_id(self):
        with self.assertRaises(Exception) as e:
            self._reseller.update_customer('0', **{
                'name': 'Vilkas Group Oy (Test)',
                'business_id': '12345678-9',
                'customer_service_phone': '12369548',
            })
        self.logger.debug("Exception message = {}".format(e.exception))

    def test_update_customer(self):
        res_data = self._reseller.update_customer(self.customer_id, **{
            'name': 'Vilkas Group Oy (Test)',
            'business_id': '12345678-9',
            'customer_service_phone': '12369548',
        })
        self.assertIsNotNone(res_data)


if __name__ == '__main__':
    unittest.main(verbosity=2)
