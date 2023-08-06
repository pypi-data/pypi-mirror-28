# -*- coding: utf-8 -*-
""" This is a module for Pakettikauppa integration for merchants to use

The module provides below functionality:
    1. Get shipping method list
    2. Get additional service list
    3. Search pickup points
    4. Get shipment status
    5. Create shipment
    6. Get shipping label
"""
from __future__ import absolute_import

__version__ = '0.1'
__author__ = 'Porntip Chaibamrung'

import sys
import logging
from base64 import b64decode
from time import time
from datetime import datetime
from xml.dom import minidom
from xml.etree import ElementTree as ET
from .pakettikauppa import Pakettikauppa, PakettikauppaException, check_api_name

if sys.version_info < (3, 0):
    from six.moves import reload_module
    reload_module(sys)
    sys.setdefaultencoding('utf8')


def decode_pdf_content(encoded_pdf_content):
    decoded_pdf_content = b64decode(encoded_pdf_content)
    return decoded_pdf_content


def write_pdf_to_file(target_file_path, pdf_content):
    with open(target_file_path, 'wb') as f:
        f.write(pdf_content)
    return 1


class PkMerchant(Pakettikauppa):
    _api_key = None
    _secret = None
    _isInTestMode = 1
    _api_mapping = {
        'get_shipping_method_list': '/shipping-methods/list',
        'get_additional_service_list': '/additional-services/list',
        'search_pickup_points': '/pickup-points/search',
        'get_shipment_status': '/shipment/status',
        'create_shipment': '/prinetti/create-shipment',
        'get_shipping_label': '/prinetti/get-shipping-label'
    }
    _package_types = ('PC', 'PU', 'ZPF', 'ZPE', 'ZPT', 'CG', 'ZPX', 'PM', 'TB', 'TC', 'TU', 'LTK', 'KA', 'VA')
    #  Possible package type codes
    # 'PC' = Paketti / Kirje
    # 'PU' = Rullakko
    # 'ZPF' = FIN-lava (100x120)
    # 'ZPE' = EURO-lava(80x120)
    # 'ZPT' = TEHO-lava(80x60)
    # 'CG' = Häkki
    # 'ZPX' = Huonekalulava
    # 'PM' = Termolaatikko 40 litraa
    # 'TB' = Termolaatikko 102 litraa
    # 'TC' = Termolaatikko 65 litraa
    # 'TU' = Termorullakko
    # 'LTK' = Laatikko
    # 'KA' = Kassi
    # 'VA' = Vaunu

    _return_instruction_codes = ('E', 'H', 'L')
    # 'E' = Edullisinta reittiä (most economical route)
    # 'H' = Hävitetään (treat as abandoned)
    # 'L' = Lentoteitse (immediately by air)

    _content_codes = ('D', 'E', 'G', 'M', 'S')
    # 'D' = Asiakirjoja (Documents)
    # 'E' = DocPack (Envelope)
    # 'G' = Lahja (Gift)
    # 'M' = Kauppatavaraa (Merchandise)
    # 'S' = Näyte (Sample)

    _accept_sender_keys = ('Sender.Contractid', 'Sender.Name1', 'Sender.Name2', 'Sender.Addr1', 'Sender.Addr2',
                           'Sender.Addr3', 'Sender.Postcode', 'Sender.City', 'Sender.Country', 'Sender.Phone',
                           'Sender.Vatcode', 'Sender.Email')

    _accept_recipient_keys = ('Recipient.Code', 'Recipient.Name1', 'Recipient.Name2', 'Recipient.Addr1',
                              'Recipient.Addr2', 'Recipient.Addr3', 'Recipient.Postcode', 'Recipient.City',
                              'Recipient.Country', 'Recipient.Phone', 'Recipient.Vatcode', 'Recipient.Email')

    _accept_parcel_keys = ('Parcel.Reference', 'Parcel.Packagetype', 'Parcel.Weight', 'Parcel.Volume',
                           'Parcel.Infocode', 'Parcel.Contents', 'Parcel.ReturnService', 'Parcel.contentline',
                           'Parcel.ParcelService')

    _accept_content_line_keys = ('contentline.description', 'contentline.quantity', 'contentline.currency',
                                 'contentline.netweight')

    def __init__(self, is_test_mode=0, api_key=None, secret=None):
        """
        Constructor for the class.
        :param is_test_mode: integer value to identify test mode operation. Default value is zero. If you set value to\
        one, you don't need to pass data to 'api_key' and 'secret' parameter unless you want to use your own test\
        credential.
        :param api_key: string of API key
        :param secret: string of secret key
        :rtype class object
        """
        self._isInTestMode = is_test_mode

        # super().__init__(self._isInTestMode) # for Python3 only
        super(PkMerchant, self).__init__(self._isInTestMode)

        self.mylogger = logging.getLogger(__name__)

        if self._isInTestMode == 1:
            if api_key is None or api_key == '':
                self._api_key = '00000000-0000-0000-0000-000000000000'
            else:
                self._api_key = api_key

            if secret is None or secret == '':
                self._secret = '1234567890ABCDEF'
            else:
                self._secret = secret
        else:
            if api_key is None:
                raise PakettikauppaException("API key", "Missing API key")
            else:
                self._api_key = api_key
            if secret is None:
                raise PakettikauppaException("Secret key", "Missing API secret key")
            else:
                self._secret = secret

    @check_api_name
    def get_api_suffix(self, api_name=None):
        """
        Get API suffix for the API name
        :param api_name: string of API name
        :return api_suffix: string of API suffix
        """
        if api_name in self._api_mapping:
            return str(self._api_mapping[api_name])
        else:
            raise PakettikauppaException(
                KeyError,
                "Invalid API name. Possible value are 'get_shipping_method_list', 'get_additional_service_list'"
            )

    def get_api_config(self, api_name=None):
        """
        Constructs API configuration

        :param api_name: string of API name
        :return dict_data: dictionary of configuration data

        dict_data keys:
            api_post_url (string): post URL address
            api_key (string): API key
            api_secret (string): secret key
        """
        _api_suffix = self.get_api_suffix(api_name)
        _api_post_url = super(PkMerchant, self).get_post_url(_api_suffix)
        _api_config = {
            'api_post_url': _api_post_url,
            'api_key': self._api_key,
            'api_secret': self._secret
        }
        return _api_config

    def search_pickup_points(self, **kwargs):
        """
        Main method to search pickup points

        :param kwargs: see get_pickup_point_req_data() function

        :return: list of pickup point data
        """
        _api_config = self.get_api_config('search_pickup_points')

        dict_req_data = self.get_pickup_point_req_data(_api_config['api_key'], **kwargs)

        res_obj = super(PkMerchant, self).send_request('POST', _api_config['api_post_url'], dict_req_data)
        # self.get_res_pickup_point_data(res_obj)
        return self.parse_res_to_list(res_obj)

    def get_res_pickup_point_data(self, res_obj):
        """
        Just helper function for testing looping through list data

        :param res_obj: response object
        :return: list_data: list of pickup points
        """
        list_data = res_obj.json()
        self.mylogger.debug("Response JSON data = {}".format(list_data))
        self.mylogger.debug("\n")

        # print("data item " + json.loads(list_data))
        for dict_item in list_data:
            self.mylogger.debug("item = {}".format(dict_item))
            self.mylogger.debug("\n")

        return list_data

    def get_pickup_point_req_data(self, api_key, **kwargs):
        """
        Constructs request data for search pickup point API

        :param api_key: string of API key
        :param kwargs:

        Kwargs:
            postal_code (string): postal code (mandatory)
            country_code2 (string): 2 letters of country code i.e 'FI'. Default is 'FI'
            street_address (string): street address
            service_provider (string): Limits search to a single service provider, possible values: "Posti", \
            "Matkahuolto" or "Db Schenker". Case insensitive values.
            max_result (integer): maximum number of search results. Default is 5

        :return dict_data: dictionary of request data
        """

        # key error is thrown automatically if postal code is empty
        _postal_code = kwargs['postal_code']
        if _postal_code is None or _postal_code == '':
            raise ValueError("Require postal code data")

        _country_code2 = kwargs['country_code2']
        if _country_code2 is None or _country_code2 == '':
            _country_code2 = 'FI'
        else:
            _country_code2 = _country_code2.upper()

        _street_address = kwargs['street_address']
        _service_provider = kwargs['service_provider']

        _max_result = kwargs['max_result']
        if _max_result is None:
            _max_result = 5
        else:
            _max_result = int(_max_result)

        dict_req_data = {
            'api_key': api_key,
            'postcode': str(_postal_code),
            'timestamp': str(int(time())),
            # 'timestamp': '1512575546', # for testing only
            'limit': _max_result,
            'country': _country_code2,
        }
        if _street_address is not None:
            dict_req_data['address'] = _street_address
        if _service_provider is not None:
            dict_req_data['service_provider'] = _service_provider

        # Calculate MAC
        digest_string = self.get_hash_sha256(self._secret, **dict_req_data)
        dict_req_data['hash'] = digest_string
        self.mylogger.debug("Hash input data for pickup point search= {}".format(dict_req_data))

        # content_string = ''
        # for key, value in dict_req_data.items():
        #    content_string += key + '&' + value

        return dict_req_data

    def get_shipping_method_list(self, language_code2='EN'):
        """
        Get list of available shipping method for the account

        :param language_code2: 2 letters of language code. Default value is 'EN'
        :return list_data: list of response data
        """
        if language_code2 is not None:
            language_code2 = language_code2.upper()

        _api_config = self.get_api_config('get_shipping_method_list')

        dict_req_data = {
            'api_key': _api_config['api_key'],
            'timestamp': str(int(time())),
            'language': language_code2
        }

        digest_string = self.get_hash_sha256(self._secret, **dict_req_data)
        dict_req_data['hash'] = digest_string
        self.mylogger.debug("Hash input data = {}".format(dict_req_data))

        res_obj = super(PkMerchant, self).send_request('POST', _api_config['api_post_url'], dict_req_data)

        return self.parse_res_to_list(res_obj)

    def get_additional_service_list(self, language_code2='EN'):
        """
        Get list of additional service for the account

        :param language_code2: 2 letters of language code. Default value is 'EN'
        :return list_data: list of response data
        """
        if language_code2 is not None:
            language_code2 = language_code2.upper()

        if language_code2 == '':
            language_code2 = 'EN'

        _api_config = self.get_api_config('get_additional_service_list')

        dict_req_data = {
            'api_key': _api_config['api_key'],
            'timestamp': str(int(time())),
            'language': language_code2
        }
        digest_string = self.get_hash_sha256(self._secret, **dict_req_data)
        dict_req_data['hash'] = digest_string
        self.mylogger.debug("Hash input data = {}".format(dict_req_data))

        res_obj = super(PkMerchant, self).send_request('POST', _api_config['api_post_url'], dict_req_data)

        return self.parse_res_to_list(res_obj)

    def create_shipment(self, **kwargs):
        """
        Main function to send a request to Pakettikauppa to create shipment.

        :param kwargs: See get_xml_shipment_req_data() function
        :return dict_data: See parse_xml_create_shipment_res() function
        """
        # This API send request data in XML format
        _api_config = self.get_api_config('create_shipment')

        # xml_req_data = None
        if self._isInTestMode:
            if kwargs is not None:
                xml_req_data = self.get_xml_shipment_req_data(**kwargs)
            else:
                xml_req_data = self.get_create_shipment_test_req_data()
        else:
            xml_req_data = self.get_xml_shipment_req_data(**kwargs)

        headers = {
            'Content-Encoding': 'utf-8',
            'Content-Type': 'application/xml'
        }
        res_obj = super(PkMerchant, self).send_request('POST', _api_config['api_post_url'], xml_req_data, **headers)
        xml_res_string = res_obj.text
        self.mylogger.debug("Response XML string = {}".format(xml_res_string))

        return self.parse_xml_create_shipment_res(xml_res_string)

    def create_shipment_with_simple_data(self, **kwargs):
        """
        Same as create_shipment() function expect the input parameter is in shorter format

        This API send request data in XML format.

        :param kwargs: see get_simple_test_data_create_shipment() function
        :return dict_data: See parse_xml_create_shipment_res() function
        """
        _api_config = self.get_api_config('create_shipment')

        if self._isInTestMode:
            if kwargs is not None:
                xml_req_data = self.get_xml_shipment_req_data(**kwargs)
            else:
                simple_dict_data = self.get_simple_test_data_create_shipment()
                req_data = self.get_proper_req_data_create_shipment(**simple_dict_data)
                xml_req_data = self.get_xml_shipment_req_data(**req_data)
        else:
            xml_req_data = self.get_xml_shipment_req_data(**kwargs)

        headers = {
            'Content-Encoding': 'utf-8',
            'Content-Type': 'application/xml'
        }
        res_obj = super(PkMerchant, self).send_request('POST', _api_config['api_post_url'], xml_req_data, **headers)
        xml_res_string = res_obj.text
        self.mylogger.debug("Response XML string = {}".format(xml_res_string))

        return self.parse_xml_create_shipment_res(xml_res_string)

    def parse_xml_create_shipment_res(self, xml_string):
        """
        Constructs dictionary from response XML string

        :param xml_string: string of XML data
        :return dict_data: dictionary of response data

        dict_data contains following keys:
            status (integer): 1 = status OK
            message (string): response message from Pakettikauppa
            reference (dictionary): contains two keys: 'uuid' and 'value'
            trackingcode (dictionary): contains two keys: 'tracking_url' and 'value' (tracking code)
        """
        root = ET.fromstring(xml_string)
        status_element = root.find("response.status")
        status = str(status_element.text)
        self.mylogger.debug("Response status from Pakettikauppa = {}".format(status))
        message_element = root.find("response.message")

        # Pakettikauppa return status=0 means OK
        if status == '0':
            ref_element = root.find("response.reference")
            uuid = ref_element.get("uuid")
            tracking_code_element = root.find("response.trackingcode")
            tracking_url = tracking_code_element.get("tracking_url")

            dict_res = {
                'status': 1,
                'message': message_element.text,
                'reference': {'uuid': uuid, 'value': ref_element.text},
                'trackingcode': {'tracking_url': tracking_url, 'value': tracking_code_element.text}
            }
        else:
            dict_res = {
                'status': 0,
                'message': message_element.text,
                'reference': None,
                'trackingcode': None
            }
            self.mylogger.error("Error code = {}, Message={}".format(status, message_element.text))

        self.mylogger.debug("Hash return data = {}".format(dict_res))
        return dict_res

    def get_routing_key(self, routing_id):
        """
        Calculate routing key.

        :param routing_id: string of routing ID
        :return digest_string: digest string of MD5 hash
        """
        digest_string = self.get_md5_hash(self._api_key, self._secret, routing_id)
        return digest_string

    def get_create_shipment_test_req_data(self):
        """
        Generates test data set for create shipment request call.

        :return dict_data: dictionary of request data
        """
        dict_data = self.get_create_shipment_test_data()
        return self.get_xml_shipment_req_data(**dict_data)

    def get_simple_test_data_create_shipment(self):
        """
        Generate more simplify version of request data of create shipment API. Output of this function should then pass
        to get_proper_req_data_create_shipment() function to get right data structure for request input data.

        For full version see get_create_shipment_test_data() function.

        :return dict_data: dictionary of request data
        """
        routing_id = '1464524676'
        order_alias = 'ORDER001'

        dict_data = {
            'Routing': {
                'account': self._api_key,
                'id': routing_id,
                'name': order_alias,
            },
            'Shipment': {
                'Sender': {
                    'Name': 'Vilkas Group Oy',
                    'Address': 'Finlaysoninkuja 19',
                    'PostalCode': '33210',
                    'City': 'Tampere',
                    'Country': 'FI',
                    'Phone': '',
                    'Vatcode': '1234567-8',
                    'Email': 'tipi@vilkas.fi',
                },
                'Recipient': {
                    'Name': 'Receiver name',
                    'Address': 'Nikinväylä 3 test',
                    'PostalCode': '33100',
                    'City': 'Tampere',
                    'Country': 'FI',
                    'Phone': '123456789',
                    'Vatcode': '',
                    'Email': 'tipi@vilkas.fi',
                },
                'Consignment': {
                    'Reference': '3211479032410',
                    'ProductCode': '90010',  # - Posti's product code 2103
                    'ContentCode': 'D',  # Order->get('PR_ContentCode')
                    'ReturnInstruction': 'E',  # Order->get('PR_ReturnInstruction')
                    'InvoiceNumber': order_alias,
                    'MerchandiseValue': 150,  # Order->get('PR_Merchandisevalue')
                    'Currency': 'EUR',
                    'AdditionalInfoText': "Order no.: 1107-1 -- Reference no.: 284554",
                    'AdditionalServices': [
                        {
                            'ServiceCode': '2106',  # pickup point service
                            'Specifier': {
                                'name': 'pickup_point_id',
                                'value': '8547',
                            }
                        },
                        {
                            'ServiceCode': '3101',  # cash on delivery service
                            'Specifier': [
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
                    'Parcels': [
                        {
                            'Reference': '123456',  # not mandatory
                            'PackageType': 'PC',
                            'Weight': {'weight_unit': 'kg', 'value': '1.2'},
                            'Volume': {'unit': 'm3', 'value': '0.6'},
                            'InfoCode': '1012',
                            'Contents': 'Test products',  # product description
                            'ReturnService': '123',
                            # Customs declaration info (for medicine)
                            'ContentLine': {
                                'description': 'Puita',
                                'quantity': 1,
                                'currency': 'EUR',
                                'netweight': 1,
                                'value': 100,
                                'countryoforigin': 'FI',
                                'tariffcode': '9608101000',
                            },
                            # this is not really needed in Pakettikauppa but Prinetti
                            # 'ParcelServices': []
                            'ParcelServices': [
                                {
                                    'ServiceCode': 'parcel service code'
                                },
                                {
                                    'ServiceCode': 'parcel service code 2'
                                },
                            ]
                        },
                        {
                            'Reference': '123457',
                            'PackageType': 'PC',
                            'Weight': {'weight_unit': 'kg', 'value': '1.2'},
                            'Volume': {'unit': 'm3', 'value': '0.6'},
                            'InfoCode': '1012',
                            'Contents': 'Muttereita ja puita',  # product description
                            'ReturnService': '123',
                            # Customs declaration info (for medicine)
                            'ContentLine': {},
                            'ParcelServices': None
                        },
                    ]
                }  # end Shipment.Consignment
            }  # end Shipment
        }

        return dict_data

    def get_proper_req_data_create_shipment(self, **simple_dict_data):
        """
        Generate low lever of request input data for create shipment API.

        :param simple_dict_data: see output of get_simple_test_data_create_shipment() function
        :return dict_data: dictionary of request data
        """
        if simple_dict_data is None:
            raise KeyError("Require dictionary of input parameters for formatting")

        _routing_id = simple_dict_data['Routing']['id']

        dict_data = {
            'eChannel': {
                'ROUTING': {
                    'Routing.Account': simple_dict_data['Routing']['account'],
                    'Routing.Key': self.get_routing_key(_routing_id),
                    'Routing.Id': _routing_id,
                    'Routing.Name': simple_dict_data['Routing']['name'],
                    'Routing.Time': datetime.now().strftime('%Y%m%d%H%M%S'),
                    # - Ignored parameters in Pakettikauppa
                    # 'Routing.Target' => { 'content' => '' },
                    # 'Routing.Source' => { 'content' => '' },
                    # 'Routing.Version'  => { 'content' => '' },
                    # 'Routing.Mode' => { 'content' => '' },
                },
                'Shipment': {
                    'Shipment.Sender': {
                        'Sender.Contractid': '',
                        'Sender.Name1': simple_dict_data['Shipment']['Sender']['Name'],
                        'Sender.Name2': '',
                        'Sender.Addr1': simple_dict_data['Shipment']['Sender']['Address'],
                        'Sender.Addr2': '',
                        'Sender.Addr3': '',
                        'Sender.Postcode': simple_dict_data['Shipment']['Sender']['PostalCode'],
                        'Sender.City': simple_dict_data['Shipment']['Sender']['City'],
                        'Sender.Country': simple_dict_data['Shipment']['Sender']['Country'],
                        'Sender.Phone': simple_dict_data['Shipment']['Sender']['Phone'],
                        'Sender.Vatcode': simple_dict_data['Shipment']['Sender']['Vatcode'],
                        'Sender.Email': simple_dict_data['Shipment']['Sender']['Email'],
                    },
                    'Shipment.Recipient': {
                        'Recipient.Code': '',
                        'Recipient.Name1': simple_dict_data['Shipment']['Recipient']['Name'],
                        'Recipient.Name2': '',
                        'Recipient.Addr1': simple_dict_data['Shipment']['Recipient']['Address'],
                        'Recipient.Addr2': '',
                        'Recipient.Addr3': '',
                        'Recipient.Postcode': simple_dict_data['Shipment']['Recipient']['PostalCode'],
                        'Recipient.City': simple_dict_data['Shipment']['Recipient']['City'],
                        'Recipient.Country': simple_dict_data['Shipment']['Recipient']['Country'],
                        'Recipient.Phone': simple_dict_data['Shipment']['Recipient']['Phone'],
                        'Recipient.Vatcode': simple_dict_data['Shipment']['Recipient']['Vatcode'],
                        'Recipient.Email': simple_dict_data['Shipment']['Recipient']['Email'],
                    },
                    'Shipment.Consignment': {
                        'Consignment.Reference': simple_dict_data['Shipment']['Consignment']['Reference'],
                        'Consignment.Product': simple_dict_data['Shipment']['Consignment']['ProductCode'],
                        'Consignment.Contentcode': simple_dict_data['Shipment']['Consignment']['ContentCode'],
                        'Consignment.ReturnInstruction': simple_dict_data['Shipment']['Consignment'][
                            'ReturnInstruction'],
                        'Consignment.Invoicenumber': simple_dict_data['Shipment']['Consignment']['InvoiceNumber'],
                        'Consignment.Merchandisevalue': simple_dict_data['Shipment']['Consignment']['MerchandiseValue'],
                        'Consignment.Currency': simple_dict_data['Shipment']['Consignment']['Currency'],
                        'Consignment.AdditionalInfo': {
                            'AdditionalInfo.Text': simple_dict_data['Shipment']['Consignment']['AdditionalInfoText'],
                        },
                        'Consignment.AdditionalService': '',
                        'Consignment.Parcel': ''
                    }  # end Shipment.Consignment
                }  # end Shipment
            }  # end eChannel
        }

        _additional_services = self.generate_additional_services_data(
            simple_dict_data['Shipment']['Consignment']['AdditionalServices']
        )
        if _additional_services is not None and len(_additional_services) > 0:
            dict_data['eChannel']['Shipment']['Shipment.Consignment']['Consignment.AdditionalService'] \
                = _additional_services

        _parcel_services = self.generate_parcels_data(
            simple_dict_data['Shipment']['Consignment']['Parcels']
        )
        if _parcel_services is not None and len(_parcel_services) > 0:
            dict_data['eChannel']['Shipment']['Shipment.Consignment']['Consignment.Parcel'] = _parcel_services

        return dict_data

    def generate_additional_services_data(self, list_data=None):
        """
        Generate additional services data.

        :param list_data: list of dictionary of additional services
        :return list_data: list of formatted dictionary of additional services
        """
        if list_data is None:
            return None

        _var_type = type(list_data).__name__

        _return_list = []
        if _var_type == 'list':
            for dict_data in list_data:
                _return_list.append(self.get_one_additional_service_data(**dict_data))
        elif _var_type == 'dict':
            _return_list.append(self.get_one_additional_service_data(**list_data))
        else:
            raise ValueError("Unsupported data type")

        return _return_list

    def get_one_additional_service_data(self, **kwargs):
        """
        Generate one additional service data item.

        :param kwargs: contain following keys:
            ServiceCode: string of additional service code
            Specifier: list of dictionary or dictionary of service details. See get_one_specifier_data() function for\
                       input format
        :return dict_data: dictionary for one additional service
        """
        _return_dict = {
            'AdditionalService.ServiceCode': kwargs['ServiceCode'],
        }
        _specifiers = kwargs['Specifier']
        _data_type = type(_specifiers).__name__

        if _data_type == 'dict':
            _return_dict['AdditionalService.Specifier'] = self.get_one_specifier_data(**_specifiers)
        elif _data_type == 'list':
            _specifier_list = []
            for _a_dict_specifier in _specifiers:
                _specifier_list.append(self.get_one_specifier_data(**_a_dict_specifier))
            _return_dict['AdditionalService.Specifier'] = _specifier_list
        else:
            raise ValueError("Unsupported data type")
        return _return_dict

    def get_one_specifier_data(self, **kwargs):
        """
        Generate one specifier data item

        :param kwargs: contain following keys:
            name: attribute name for additional service
            value: attribute value
        :return dict_data: dictionary of one specifier
        """
        dict_data = {
            'name': kwargs['name'],
            'value': kwargs['value']
        }
        return dict_data

    def generate_parcels_data(self, list_data=None):
        """
        Generate parcels data.

        :param list_data: list of dictionary of parcels
        :return list_data: list of formatted dictionary of parcels
        """
        if list_data is None:
            return None

        _var_type = type(list_data).__name__

        _return_list = []
        if _var_type == 'list':
            for dict_data in list_data:
                _return_list.append(self.get_one_parcel_data(**dict_data))
        elif _var_type == 'dict':
            _return_list.append(self.get_one_parcel_data(**list_data))
        else:
            raise ValueError("Unsupported data type")

        return _return_list

    def get_one_parcel_data(self, **kwargs):
        """
        Generate one parcel data.

        :param kwargs: dictionary contain following keys:
            Reference: parcel reference
            PackageType: code of package type
            Weight: dictionary with 'weight_unit' and 'value' key.
            Volume: dictionary with 'unit' and 'value' key.
            InfoCode:
            Contents: product description
            ReturnService: return service code
            ContentLine: dictionary of parcel content data
            ParcelServices: parcel additional service (optional)
        :return dict_data: dictionary of parcel data
        """
        # print("Kwargs {}".format(kwargs))
        _parcel_data = {
            'Parcel.Reference': kwargs['Reference'],
            'Parcel.Packagetype': kwargs['PackageType'],
            'Parcel.Weight': {
                'weight_unit': kwargs['Weight']['weight_unit'],
                'value': kwargs['Weight']['value'],
            },
            'Parcel.Volume': {
                'unit': kwargs['Volume']['unit'],
                'value': kwargs['Volume']['value'],
            },
            'Parcel.Infocode': kwargs['InfoCode'],
            'Parcel.Contents': kwargs['Contents'],
            'Parcel.ReturnService': kwargs['ReturnService'],
            'Parcel.contentline': {},
            'Parcel.ParcelService': None
        }

        if kwargs['ContentLine'] is not None and len(kwargs['ContentLine']) > 0:
            _parcel_data['Parcel.contentline'] = {
                'contentline.description': kwargs['ContentLine']['description'],
                'contentline.quantity': kwargs['ContentLine']['quantity'],
                'contentline.currency': kwargs['ContentLine']['currency'],
                'contentline.netweight': kwargs['ContentLine']['netweight'],
                'contentline.value': kwargs['ContentLine']['value'],
                'contentline.countryoforigin': kwargs['ContentLine']['countryoforigin'],
                'contentline.tariffcode': kwargs['ContentLine']['tariffcode'],
            }

        if kwargs['ParcelServices'] is not None and len(kwargs['ParcelServices']) > 0:
            _parcel_services = []
            if type(kwargs['ParcelServices']).__name__ == 'dict':
                _parcel_services.append(self.get_one_parcel_service_data(**kwargs['ParcelServices']))
            elif type(kwargs['ParcelServices']).__name__ == 'list':
                for dict_data in kwargs['ParcelServices']:
                    _parcel_services.append(self.get_one_parcel_service_data(**dict_data))
            else:
                raise ValueError("Unsupported data type")
            _parcel_data['Parcel.ParcelService'] = _parcel_services

        return _parcel_data

    def get_one_parcel_service_data(self, **kwargs):
        """
        Generate one parcel service data.

        :param kwargs: dictionary of parcel service code, contain following key:
            ServiceCode: parcel service code - string
        :return dict_data: dictionary of one parcel service
        """
        dict_data = {
            'ServiceCode': kwargs['ServiceCode']
        }
        return dict_data

    def get_create_shipment_test_data(self):
        """
        Main function to generate test data set for create shipment request call.

        :return dict_data: dictionary of request data
        """
        routing_id = '1464524676'
        order_alias = 'ORDER001'

        dict_data = {
            'eChannel': {
                'ROUTING': {
                    'Routing.Account': self._api_key,
                    'Routing.Key': self.get_routing_key(routing_id),
                    'Routing.Id': routing_id,
                    'Routing.Name': order_alias,
                    'Routing.Time': datetime.now().strftime('%Y%m%d%H%M%S'),
                    # - Ignored parameters in Pakettikauppa
                    # 'Routing.Target' => { 'content' => '' },
                    # 'Routing.Source' => { 'content' => '' },
                    # 'Routing.Version'  => { 'content' => '' },
                    # 'Routing.Mode' => { 'content' => '' },
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
                        'Recipient.Name1': 'Receiver name',
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
                        'Consignment.Contentcode': 'D',  # Order->get('PR_ContentCode')
                        'Consignment.ReturnInstruction': 'E',  # Order->get('PR_ReturnInstruction')
                        # 'Consignment.ReturnInstruction': None,
                        'Consignment.Invoicenumber': order_alias,
                        'Consignment.Merchandisevalue': 150,  # Order->get('PR_Merchandisevalue')
                        'Consignment.Currency': 'EUR',
                        'Consignment.AdditionalInfo': {
                            # Order->get('PR_AdditionalInfoText')
                            'AdditionalInfo.Text': "Order no.: 1107-1 -- Reference no.: 284554"
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
                                # 'Parcel.ParcelService': [
                                #    {
                                #        'ParcelService.Servicecode': 'parcel service code'
                                #    },
                                #    {
                                #        'ParcelService.Servicecode': 'parcel service code 2'
                                #    },
                                # ]
                            },
                            {
                                'Parcel.Reference': '123457',
                                'Parcel.Packagetype': 'PC',
                                'Parcel.Weight': {'weight_unit': 'kg', 'value': '1.2'},
                                'Parcel.Volume': {'unit': 'm3', 'value': '0.6'},
                                'Parcel.Infocode': '1012',
                                'Parcel.Contents': 'Muttereita ja puita',  # product description
                                'Parcel.ReturnService': '123',
                                # Customs declaration info (for medicine)
                                'Parcel.contentline': {},
                                # 'Parcel.contentline': {
                                #    'contentline.description': 'Puita',
                                #    'contentline.quantity': 1,
                                #    'contentline.currency': 'EUR',
                                #    'contentline.netweight': 1,
                                #    'contentline.value': 100,
                                #    'contentline.countryoforigin': 'FI',
                                #    'contentline.tariffcode': '9608101000',
                                # },
                                # this is not really needed in Pakettikauppa but Prinetti
                                'Parcel.ParcelService': None
                            },
                        ]
                    }  # end Shipment.Consignment
                }  # end Shipment
            }  # end eChannel
        }

        return dict_data

    def validate_input_params_create_shipment(self, **kwargs):
        if len(kwargs) <= 0:
            raise KeyError("Require input parameters")

        self.mylogger.debug("Root input data = {}".format(kwargs))

        if 'eChannel' not in kwargs:
            raise KeyError("eChannel key is missing")

        self.validate_routing_data(**kwargs)

        if 'Shipment' not in kwargs['eChannel']:
            raise KeyError("Shipment key is missing")

        if 'Shipment.Sender' not in kwargs['eChannel']['Shipment']:
            raise KeyError("Missing Shipment.Sender key")

        if 'Sender.Name1' and 'Sender.Addr1' and 'Sender.Postcode' and 'Sender.City' and 'Sender.Country' \
                and 'Sender.Vatcode' and 'Sender.Email' not in kwargs['eChannel']['Shipment']['Shipment.Sender']:
            raise KeyError("Missing mandatory key in Shipment.Sender element")

        if 'Shipment.Recipient' not in kwargs['eChannel']['Shipment']:
            raise KeyError("Missing Shipment.Recipient key")

        if 'Recipient.Name1' and 'Recipient.Addr1' and 'Recipient.Postcode' and 'Recipient.City' \
                and 'Recipient.Country' and 'Recipient.Phone' and 'Recipient.Email' not in \
                kwargs['eChannel']['Shipment']['Shipment.Recipient']:
            raise KeyError("Missing mandatory key in Shipment.Recipient element")

        if 'Shipment.Consignment' not in kwargs['eChannel']['Shipment']:
            raise KeyError("Missing Shipment.Consignment key")

        if 'Consignment.Reference' and 'Consignment.Product' and 'Consignment.Contentcode' and \
                'Consignment.Invoicenumber' and 'Consignment.Currency' and 'Consignment.Parcel' not in \
                kwargs['eChannel']['Shipment']['Shipment.Consignment']:
            raise KeyError("Missing mandatory key in Shipment.Consignment element")

        return

    def validate_routing_data(self, **kwargs):
        if 'ROUTING' not in kwargs['eChannel']:
            raise KeyError("ROUTING key is missing")
        dict_routing = kwargs['eChannel']['ROUTING']
        if len(dict_routing) == 0:
            raise ValueError("Missing routing data")

        self.mylogger.debug("Data type for ROUTING key = " + type(dict_routing).__name__)
        if type(dict_routing).__name__ != 'dict':
            raise TypeError("Invalid data type for ROUTING key")

        if 'Routing.Account' and 'Routing.Id' and 'Routing.Key' and 'Routing.Name' and 'Routing.Time' not in \
                kwargs['eChannel']['ROUTING']:
            raise KeyError("Missing mandatory key in ROUTING element")
        return

    def get_xml_shipment_req_data(self, **kwargs):
        """
        Construct XML string of request data for create shipment API

        :param kwargs:

        Kwargs:
            eChannel: dictionary with following keys
                ROUTING: see _create_routing_elements() function

                Shipment: see _create_shipment_elements() function

        :return xml_string: string of XML request data for create shipment API
        """
        self.validate_input_params_create_shipment(**kwargs)

        root = ET.Element('eChannel')

        dict_routing = kwargs['eChannel']['ROUTING']
        self._create_routing_elements(root, **dict_routing)

        self._create_shipment_elements(root, **kwargs['eChannel']['Shipment'])

        # for Python2.7
        # tmp_string = ET.tostring(root).decode('utf-8')
        tmp_string = ET.tostring(root)
        xml_string = minidom.parseString(tmp_string).toprettyxml(indent="   ", encoding="utf-8")
        self.mylogger.debug("XML string = {}".format(xml_string))
        return xml_string

    def _create_routing_elements(self, root_element, **kwargs):
        """
        Append 'ROUTING' element to root

        :param root_element: XML root element object
        :param kwargs:

        Kwargs:
            Routing.Account: API key
            Routing.Id: string of routing ID, could be order id or shop id
            Routing.Name: string of routing name, could be order alias or shop alias or combination of shop alias and\
            order alias.
            Routing.Time: datetime string in following format '%Y%m%d%H%M%S'
        :return:
        """
        routing_root = ET.SubElement(root_element, "ROUTING")
        account_element = ET.SubElement(routing_root, "Routing.Account")
        account_element.text = str(kwargs['Routing.Account'])
        routing_id_element = ET.SubElement(routing_root, "Routing.Id")
        routing_id_element.text = str(kwargs['Routing.Id'])
        routing_key_element = ET.SubElement(routing_root, "Routing.Key")
        routing_key_element.text = self.get_md5_hash(self._api_key, self._secret, kwargs['Routing.Id'])
        routing_name_element = ET.SubElement(routing_root, "Routing.Name")
        routing_name_element.text = str(kwargs['Routing.Name'])
        routing_time_element = ET.SubElement(routing_root, "Routing.Time")
        routing_time_element.text = str(kwargs['Routing.Time'])

        return

    def _create_shipment_elements(self, root_element, **kwargs):
        """
        Append Shipment element to root element.

        :param root_element: root element object
        :param kwargs:

        Kwargs:
            Shipment.Recipient: recipient address information. See _create_shipment_address_element() function
            Shipment.Sender: sender address information. See _create_shipment_address_element() function
            Shipment.Consignment: consignment data. See _create_shipment_consignment_element() function

        :return:
        """
        shipment_root = ET.SubElement(root_element, "Shipment")
        self._create_shipment_address_element(shipment_root, "recipient", **kwargs['Shipment.Recipient'])
        self._create_shipment_address_element(shipment_root, "sender", **kwargs['Shipment.Sender'])

        self.logger.debug("[_create_shipment_elements] Shipment.Consignment={}".format(kwargs['Shipment.Consignment']))
        self._create_shipment_consignment_element(shipment_root, **kwargs['Shipment.Consignment'])

    def _create_shipment_address_element(self, root_element, address_type="recipient", **kwargs):
        """
        Append address element according to given address type

        :param root_element: root element for appending
        :param address_type: possible values: 'recipient' and 'sender'. Default value is 'recipient'
        :param kwargs:

        Kwargs for 'recipient' type:
            Recipient.Name1: recipient name
            Recipient.Name2:
            Recipient.Addr1: street address
            Recipient.Addr2:
            Recipient.Addr3:
            Recipient.Postcode: postal code
            Recipient.City: city name
            Recipient.Country: 2 letter of country code i.e. 'FI'
            Recipient.Phone: phone number
            Recipient.Vatcode: VAT code
            Recipient.Email: email address

        Kwargs for 'sender' type:
            Sender.Contractid: can leave it empty (not really in used)
            Sender.Name1: sender name
            Sender.Name2:
            Sender.Addr1: street address
            Sender.Addr2:
            Sender.Addr3:
            Sender.Postcode: postal code
            Sender.City: city name
            Sender.Country: 2 letter of country code i.e. 'FI'
            Sender.Phone: phone number
            Sender.Vatcode: VAT code
            Sender.Email: email address

        :return:
        """
        address_type = address_type.lower()
        accept_value = ('recipient', 'sender')
        if address_type not in accept_value:
            raise ValueError("Invalid value. Possible value are 'recipient' and 'sender'.")

        if address_type == "recipient":
            address_root_element = ET.SubElement(root_element, "Shipment.Recipient")
        else:
            address_root_element = ET.SubElement(root_element, "Shipment.Sender")

        for key in kwargs:
            if address_type == "recipient":
                if key not in self._accept_recipient_keys:
                    raise Exception(KeyError("Invalid key"))
            else:
                if key not in self._accept_sender_keys:
                    raise Exception(KeyError("Invalid key"))

            child = ET.SubElement(address_root_element, key)
            child.text = str(kwargs[key])

        return

    def _create_shipment_consignment_element(self, root_element, **kwargs):
        """
        Constructs consignment elements

        :param root_element: root xml element
        :param kwargs:

        Kwargs:
            Consignment.Currency: consignment currency code i.e. 'EUR'
            Consignment.Product: Posti's product code
            Consignment.Reference: consignment reference string
            Consignment.Invoicenumber: consignment invoice number string
            Consignment.AdditionalInfo: See create_additional_info_element() function
            Consignment.Contentcode: See _create_content_code_element() function
            Consignment.ReturnInstruction: See _create_return_instruction_element() function
            Consignment.Merchandisevalue: merchandise price value
            Consignment.AdditionalService: See _create_additional_service_elements() function
            Consignment.Parcel: See _create_one_consignment_parcel() function

        :return:
        """
        if kwargs is None:
            raise Exception(KeyError("Require parameters"))

        if len(kwargs) == 0:
            raise Exception(KeyError("Input parameter cann't be empty."))

        self.logger.debug("[_create_shipment_consignment_element] KWARGS={}".format(kwargs))

        root = ET.SubElement(root_element, "Shipment.Consignment")

        create_currency_element(root, kwargs['Consignment.Currency'])

        create_product_element(root, kwargs['Consignment.Product'])

        create_reference_element(root, kwargs['Consignment.Reference'])

        self._create_invoice_number_element(root, kwargs['Consignment.Invoicenumber'])

        create_additional_info_element(root, **kwargs['Consignment.AdditionalInfo'])

        self._create_content_code_element(root, kwargs['Consignment.Contentcode'])

        info_code_element = ET.SubElement(root, "Consignment.Infocode")
        info_code_element.text = ''

        self._create_return_instruction_element(root, kwargs['Consignment.ReturnInstruction'])

        # this is for aboard shipment when custom need to know value of products in the shipment
        create_merchandise_value_element(root, kwargs['Consignment.Merchandisevalue'])

        self._create_additional_service_elements(root, kwargs['Consignment.AdditionalService'])

        if type(kwargs['Consignment.Parcel']).__name__ == 'dict':
            self._create_one_consignment_parcel(root, **kwargs['Consignment.Parcel'])
        elif type(kwargs['Consignment.Parcel']).__name__ == 'list':
            if kwargs['Consignment.Parcel'] is None:
                return
            if len(kwargs['Consignment.Parcel']) == 0:
                return

            for one_dict_data in kwargs['Consignment.Parcel']:
                self._create_one_consignment_parcel(root, **one_dict_data)
        else:
            raise PakettikauppaException("Invalid argument type for 'Consignment.Parcel' key")

    def _create_additional_service_elements(self, root, list_services):
        """
        Append 'Consignment.AdditionalService' element and its children element to given root object.

        :param root: root XML element object
        :param list_services: list data of dictionary of additional services
        :return:
        """
        if list_services is None:
            return
        if len(list_services) == 0:
            return

        if type(list_services).__name__ != 'list':
            raise Exception(ValueError("Expected data type list"))

        for dict_data in list_services:
            additional_service_root_element = ET.SubElement(root, "Consignment.AdditionalService")
            self.mylogger.debug("Inner Hash= {}".format(dict_data))
            for key in dict_data:
                value_data_type = type(dict_data[key]).__name__
                # self.mylogger.debug("Key= {}, Value={}".format(key, dict_data[key]))
                self.mylogger.debug("[_create_additional_service_elements] Value data type={}".format(value_data_type))
                if value_data_type == 'dict':
                    if key == 'AdditionalService.Specifier':
                        self._create_one_service_specifier(additional_service_root_element, dict_data[key])
                    else:
                        child = ET.SubElement(additional_service_root_element, key)
                        for key2 in dict_data[key]:
                            # self.mylogger.debug("Key2={}, Value={}".format(key2, dict_data[key][key2]))
                            if key2 == 'value':
                                child.text = str(dict_data[key][key2])
                            else:
                                child.set(key2, str(dict_data[key][key2]))
                elif value_data_type == 'list':
                    # array case
                    for one_dict_data in dict_data[key]:
                        self._create_one_service_specifier(additional_service_root_element, one_dict_data)
                else:
                    # string case
                    if dict_data[key] is not None:
                        child = ET.SubElement(additional_service_root_element, key)
                        child.text = str(dict_data[key])

    def _create_one_service_specifier(self, additional_service_root_element, dict_data):
        """
        Append 'AdditionalService.Specifier' element to additional service root element.

        :param additional_service_root_element: additional service root element object
        :param dict_data: dictionary with 'name' and 'value' key. 'name' is for attribute in XML element. 'value' is\
                          for content of XML element.
        :return:
        """
        self.mylogger.debug("[_create_one_service_specifier] dict_data={}".format(dict_data))

        if dict_data is None:
            return
        if len(dict_data) == 0:
            return

        child = ET.SubElement(additional_service_root_element, 'AdditionalService.Specifier')
        for key in dict_data:
            if key == 'value':
                child.text = str(dict_data[key])
            else:
                child.set(key, str(dict_data[key]))

    def _create_invoice_number_element(self, root, value=None):
        """
        Create 'Consignment.Invoicenumber' element under given root object.

        :param root: root XML element object
        :param value: string of invoice number
        :return:
        """
        self.logger.debug("Invoice number value={}".format(value))
        if value is None:
            value = ''
        invoice_number_element = ET.SubElement(root, "Consignment.Invoicenumber")
        invoice_number_element.text = str(value)

    def _create_content_code_element(self, root, value):
        """
        Append 'Consignment.Contentcode' element to given root object.

        :param root: root XML element object
        :param value: string of content code
        :return:
        """
        if value is None or value == '':
            raise PakettikauppaException("Require Consignment.Contentcode value")
        else:
            value = str(value)
            self._validate_content_code_value(value)

        content_element = ET.SubElement(root, "Consignment.Contentcode")
        content_element.text = value

    def _validate_content_code_value(self, code):
        """
        Validate given content code and raise error if the value is invalid.

        :param code: 1 letter of content code. Possible values:'D', 'E', 'G', 'M' and 'S'
        :return:
        """
        if code not in self._content_codes:
            raise PakettikauppaException("Invalid content code. Possible values:'D', 'E', 'G', 'M' and 'S'")

    def _create_return_instruction_element(self, root, value=''):
        """
        Append 'Consignment.ReturnInstruction' element to given root object
        :param root: root XML element object
        :param value: a letter of return instruction code. Possible value are 'E', 'H' and 'L'
        :return:
        """
        if value != '':
            self._validate_return_instruction_code(value)

        return_instruction_element = ET.SubElement(root, "Consignment.ReturnInstruction")
        return_instruction_element.text = str(value)

    def _validate_return_instruction_code(self, code):
        """
        Validate given return instruction code. Raise exception if given code is invalid.

        :param code: a letter of return instruction code. Possible value are 'E', 'H' and 'L'
        :return:
        """
        if code not in self._return_instruction_codes:
            raise PakettikauppaException("Invalid return instruction code. Possible value are 'E', 'H' and 'L'")

    def _create_one_consignment_parcel(self, root, **kwargs):
        """
        Append 'Consignment.Parcel' element and its children element to given root object

        :param root: root XML element object
        :param kwargs: See _create_parcel_elements() function
        :return:
        """
        if kwargs is None:
            return
        if len(kwargs) == 0:
            return

        parcel_root_element = ET.SubElement(root, "Consignment.Parcel")
        parcel_root_element.set("type", "normal")
        self._create_parcel_elements(parcel_root_element, **kwargs)

    def _create_parcel_elements(self, parcel_root_element, **kwargs):
        """
        Append child elements to 'Consignment.Parcel' element.

        :param parcel_root_element: parcel root element object.
        :param kwargs:
        Kwargs:
            Parcel.contentline: See _create_content_line_elements() function
            Parcel.ParcelService: See _create_parcel_service_elements() function
            Parcel.Weight: dictionary of weight data with 'weight_unit' and 'value' key.
            Parcel.Volume: dictionary of volume data with 'unit' and 'value' key
            Parcel.Reference: parcel reference
            Parcel.Packagetype: code of package type. See _validate_package_type() for code details.
            Parcel.Infocode:
            Parcel.Contents: product description
            Parcel.ReturnService:
        :return:
        """
        parcel_reference_element = ET.SubElement(parcel_root_element, "Parcel.Reference")
        parcel_reference_element.text = None

        # self.mylogger.debug("Hash input for creating Parcel elements={}".format(kwargs))
        for key in kwargs:
            if key not in self._accept_parcel_keys:
                raise Exception(KeyError("Invalid key parameter"))

            if key == 'Parcel.contentline':
                self._create_content_line_elements(parcel_root_element, **kwargs[key])
            elif key == 'Parcel.ParcelService':
                _create_parcel_service_elements(parcel_root_element, kwargs[key])
            elif key == 'Parcel.Weight':
                if kwargs[key]['weight_unit'] is None or kwargs[key]['weight_unit'] == '':
                    raise PakettikauppaException("Expect value in weight_unit parameter")
                if kwargs[key]['value'] is None or kwargs[key]['value'] == '':
                    raise PakettikauppaException("Require parcel weight in 'value' parameter")

                child = ET.SubElement(parcel_root_element, key)
                child.set("unit", kwargs[key]['weight_unit'])
                child.text = str(kwargs[key]['value'])
            elif key == 'Parcel.Volume':
                volume_unit = kwargs[key]['unit']
                if kwargs[key]['unit'] is None or kwargs[key]['unit'] == '':
                    volume_unit = 'm3'
                if kwargs[key]['value'] is None or kwargs[key]['value'] == '':
                    raise PakettikauppaException("Require parcel volume in 'value' parameter")

                child = ET.SubElement(parcel_root_element, key)
                child.set("unit", str(volume_unit))
                child.text = str(kwargs[key]['value'])
            else:
                # expected string value from kwargs[key]
                # self.mylogger.debug("Key for creating Parcel elements={}, Value={}".format(key, kwargs[key]))
                if type(kwargs[key]).__name__ != 'str':
                    raise PakettikauppaException("Invalid value in key={}".format(key))

                if key == 'Parcel.Packagetype':
                    if kwargs[key] is None or kwargs[key] == '':
                        kwargs[key] = 'PC'
                    self._validate_package_type(kwargs[key])

                child = ET.SubElement(parcel_root_element, key)
                child.text = str(kwargs[key])

    def _validate_package_type(self, code=None):
        """
        Validate package type code. Raise exception if code is invalid.

        :param code: string of package type code
        :return:
        """
        if code not in self._package_types:
            raise PakettikauppaException("Invalid package type code")

    def _create_content_line_elements(self, parcel_root_element, **kwargs):
        self.mylogger.debug("[_create_content_line_elements]Length of data={}".format(len(kwargs)))
        if kwargs is None:
            return

        if len(kwargs) == 0:
            return

        root = ET.SubElement(parcel_root_element, "Parcel.contentline")
        for key in kwargs:
            child = ET.SubElement(root, key)
            child.text = str(kwargs[key])

    # Not yet getting expected result in Test server
    def get_shipment_status(self, tracking_code):
        """
        Get shipment status from Pakettikauppa.

        :param tracking_code: string of tracking code for checking
        :return:
        """
        _api_config = self.get_api_config('get_shipment_status')
        dict_req_data = self.get_shipment_status_req_data(tracking_code)
        res_obj = super(PkMerchant, self).send_request('POST', _api_config['api_post_url'], dict_req_data)
        self.logger.debug("[GetShipment] Response={}".format(res_obj.text))
        return

    def get_shipment_status_req_data(self, tracking_code):
        """
        Construct request data for get shipment status API.

        :param tracking_code: string of tracking code
        :return dict_data: dictionary of request data
        """
        if tracking_code is None or tracking_code == '':
            raise Exception(KeyError("Require tracking code string"))

        dict_req_data = {
            'api_key': self._api_key,
            'tracking_code': str(tracking_code),
            'timestamp': str(int(time())),
            # 'timestamp': '1512575546',
        }

        # Calculate MAC
        digest_string = self.get_hash_sha256(self._secret, **dict_req_data)
        dict_req_data['hash'] = digest_string
        self.mylogger.debug("Hash data for shipment status= {}".format(dict_req_data))
        return dict_req_data

    def get_shipping_label(self, **kwargs):
        """
        Get shipping labels from Pakettikauppa. This API send request data in XML format.

        :param kwargs: See get_xml_shipping_label_req_data() function
        :return: See parse_xml_get_shipping_label_res() function
        """
        _api_config = self.get_api_config('get_shipping_label')

        if self._isInTestMode:
            if kwargs is not None:
                xml_req_data = self.get_xml_shipping_label_req_data(**kwargs)
            else:
                dict_data = self.get_shipping_label_req_test_data()
                xml_req_data = self.get_xml_shipping_label_req_data(**dict_data)
        else:
            xml_req_data = self.get_xml_shipping_label_req_data(**kwargs)

        headers = {
            'Content-Encoding': 'utf-8',
            'Content-Type': 'application/xml'
        }

        res_obj = super(PkMerchant, self).send_request('POST', _api_config['api_post_url'], xml_req_data, **headers)

        xml_res_string = res_obj.text
        self.mylogger.debug("Response XML string = {}".format(xml_res_string))

        return self.parse_xml_get_shipping_label_res(xml_res_string)

    def parse_xml_get_shipping_label_res(self, xml_string):
        """
        Construct dictionary from response data.

        :param xml_string: XML string of response data
        :return: dict_data: dictionary, contains below keys
            status (integer): 1 = operation OK
            message (string): response message
            PDFcontent (string): binary data of PDF content
            ContentEncoded (boolean): True = PDFContent data is encoded
        """
        if xml_string is None or xml_string == '':
            self.mylogger.error("No XML string pass to the function")
            return None

        root = ET.fromstring(xml_string)
        status_element = root.find("response.status")
        status = str(status_element.text)
        self.mylogger.debug("Response status from Pakettikauppa = {}".format(status))
        message_element = root.find("response.message")

        pdf_content_element = root.find("response.file")
        if pdf_content_element is not None:
            encoded_pdf_content = pdf_content_element.text
            # self.mylogger.debug("PDF content= {}".format(encoded_pdf_content))

            # Pakettikauppa return status=0 means OK
            if status == '0':
                dict_data = {
                    'status': 1,
                    'message': message_element.text,
                    'PDFcontent': encoded_pdf_content,
                    'ContentEncoded': True,
                }
            else:
                dict_data = {
                    'status': 0,
                    'message': message_element.text,
                    'PDFcontent': encoded_pdf_content,
                    'ContentEncoded': True,
                }

            self.mylogger.debug("Return dict data= {}".format(dict_data))
            return dict_data
        else:
            self.logger.error("Unable to find PDF content from response")
            return {
                'status': 0,
                'message': 'Unable to find PDF content from response data',
                'PDFcontent': None,
                'ContentEncoded': False,
            }

    def get_shipping_label_req_test_data(self):
        """
        Generate test request data for getting shipping label.

        :return dict_data: dictionary
        """
        routing_id = '1479035179'
        order_alias = 'ORDER001'

        dict_data = {
            'eChannel': {
                'ROUTING': {
                    'Routing.Account': self._api_key,
                    'Routing.Key': self.get_routing_key(routing_id),
                    'Routing.Id': routing_id,
                    'Routing.Name': order_alias,
                    'Routing.Time': datetime.now().strftime('%Y%m%d%H%M%S'),
                    # - Ignored parameters in Pakettikauppa
                    # 'Routing.Target' => { 'content' => '' },
                    # 'Routing.Source' => { 'content' => '' },
                    # 'Routing.Version'  => { 'content' => '' },
                    # 'Routing.Mode' => { 'content' => '' },
                },
                'PrintLabel': {
                    'responseFormat': "File",  # "File" and "inline" are supported. "File" is default
                    'content': {
                        # Send request for multiple shipping labels
                        # this is for test credential
                        'TrackingCode': [
                            {
                                'Code': 'JJFITESTLABEL601'
                            },
                            {
                                'Code': 'JJFITESTLABEL602'
                            },
                        ]
                        #
                        # or use this way to send a request for one shipping label
                        # This is for Vilkas API key
                        # 'TrackingCode': {
                        #    'Code': 'JJFITESTLABEL1332'
                        # }
                    }
                }
            }
        }

        return dict_data

    def get_xml_shipping_label_req_data(self, **kwargs):
        """
        Construct XML string request data for getting shipping label

        :param kwargs: contains following keys

            eChannel: contains following keys
                ROUTING: dictionary of routing data
                PrintLabel: dictionary of tracking codes

            ROUTING:
                Routing.Account: API key
                Routing.Key: MD5 hash string
                Routing.Id: could be order id or shop id or combination of both
                Routing.Name: could be order alias or shop alias or combination of both
                Routing.Time: string of current datetime with following format '%Y%m%d%H%M%S'

            PrintLabel:
                responseFormat: expected response data format. Possible values are "File" and "inline", \
                                "File" is default.
                content: dictionary of tracking code with 'TrackingCode' as a key.

            TrackingCode: could be dictionary with 'Code' key or list of dictionary of 'Code' key for asking \
                          multiple labels
                Code: string of tracking code

        :return xml_string:
        """
        if kwargs is None:
            raise Exception(KeyError("Expect input parameters"))
        if len(kwargs) == 0:
            raise Exception(KeyError("Expect input parameters"))

        if 'eChannel' not in kwargs:
            raise KeyError("eChannel key is missing")

        self.validate_routing_data(**kwargs)

        # self.logger.debug("[GetXmlShippingLabel] KWARGS={}".format(kwargs))
        root = ET.Element('eChannel')

        dict_routing = kwargs['eChannel']['ROUTING']
        self._create_routing_elements(root, **dict_routing)

        if 'PrintLabel' not in kwargs['eChannel']:
            raise KeyError("Missing PrintLabel key")
        self._create_print_label_element(root, **kwargs['eChannel']['PrintLabel'])

        xml_string = minidom.parseString(ET.tostring(root)).toprettyxml(indent="   ", encoding="utf-8")
        # print(repr(xml_string))
        self.mylogger.debug("XML string = {}".format(xml_string))

        return xml_string

    def _create_print_label_element(self, root, **dict_data):
        """
        Append 'PrintLabel' element and its child elements to given root object.

        :param root: root XML object
        :param dict_data: dictionary of tracking codes
        :return:
        """
        if dict_data is None or len(dict_data) == 0:
            raise KeyError("Missing data in PrintLabel key")

        if 'responseFormat' not in dict_data:
            raise KeyError("Missing responseFormat -key")

        if dict_data['responseFormat'] is None or dict_data['responseFormat'] == '':
            raise ValueError("Invalid value for responseFormat key")

        _accept_value = ('File', 'inline')
        if dict_data['responseFormat'] not in _accept_value:
            raise ValueError("Invalid value for responseFormat key")

        if 'content' not in dict_data:
            raise KeyError("Missing content -key")

        if 'TrackingCode' not in dict_data['content']:
            raise KeyError("Missing TrackingCode -key")

        self.logger.debug("[CreatePrintLabelElement] Dict data={}".format(dict_data))
        print_label_element = ET.SubElement(root, "PrintLabel")
        for key in dict_data:
            if key != 'content':
                print_label_element.set(key, dict_data[key])
            else:
                child_dict = dict_data[key]
                self._create_child_print_label_element(print_label_element, **child_dict)

    def _create_child_print_label_element(self, print_label_element, **child_dict):
        """
        Append child element to 'PrintLabel' element object.

        :param print_label_element: print label root element object
        :param child_dict: dictionary of tracking codes
        :return:
        """
        for key in child_dict:
            value_type = type(child_dict[key]).__name__
            if value_type == 'str':
                child = ET.SubElement(print_label_element, key)
                child.text = child_dict[key]
            else:
                if key == 'TrackingCode':
                    if value_type == 'list':
                        self.logger.debug("Child dict:{}".format(child_dict[key]))
                        for dict_code in child_dict[key]:
                            self.logger.debug("dict_code={}".format(dict_code))
                            _create_one_tracking_code_element(print_label_element, dict_code['Code'])
                    else:
                        # Hash data type
                        _create_one_tracking_code_element(print_label_element, child_dict[key]['Code'])
                else:
                    raise PakettikauppaException("Unexpected key for creating child element of PrintLabel")


def create_additional_info_element(root, **dict_data):
    """
    Append additional info element to given root object.
    :param root: root XML object.
    :param dict_data: dictionary of additional info text
    :return:
    """
    if dict_data is None:
        return None
    if len(dict_data) == 0:
        return None

    text_value = dict_data['AdditionalInfo.Text']
    if text_value is None:
        return None
    if type(text_value).__name__ != 'str':
        raise PakettikauppaException("Expect string value in 'AdditionalInfo.Text' parameter")

    additional_info_root_element = ET.SubElement(root, "Consignment.AdditionalInfo")
    additional_info_element = ET.SubElement(additional_info_root_element, "AdditionalInfo.Text")
    additional_info_element.text = str(text_value)


def create_reference_element(root, value=None):
    """
    Append 'Consignment.Reference' element to given root object.

    :param root: root XML object
    :param value: string of reference number
    :return:
    """
    if value is None:
        value = ''
    reference_element = ET.SubElement(root, "Consignment.Reference")
    reference_element.text = str(value)


def create_product_element(root, product_code):
    """
    Append 'Consignment.Product' element to given root object.

    :param root: root XML object
    :param product_code: string of Posti's product code
    :return:
    """
    if product_code is None or product_code == '':
        raise PakettikauppaException("Require product code in 'Consignment.Product'")

    product_element = ET.SubElement(root, "Consignment.Product")
    product_element.text = str(product_code)


def create_merchandise_value_element(root, value=None):
    """
    Append 'Consignment.Merchandisevalue' element to given root object.

    :param root: root XML element object
    :param value: string of merchandise value
    :return:
    """
    merchandise_value_element = ET.SubElement(root, "Consignment.Merchandisevalue")
    if value is None:
        merchandise_value_element.text = ''
    else:
        merchandise_value_element.text = str(value)


def create_currency_element(root, value=None):
    """
    Append 'Consignment.Currency' element to given root object.

    :param root: root XML element object
    :param value: string of currency code i.e. 'EUR'
    :return:
    """
    if value is None:
        value = 'EUR'
    else:
        value = value.upper()
    currency_element = ET.SubElement(root, "Consignment.Currency")
    currency_element.text = str(value)


def _create_one_tracking_code_element(root, tracking_code):
    """
    Append 'TrackingCode' element to given root object.

    :param root: root XML element object
    :param tracking_code: string of tracking code
    :return:
    """
    child = ET.SubElement(root, "TrackingCode")
    child.text = str(tracking_code)


def _create_parcel_service_elements(root, list_services):
    """
    Append 'Parcel.ParcelService' element to given root object.

    :param root: root XML element object
    :param list_services:  list data of parcel services
    :return:
    """
    if list_services is None:
        return

    if len(list_services) == 0:
        return
    else:
        for dict_data in list_services:
            parcel_service_root_element = ET.SubElement(root, "Parcel.ParcelService")
            for key in dict_data:
                child = ET.SubElement(parcel_service_root_element, key)
                child.text = str(dict_data[key])
