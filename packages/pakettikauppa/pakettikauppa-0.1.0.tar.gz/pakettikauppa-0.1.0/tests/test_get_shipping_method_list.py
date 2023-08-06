import logging
from unittest import TestCase, main
from pakettikauppa.merchant import PkMerchant


logging.basicConfig(
    level=logging.DEBUG,
)


class TestGetShippingMethodList(TestCase):
    @classmethod
    def setUpClass(cls):
        cls._merchant = PkMerchant(1)
        cls.logger = logging.getLogger(__name__)

    def test_get_shipping_method_list(self):
        list_data = self._merchant.get_shipping_method_list()
        self.assertIsNotNone(list_data)


if __name__ == '__main__':
    main(verbosity=2)
