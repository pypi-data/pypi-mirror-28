import logging
from unittest import TestCase, main
from pakettikauppa.merchant import PkMerchant
from datetime import datetime

logging.basicConfig(
    level=logging.DEBUG,
)


class TestGetShippingLabel(TestCase):
    @classmethod
    def setUpClass(cls):
        # Vilkas own key for customer id = 65 but end point must be in test mode
        cls.API_KEY = 'd4fb618f-1f44-4dc0-bdce-4993f4b91b77'
        cls.SECRET = 'b5c95243276d3ff398207f8dea3013fef001e6e5f51fb9cb2252f609608a81'
        cls.ROUTING_ID = '1464524676'
        cls.ORDER_ALIAS = 'ORDER10002'

        cls._merchant = PkMerchant(1, cls.API_KEY, cls.SECRET)
        cls.logger = logging.getLogger(__name__)

    def test_empty__input_params(self):
        with self.assertRaises(Exception) as e:
            self._merchant.get_shipping_label(**{})
        self.logger.debug("Exception message = {}".format(e.exception))

    def test_missing_root_element(self):
        with self.assertRaises(KeyError) as e:
            self._merchant.get_shipping_label(**{
                'InvalidKey': 'KeyValue'
            })
        self.logger.debug("Exception message = {}".format(e.exception))
        self.assertEqual(str(e.exception), "'eChannel key is missing'")

    def test_missing_routing_element(self):
        with self.assertRaises(KeyError) as e:
            self._merchant.get_shipping_label(**{
                'eChannel': {
                    'InvalidKey': 'Value'
                }
            })
        self.logger.debug("Exception message = {}".format(e.exception))
        self.assertEqual(str(e.exception), "'ROUTING key is missing'")

    def test_empty_routing(self):
        with self.assertRaises(ValueError) as e:
            self._merchant.get_shipping_label(**{
                'eChannel': {
                    'ROUTING': {},
                }
            })
        self.logger.debug("Exception message = {}".format(e.exception))
        self.assertEqual(str(e.exception), "Missing routing data")

    def test_wrong_data_type_routing(self):
        with self.assertRaises(TypeError) as e:
            self._merchant.get_shipping_label(**{
                'eChannel': {
                    'ROUTING': 'test',
                }
            })
        self.logger.debug("Exception message = {}".format(e.exception))

    def test_missing_keys_in_routing(self):
        with self.assertRaises(KeyError) as e:
            self._merchant.get_shipping_label(**{
                'eChannel': {
                    'ROUTING': {
                        'InvalidKey': 'test'
                    },
                }
            })
        self.logger.debug("Exception message = {}".format(e.exception))

    def test_missing_printlabel_element(self):
        with self.assertRaises(KeyError) as e:
            self._merchant.get_shipping_label(**{
                'eChannel': {
                    'ROUTING': {
                        'Routing.Account': self.API_KEY,
                        'Routing.Key': self._merchant.get_routing_key(self.ROUTING_ID),
                        'Routing.Id': self.ROUTING_ID,
                        'Routing.Name': self.ORDER_ALIAS,
                        'Routing.Time': datetime.now().strftime('%Y%m%d%H%M%S'),
                    },
                }
            })
        self.logger.debug("Exception message = {}".format(e.exception))

    def test_missing_printlabel_data(self):
        with self.assertRaises(TypeError) as e:
            self._merchant.get_shipping_label(**{
                'eChannel': {
                    'ROUTING': {
                        'Routing.Account': self.API_KEY,
                        'Routing.Key': self._merchant.get_routing_key(self.ROUTING_ID),
                        'Routing.Id': self.ROUTING_ID,
                        'Routing.Name': self.ORDER_ALIAS,
                        'Routing.Time': datetime.now().strftime('%Y%m%d%H%M%S'),
                    },
                    'PrintLabel': ''
                }
            })
        self.logger.debug("Exception message = {}".format(e.exception))

    def test_missing_response_format_key(self):
        with self.assertRaises(KeyError) as e:
            self._merchant.get_shipping_label(**{
                'eChannel': {
                    'ROUTING': {
                        'Routing.Account': self.API_KEY,
                        'Routing.Key': self._merchant.get_routing_key(self.ROUTING_ID),
                        'Routing.Id': self.ROUTING_ID,
                        'Routing.Name': self.ORDER_ALIAS,
                        'Routing.Time': datetime.now().strftime('%Y%m%d%H%M%S'),
                    },
                    'PrintLabel': {
                        'InvalidKey': ''
                    }
                }
            })
        self.logger.debug("Exception message = {}".format(e.exception))

    def test_invalid_response_format_data(self):
        with self.assertRaises(ValueError) as e:
            self._merchant.get_shipping_label(**{
                'eChannel': {
                    'ROUTING': {
                        'Routing.Account': self.API_KEY,
                        'Routing.Key': self._merchant.get_routing_key(self.ROUTING_ID),
                        'Routing.Id': self.ROUTING_ID,
                        'Routing.Name': self.ORDER_ALIAS,
                        'Routing.Time': datetime.now().strftime('%Y%m%d%H%M%S'),
                    },
                    'PrintLabel': {
                        'responseFormat': 'text',
                    }
                }
            })
        self.logger.debug("Exception message = {}".format(e.exception))

    def test_missing_content_key(self):
        with self.assertRaises(KeyError) as e:
            self._merchant.get_shipping_label(**{
                'eChannel': {
                    'ROUTING': {
                        'Routing.Account': self.API_KEY,
                        'Routing.Key': self._merchant.get_routing_key(self.ROUTING_ID),
                        'Routing.Id': self.ROUTING_ID,
                        'Routing.Name': self.ORDER_ALIAS,
                        'Routing.Time': datetime.now().strftime('%Y%m%d%H%M%S'),
                    },
                    'PrintLabel': {
                        'responseFormat': 'File',
                    }
                }
            })
        self.logger.debug("Exception message = {}".format(e.exception))

    def test_missing_tracking_code_key(self):
        with self.assertRaises(KeyError) as e:
            self._merchant.get_shipping_label(**{
                'eChannel': {
                    'ROUTING': {
                        'Routing.Account': self.API_KEY,
                        'Routing.Key': self._merchant.get_routing_key(self.ROUTING_ID),
                        'Routing.Id': self.ROUTING_ID,
                        'Routing.Name': self.ORDER_ALIAS,
                        'Routing.Time': datetime.now().strftime('%Y%m%d%H%M%S'),
                    },
                    'PrintLabel': {
                        'responseFormat': 'File',
                        'content': {
                            'InvalidKey': ''
                        }
                    }
                }
            })
        self.logger.debug("Exception message = {}".format(e.exception))

    def test_get_shipping_label(self):
        req_input = {
            'eChannel': {
                'ROUTING': {
                    'Routing.Account': self.API_KEY,
                    'Routing.Key': self._merchant.get_routing_key(self.ROUTING_ID),
                    'Routing.Id': self.ROUTING_ID,
                    'Routing.Name': self.ORDER_ALIAS,
                    'Routing.Time': datetime.now().strftime('%Y%m%d%H%M%S'),
                },
                'PrintLabel': {
                    'responseFormat': "File",
                    'content': {
                        # Send request for multiple shipping labels
                        # this is for test credential
                        # 'TrackingCode': [
                        #    {
                        #        'Code': 'JJFITESTLABEL601'
                        #    },
                        #    {
                        #        'Code': 'JJFITESTLABEL602'
                        #    },
                        # ]
                        #
                        # or use this way to send a request for one shipping label
                        # This is for Vilkas API key
                        'TrackingCode': {
                            'Code': 'JJFITESTLABEL1332'
                        }
                    }
                }
            }
        }
        dict_res_data = self._merchant.get_shipping_label(**req_input)
        encoded_pdf_content = dict_res_data['PDFcontent']

        self.assertIsNotNone(dict_res_data) and self.assertIsNotNone(encoded_pdf_content)


if __name__ == '__main__':
    main(verbosity=2)
