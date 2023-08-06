# -*- coding: utf-8 -*-
import logging
from unittest import TestCase, main
from pakettikauppa.merchant import PkMerchant
from datetime import datetime

logging.basicConfig(
    level=logging.DEBUG,
)


class TestCreateShipment(TestCase):
    @classmethod
    def setUpClass(cls):
        # Vilkas own key for customer id = 65 but end point must be in test mode
        cls.API_KEY = 'd4fb618f-1f44-4dc0-bdce-4993f4b91b77'
        cls.SECRET = 'b5c95243276d3ff398207f8dea3013fef001e6e5f51fb9cb2252f609608a81'
        cls.ROUTING_ID = '1464524676'
        cls.ORDER_ALIAS = 'ORDER10002'

        cls._merchant = PkMerchant(1, cls.API_KEY, cls.SECRET)
        cls.logger = logging.getLogger(__name__)

    def test_empty_parameter(self):
        with self.assertRaises(Exception) as e:
            self._merchant.create_shipment(**{})
        self.logger.debug("Exception message = {}".format(e.exception))

    def test_missing_root_element(self):
        with self.assertRaises(KeyError) as e:
            self._merchant.create_shipment(**{
                'InvalidKey': 'KeyValue'
            })
        self.logger.debug("Exception message = {}".format(e.exception))
        self.assertEqual(str(e.exception), "'eChannel key is missing'")

    def test_missing_routing_element(self):
        with self.assertRaises(KeyError) as e:
            self._merchant.create_shipment(**{
                'eChannel': {
                    'InvalidKey': 'Value'
                }
            })
        self.logger.debug("Exception message = {}".format(e.exception))
        self.assertEqual(str(e.exception), "'ROUTING key is missing'")

    def test_missing_shipment_element(self):
        with self.assertRaises(KeyError) as e:
            self._merchant.create_shipment(**{
                'eChannel': {
                    'ROUTING': {
                        'Routing.Account': 'test',
                        'Routing.Id': '',
                        'Routing.Key': '',
                        'Routing.Name': '',
                        'Routing.Time': '',
                    },
                    'InvalidKey': 'Value'
                }
            })
        self.logger.debug("Exception message = {}".format(e.exception))
        self.assertEqual(str(e.exception), "'Shipment key is missing'")

    def test_empty_routing(self):
        with self.assertRaises(ValueError) as e:
            self._merchant.create_shipment(**{
                'eChannel': {
                    'ROUTING': {},
                    'Shipment': {}
                }
            })
        self.logger.debug("Exception message = {}".format(e.exception))
        self.assertEqual(str(e.exception), "Missing routing data")

    def test_wrong_data_type_routing(self):
        with self.assertRaises(TypeError) as e:
            self._merchant.create_shipment(**{
                'eChannel': {
                    'ROUTING': 'test',
                    'Shipment': {}
                }
            })
        self.logger.debug("Exception message = {}".format(e.exception))
        # self.assertEqual(str(e.exception), "Missing routing data")

    def test_missing_keys_in_routing(self):
        with self.assertRaises(KeyError) as e:
            self._merchant.create_shipment(**{
                'eChannel': {
                    'ROUTING': {
                        'InvalidKey': 'test'
                    },
                    'Shipment': {}
                }
            })
        self.logger.debug("Exception message = {}".format(e.exception))

    def test_missing_sender(self):
        with self.assertRaises(KeyError) as e:
            self._merchant.create_shipment(**{
                'eChannel': {
                    'ROUTING': {
                        'Routing.Account': 'test',
                        'Routing.Id': '',
                        'Routing.Key': '',
                        'Routing.Name': '',
                        'Routing.Time': '',
                    },
                    'Shipment': {
                        'InvalidKey': '',
                    }
                }
            })
        self.logger.debug("Exception message = {}".format(e.exception))
        self.assertEqual(str(e.exception), "'Missing Shipment.Sender key'")

    def test_missing_sender_info(self):
        with self.assertRaises(KeyError) as e:
            self._merchant.create_shipment(**{
                'eChannel': {
                    'ROUTING': {
                        'Routing.Account': 'test',
                        'Routing.Id': '',
                        'Routing.Key': '',
                        'Routing.Name': '',
                        'Routing.Time': '',
                    },
                    'Shipment': {
                        'Shipment.Sender': {},
                    }
                }
            })
        self.logger.debug("Exception message = {}".format(e.exception))

    def test_missing_recipient(self):
        with self.assertRaises(KeyError) as e:
            self._merchant.create_shipment(**{
                'eChannel': {
                    'ROUTING': {
                        'Routing.Account': 'test',
                        'Routing.Id': '',
                        'Routing.Key': '',
                        'Routing.Name': '',
                        'Routing.Time': '',
                    },
                    'Shipment': {
                        'Shipment.Sender': {
                            'Sender.Name1': 'Vilkas Group Oy',
                            'Sender.Addr1': 'Finlaysoninkuja 19',
                            'Sender.Postcode': '33210',
                            'Sender.City': 'Tampere',
                            'Sender.Country': 'FI',
                            'Sender.Phone': '',
                            'Sender.Vatcode': '1234567-8',
                            'Sender.Email': 'tipi@vilkas.fi',
                        },
                    }
                }
            })
        self.logger.debug("Exception message = {}".format(e.exception))
        self.assertEqual(str(e.exception), "'Missing Shipment.Recipient key'")

    def test_missing_recipient_info(self):
        with self.assertRaises(KeyError) as e:
            self._merchant.create_shipment(**{
                'eChannel': {
                    'ROUTING': {
                        'Routing.Account': 'test',
                        'Routing.Id': '',
                        'Routing.Key': '',
                        'Routing.Name': '',
                        'Routing.Time': '',
                    },
                    'Shipment': {
                        'Shipment.Sender': {
                            'Sender.Name1': 'Vilkas Group Oy',
                            'Sender.Addr1': 'Finlaysoninkuja 19',
                            'Sender.Postcode': '33210',
                            'Sender.City': 'Tampere',
                            'Sender.Country': 'FI',
                            'Sender.Phone': '',
                            'Sender.Vatcode': '1234567-8',
                            'Sender.Email': 'tipi@vilkas.fi',
                        },
                        'Shipment.Recipient': {}
                    }
                }
            })
        self.logger.debug("Exception message = {}".format(e.exception))
        self.assertEqual(str(e.exception), "'Missing mandatory key in Shipment.Recipient element'")

    def test_missing_consignment(self):
        with self.assertRaises(KeyError) as e:
            self._merchant.create_shipment(**{
                'eChannel': {
                    'ROUTING': {
                        'Routing.Account': 'test',
                        'Routing.Id': '',
                        'Routing.Key': '',
                        'Routing.Name': '',
                        'Routing.Time': '',
                    },
                    'Shipment': {
                        'Shipment.Sender': {
                            'Sender.Name1': 'Vilkas Group Oy',
                            'Sender.Addr1': 'Finlaysoninkuja 19',
                            'Sender.Postcode': '33210',
                            'Sender.City': 'Tampere',
                            'Sender.Country': 'FI',
                            'Sender.Phone': '',
                            'Sender.Vatcode': '1234567-8',
                            'Sender.Email': 'tipi@vilkas.fi',
                        },
                        'Shipment.Recipient': {
                            'Recipient.Name1': 'Receiver name',
                            'Recipient.Addr1': 'Nikinväylä 3 test',
                            'Recipient.Postcode': '33100',
                            'Recipient.City': 'Tampere',
                            'Recipient.Country': 'FI',
                            'Recipient.Phone': '123456789',
                            'Recipient.Email': 'tipi@vilkas.fi',
                        }
                    }
                }
            })
        self.logger.debug("Exception message = {}".format(e.exception))
        self.assertEqual(str(e.exception), "'Missing Shipment.Consignment key'")

    def test_missing_consignment_info(self):
        with self.assertRaises(KeyError) as e:
            self._merchant.create_shipment(**{
                'eChannel': {
                    'ROUTING': {
                        'Routing.Account': 'test',
                        'Routing.Id': '',
                        'Routing.Key': '',
                        'Routing.Name': '',
                        'Routing.Time': '',
                    },
                    'Shipment': {
                        'Shipment.Sender': {
                            'Sender.Name1': 'Vilkas Group Oy',
                            'Sender.Addr1': 'Finlaysoninkuja 19',
                            'Sender.Postcode': '33210',
                            'Sender.City': 'Tampere',
                            'Sender.Country': 'FI',
                            'Sender.Phone': '',
                            'Sender.Vatcode': '1234567-8',
                            'Sender.Email': 'tipi@vilkas.fi',
                        },
                        'Shipment.Recipient': {
                            'Recipient.Name1': 'Receiver name',
                            'Recipient.Addr1': 'Nikinväylä 3 test',
                            'Recipient.Postcode': '33100',
                            'Recipient.City': 'Tampere',
                            'Recipient.Country': 'FI',
                            'Recipient.Phone': '123456789',
                            'Recipient.Email': 'tipi@vilkas.fi',
                        },
                        'Shipment.Consignment': {}
                    }
                }
            })
        self.logger.debug("Exception message = {}".format(e.exception))
        self.assertEqual(str(e.exception), "'Missing mandatory key in Shipment.Consignment element'")

    def test_create_shipment(self):
        _additional_info_text = "Order no.: " + self.ORDER_ALIAS + "-- Reference no.: 00001"
        req_input = {
            'eChannel': {
                'ROUTING': {
                    'Routing.Account': self.API_KEY,
                    'Routing.Key': self._merchant.get_routing_key(self.ROUTING_ID),
                    'Routing.Id': self.ROUTING_ID,
                    'Routing.Name': self.ORDER_ALIAS,
                    'Routing.Time': datetime.now().strftime('%Y%m%d%H%M%S'),
                },
                'Shipment': {
                    'Shipment.Sender': {
                        'Sender.Contractid': '',
                        'Sender.Name1': 'Vilkas Group Oy',
                        'Sender.Name2': '',
                        'Sender.Addr1': 'Finlaysoninkuja 19',
                        'Sender.Addr2': '',
                        'Sender.Addr3': '',
                        'Sender.Postcode': '33210',
                        'Sender.City': 'Tampere',
                        'Sender.Country': 'FI',
                        'Sender.Phone': '',
                        'Sender.Vatcode': '1234567-8',
                        'Sender.Email': 'tipi@vilkas.fi',
                    },
                    'Shipment.Recipient': {
                        # 'Recipient.Code': '',
                        'Recipient.Name1': 'John Doe',
                        'Recipient.Name2': '',
                        'Recipient.Addr1': 'Nikinväylä 3 test',
                        'Recipient.Addr2': '',
                        'Recipient.Addr3': '',
                        'Recipient.Postcode': '33100',
                        'Recipient.City': 'Tampere',
                        'Recipient.Country': 'FI',
                        'Recipient.Phone': '123456789',
                        'Recipient.Vatcode': '',
                        'Recipient.Email': 'tipi@vilkas.fi',
                    },
                    'Shipment.Consignment': {
                        'Consignment.Reference': '3211479032410',
                        'Consignment.Product': '90010',  # - Posti's product code 2103
                        'Consignment.Contentcode': 'D',
                        'Consignment.ReturnInstruction': 'E',
                        # 'Consignment.ReturnInstruction': None,
                        'Consignment.Invoicenumber': self.ORDER_ALIAS,
                        'Consignment.Merchandisevalue': 150,
                        'Consignment.Currency': 'eur',
                        'Consignment.AdditionalInfo': {
                            'AdditionalInfo.Text': _additional_info_text
                        },
                        'Consignment.AdditionalService': [
                            {
                                'AdditionalService.ServiceCode': '2106',  # pickup point service
                                'AdditionalService.Specifier': {
                                    'name': 'pickup_point_id',
                                    'value': '8547',
                                }
                            },
                            {
                                'AdditionalService.ServiceCode': '3101',  # cash on delivery service
                                'AdditionalService.Specifier': [
                                    {
                                        'name': 'amount',
                                        'value': '150'
                                    },
                                    {
                                        'name': 'account',
                                        'value': 'FI2180000012345678'
                                    },
                                    {
                                        'name': 'codbic',
                                        'value': 'DABAFIHH'
                                    },
                                    {
                                        'name': 'reference',
                                        'value': '12344'
                                    },
                                ]
                            },
                        ],
                        'Consignment.Parcel': [
                            {
                                'Parcel.Reference': '123456',  # not mandatory
                                'Parcel.Packagetype': 'PC',
                                'Parcel.Weight': {'weight_unit': 'kg', 'value': '1.2'},
                                'Parcel.Volume': {'unit': 'm3', 'value': '0.6'},
                                'Parcel.Infocode': '1012',
                                'Parcel.Contents': 'Test products',  # product description
                                'Parcel.ReturnService': '123',
                                # Customs declaration info (for medicine)
                                'Parcel.contentline': {
                                    'contentline.description': 'Puita',
                                    'contentline.quantity': 1,
                                    'contentline.currency': 'EUR',
                                    'contentline.netweight': 1,
                                    'contentline.value': 100,
                                    'contentline.countryoforigin': 'FI',
                                    'contentline.tariffcode': '9608101000',
                                },
                                # this is not really needed in Pakettikauppa but Prinetti
                                'Parcel.ParcelService': []
                            },
                        ]
                    }  # end Shipment.Consignment
                }  # end Shipment
            }  # end eChannel
        }
        dict_res = self._merchant.create_shipment(**req_input)
        status = dict_res['status']
        dict_tracking_code = dict_res['trackingcode']
        # tracking_url = dict_tracking_code['tracking_url']
        tracking_code = dict_tracking_code['value']
        self.assertIsNotNone(dict_res) and self.assertTrue(status) and self.assertIsNotNone(tracking_code)


if __name__ == '__main__':
    main(verbosity=2)
