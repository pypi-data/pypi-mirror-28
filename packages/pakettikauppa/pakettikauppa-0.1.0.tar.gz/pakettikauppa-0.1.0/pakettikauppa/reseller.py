"""This is a module for Pakettikauppa integration for resellers to use

The module provides below functionality:
    1. Create customer
    2. Update customer
    3. Get list of customer
    4. De-activate customer

"""
from __future__ import absolute_import

__version__ = '0.1'
__author__ = 'Porntip Chaibamrung'

import re
import logging
from time import time
from .pakettikauppa import Pakettikauppa, PakettikauppaException, check_api_name


class PkReseller(Pakettikauppa):
    """
    Pakettikauppa reseller class is mean for reseller.

    """
    _api_key = None
    _secret = None
    _isInTestMode = 1

    _api_mapping = {
        'create_customer': '/customer/create',
        'update_customer': '/customer/update',
        'list_customer': '/customer/list',
        'deactivate_customer': '/customer/deactivate'
    }

    accept_payment_service_provider = ('CHECKOUT', 'CREDIT_CARD')

    _accepted_keys = ('name', 'business_id', 'payment_service_provider', 'psp_merchant_id', 'marketing_name',
                      'street_address', 'post_office', 'postcode', 'country', 'phone', 'email',
                      'contact_person_name', 'contact_person_phone', 'contact_person_email',
                      'customer_service_phone', 'customer_service_email'
                      )
    _all_accepted_keys_length = len(_accepted_keys)

    def __init__(self, is_test_mode=0, api_key=None, secret=None):
        """
        Constructor for Pakettikauppa reseller class. Initial API and secret key included logger.
        :param is_test_mode: integer value to identify test mode. Zero is default value. If you set '1' to the \
                             parameter, you may skip passing API key and secret key
        :param api_key: API key string
        :param secret: secret key string
        """
        self._isInTestMode = is_test_mode

        # super().__init__(self._isInTestMode) # for Python3 only
        super(PkReseller, self).__init__(self._isInTestMode)

        self.mylogger = logging.getLogger(__name__)

        if self._isInTestMode == 1:
            if api_key is None or api_key == '':
                self._api_key = '11111111-1111-1111-1111-111111111111'
            else:
                self._api_key = api_key

            if secret is None or secret == '':
                self._secret = 'FEDCBA0987654321'
            else:
                self._secret = secret
        else:
            if api_key is None or api_key == '':
                raise PakettikauppaException("Missing API key")
            else:
                self._api_key = api_key
            if secret is None or secret == '':
                raise PakettikauppaException("Missing API secret key")
            else:
                self._secret = secret

    @check_api_name
    def get_api_suffix(self, api_name=None):
        """
        Get API suffix for given API name.

        :param api_name: string of API name
        :return api_suffix: string of API suffix
        """
        if api_name in self._api_mapping:
            retval = str(self._api_mapping[api_name])
            self.mylogger.debug("Api suffix: {}".format(retval))
            return retval
        else:
            raise PakettikauppaException("Invalid API name. Possible value are 'create_customer', 'update_customer',\
             'list_customer' and 'deactivate_customer'")

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
        _api_post_url = super(PkReseller, self).get_post_url(_api_suffix)
        _api_config = {
            'api_post_url': _api_post_url,
            'api_key': self._api_key,
            'api_secret': self._secret
        }
        return _api_config

    def clean_up_phone_data(self, phone_string=None):
        """
        Remove none-digit data from phone number.

        :param phone_string: string of phone number
        :return:
        """
        if phone_string is None or phone_string == '':
            return ''
        else:
            phone_string = str(phone_string)
            # self.mylogger.debug("Original phone string={}".format(phone_string))

            formatted_string = re.sub('\D', '', phone_string)
            self.mylogger.debug("[clean_up_phone_data] Formatted phone={}".format(formatted_string))
            return formatted_string

    def get_customer_list(self):
        """
        Get list of customer for your account.

        :return list_data: list of response data
        """
        _api_config = self.get_api_config('list_customer')

        input_req_data = {
            'api_key': self._api_key,
            'timestamp': str(int(time())),
        }

        # Calculate MAC
        digest_string = self.get_hash_sha256(self._secret, **input_req_data)
        input_req_data['hash'] = digest_string
        self.mylogger.debug("Hash input data={}".format(input_req_data))

        res_obj = super(PkReseller, self).send_request('POST', _api_config['api_post_url'], input_req_data)
        return self.parse_res_to_list(res_obj)

    def create_customer(self, **kwargs):
        """
        Create customer in Pakettikauppa's system.

        :param kwargs: See get_create_customer_req_data() function
        :return list_data: list of response data
        """
        h_config = self.get_api_config('create_customer')

        _hInputData = self.get_create_customer_req_data(**kwargs)

        res_obj = super(PkReseller, self).send_request('POST', h_config['api_post_url'], _hInputData)

        return self.parse_res_to_list(res_obj)

    def get_create_customer_req_data(self, **kwargs):
        """
        Construct request data for create customer API.

        :param kwargs: contains following key
            name: customer name
            business_id: VAT ID
            payment_service_provider: possible values are 'CHECKOUT' and 'CREDIT_CARD', can be empty string
            psp_merchant_id: Required if payment_service_provider is CHECKOUT. Value is merchant id in the \
                             Checkout service.
            marketing_name: optional field
            street_address: street address
            post_office: city name
            postcode: postal code
            country: country name
            phone: phone number
            email: email address
            contact_person_name: contact person name
            contact_person_phone: contact person phone number
            contact_person_email: contact person email address
            customer_service_phone: customer service phone number
            customer_service_email: customer service email address

        :return dict_data: dictionary of request data
        """
        if kwargs is None:
            raise PakettikauppaException("Require input parameters")

        key_length = len(kwargs)
        self.logger.debug("Kwargs length={}".format(key_length))

        if key_length == 0:
            raise KeyError("Require input parameters")

        _mandatory_keys = ('name', 'business_id', 'street_address', 'post_office', 'postcode', 'country', 'phone',
                           'email', 'contact_person_name', 'contact_person_phone', 'contact_person_email')
        mandatory_key_length = len(_mandatory_keys)

        self.logger.debug("Mandatory key length={}".format(mandatory_key_length))
        if key_length != self._all_accepted_keys_length:
            raise KeyError("Too short parameter")

        for key in kwargs:
            if key not in self._accepted_keys:
                raise KeyError("Invalid key")
            else:
                if key in _mandatory_keys:
                    if kwargs[key] is None or kwargs[key] == '':
                        raise ValueError("Mandatory field data is missing")

        payment_service_provider = kwargs['payment_service_provider']
        checkout_account_id = kwargs['psp_merchant_id']
        if payment_service_provider is not None and payment_service_provider != '':
            if payment_service_provider not in self.accept_payment_service_provider:
                raise ValueError("Invalid payment service provider option")
            else:
                if checkout_account_id is None or checkout_account_id == '':
                    raise ValueError("Require checkout account id")

        _hInputData = {
            'api_key': self._api_key,
            'name': kwargs['name'],
            'business_id': kwargs['business_id'],
            'payment_service_provider': payment_service_provider,
            'psp_merchant_id': checkout_account_id,
            'marketing_name': kwargs['marketing_name'],
            'street_address': kwargs['street_address'],
            'post_office': kwargs['post_office'],
            'postcode': kwargs['postcode'],
            'country': kwargs['country'],
            'phone': self.clean_up_phone_data(kwargs['phone']),
            'email': kwargs['email'],
            'contact_person_name': kwargs['contact_person_name'],
            'contact_person_phone': self.clean_up_phone_data(kwargs['contact_person_phone']),
            'contact_person_email': kwargs['contact_person_email'],
            'customer_service_phone': self.clean_up_phone_data(kwargs['customer_service_phone']),
            'customer_service_email': kwargs['customer_service_email'],
        }

        # Calculate MAC
        digest_string = self.get_hash_sha256(self._secret, **_hInputData)
        _hInputData['hash'] = digest_string
        self.mylogger.debug("Hash input data={}".format(_hInputData))

        return _hInputData

    def update_customer(self, customer_id=None, **kwargs):
        """
        Update customer details in Pakettikauppa's system.

        :param customer_id: Pakettikauppa's customer id
        :param kwargs: attributes that you wish to update. See possible keys from get_create_customer_req_data()
        :return:
        """
        if customer_id is None:
            raise PakettikauppaException("Customer id is empty")

        customer_id = str(customer_id)
        if customer_id == '':
            raise PakettikauppaException("Customer id is empty")

        length_arguments = len(kwargs)
        self.mylogger.debug("Length of input params={}".format(length_arguments))

        if kwargs is None or len(kwargs) == 0:
            return

        self.mylogger.debug("Updating customer id={}".format(customer_id))

        _api_config = self.get_api_config('update_customer')

        update_req_data = self.get_update_customer_req_data(customer_id, **kwargs)

        if update_req_data is None:
            self.mylogger.debug("No update request data found")
            return None
        else:
            res_obj = super(PkReseller, self).send_request('POST', _api_config['api_post_url'], update_req_data)
            return self.parse_res_to_list(res_obj)

    def get_update_customer_req_data(self, customer_id, **kwargs):
        """
        Construct request data for updating customer details.

        :param customer_id: Pakettikauppa's customer id
        :param kwargs: attributes that you wish to update. See possible keys from get_create_customer_req_data()
        :return dict_data: dictionary of request data
        """
        update_req_data = {
            'api_key': self._api_key,
            'customer_id': customer_id,
        }

        for key in kwargs:
            if key in self._accepted_keys:
                item_value = kwargs[key]
                if item_value is not None and item_value != '':
                    update_req_data[key] = item_value
                else:
                    continue
            else:
                raise PakettikauppaException("Invalid input key parameter")

        # Calculate MAC
        digest_string = self.get_hash_sha256(self._secret, **update_req_data)
        update_req_data['hash'] = digest_string
        self.mylogger.debug("Hash update input data={}".format(update_req_data))

        return update_req_data

    def deactivate_customer(self, customer_id):
        """
        De-activate customer account in Pakettikauppa's system.

        :param customer_id: Pakettikauppa's customer id
        :return list_data: list of response data
        """
        if customer_id is None:
            raise ValueError("Require customer id")

        customer_id = str(customer_id)
        if customer_id == '':
            raise ValueError("Require customer id")

        self.mylogger.debug("De-activating customer id={}".format(customer_id))

        _api_config = self.get_api_config('deactivate_customer')

        input_req_data = {
            'api_key': self._api_key,
            'customer_id': customer_id,
            'timestamp': str(int(time())),
        }

        # Calculate MAC
        digest_string = self.get_hash_sha256(self._secret, **input_req_data)
        input_req_data['hash'] = digest_string
        self.mylogger.debug("Hash de-activate input data={}".format(input_req_data))

        res_obj = super(PkReseller, self).send_request('POST', _api_config['api_post_url'], input_req_data)
        return self.parse_res_to_list(res_obj)
