"""Pakettikauppa app

This module provides base functionality for Pakettikauppa integration

"""
__version__ = '0.1'
__author__ = 'Porntip Chaibamrung'

import hashlib
import hmac
import requests
import logging
import sys
from functools import wraps


def check_api_name(in_function):
    """
    Validate API name
    :type in_function: input function
    """
    @wraps(in_function)
    def decorated_function(self, param):
        if param is None or param == '':
            raise PakettikauppaException("API name", "Missing API name")

        self.logger.debug("API name variable type={}".format(type(param).__name__))
        if str(type(param).__name__) != 'str':
            raise PakettikauppaException(param, "Invalid parameter type")
        else:
            return in_function(self, param)

    # or use this line => return wraps(function)(decorated_function)
    return decorated_function


class PakettikauppaException(Exception):
    pass


class Pakettikauppa(object):
    """
    Base class for Pakettikauppa integration.

    """
    _base_api_end_point = None
    logger = None

    def __init__(self, is_test_mode=0):
        """
        Constructor for Pakettikauppa class. Initial base API end point and logger object

        :param is_test_mode: integer value to identify test mode
        """
        logging.basicConfig(
            #    filename="pakettikauppa.log",
            #    format="%(asctime)s:%(levelname)s:%(message)s",
            level=logging.DEBUG,
        )
        self.set_logger()

        if is_test_mode == 1:
            self._base_api_end_point = 'https://apitest.pakettikauppa.fi'
        else:
            self._base_api_end_point = 'https://api.pakettikauppa.fi'

    def set_logger(self):
        """
        Set logger object.

        :return:
        """
        self.logger = logging.getLogger(__name__)

    def get_logger(self):
        """
        Get logger object.

        :return:
        """
        return self.logger

    def get_post_url(self, api_suffix=None):
        """
        Get API post URL address

        :param api_suffix: string of API suffix

        :return api_post_url (string): Post URL
        """
        if api_suffix is None:
            raise PakettikauppaException("Missing API suffix")

        _api_post_url = self._base_api_end_point + api_suffix
        return _api_post_url

    def get_api_end_point(self):
        """
        Get API base end point string

        :return base_end_point: API base end point string
        """
        return self._base_api_end_point

    def get_hash_sha256(self, secret_key, **kwargs):
        """
        Calculate SHA256 digest string.

        :param secret_key: string of secret key
        :param kwargs: dictionary of parameters for caluclation
        :return digest_string: digest string
        """
        if kwargs is None or len(kwargs) == 0:
            raise Exception(KeyError("Expect input parameters"))

        secret_key = str(secret_key)
        self.logger.debug("Secret key: {}".format(secret_key))

        my_lst = []
        for key in sorted(kwargs):
            self.logger.debug("Key={}, Value={}".format(key, kwargs[key]))
            my_lst.append(str(kwargs[key]))
        plain_text = '&'.join(map(str, my_lst))
        self.logger.debug("Plain text={}".format(plain_text))

        if sys.version_info < (3, 0):
            message_bytes = bytes(plain_text)
            secret_bytes = bytes(secret_key)
        else:
            message_bytes = bytes(plain_text, 'utf-8')
            secret_bytes = bytes(secret_key, 'utf-8')

        hash_string = hmac.new(secret_bytes, message_bytes, hashlib.sha256)

        # to lowercase hexits
        digest_string = hash_string.hexdigest()
        self.logger.debug("Digest string={}".format(digest_string))
        return str(digest_string)

    def get_md5_hash(self, api_key=None, secret_key=None, routing_id=None):
        """
        Calculate MD5 digest string.

        :param api_key: string of API key
        :param secret_key: string of secret key
        :param routing_id: string of routing id
        :return digest_string: digest string
        """
        if api_key is None or api_key == '':
            raise Exception(ValueError("Need API key parameter"))

        if secret_key is None or secret_key == '':
            raise Exception(ValueError("Need Secret key parameter"))

        if routing_id is None or routing_id == '':
            raise Exception(ValueError("Need routing id parameter"))

        routing_key_data = str(api_key) + str(routing_id) + str(secret_key)
        self.logger.debug("Routing key data={}".format(routing_key_data))
        digest_string = hashlib.md5(routing_key_data.encode('utf-8')).hexdigest()
        self.logger.debug("MD5 Digest string={}".format(digest_string))
        return digest_string

    def send_request(self, send_method='POST', _api_post_url=None, req_input=None, **headers):
        """
        Send a request to Pakettikauppa.

        :param send_method: type of request method. Possible value are 'POST' and 'GET', 'POST' is default value.
        :param _api_post_url: string of post URL
        :param req_input: request input data
        :param headers: dictionary of header data
        :return res_obj: response object
        """
        if _api_post_url is None or _api_post_url == '':
            raise Exception(ValueError("Need post URL data"))

        if headers is None:
            headers = {
                # 'Content-type': 'application/x-www-form-urlencoded;charset=utf-8',
                'Content-Encoding': 'utf-8'
            }

        if send_method == 'POST':
            if req_input is None:
                res_obj = requests.post(_api_post_url, headers=headers)
            else:
                res_obj = requests.post(_api_post_url, data=req_input, headers=headers)

        else:
            if req_input is None:
                res_obj = requests.get(_api_post_url, headers=headers)
            else:
                res_obj = requests.get(_api_post_url, headers=headers, data=req_input, params=req_input)

        # self.logger.debug("Request headers={}".format(res_obj.request.headers))

        # Response data object is in 'res_obj' variable
        res_status_code = res_obj.status_code
        self.logger.debug("Response status code={}".format(res_status_code))
        # self.logger.debug("Response content={}".format(res_obj.content))

        if res_status_code != 200 and res_status_code != 201:
            error_text = res_obj.text
            self.logger.error("Unexpected response text={}".format(error_text))
            raise PakettikauppaException(error_text)

        return res_obj

    def parse_res_json_data(self, res_obj):
        """
        Parse response JSON data (Not yet completely implemented)

        :param res_obj: response object
        :return:
        """
        list_data = res_obj.json()
        self.logger.debug("Response JSON data={}".format(list_data))

        # self.logger.debug("data item={}".format(json.loads(list_data)))
        for item in list_data:
            self.logger.debug("item={}".format(item))
            self.logger.debug("\n")

    def parse_res_to_list(self, res_obj=None):
        """
        Parse response object to list data.

        :param res_obj: response object
        :return list_data: list data of response data from Pakettikauppa
        """
        if res_obj is not None:
            list_data = None
            try:
                list_data = res_obj.json()
                self.logger.debug("Response: {}".format(list_data))
            except Exception:
                raise PakettikauppaException("Unable to parse JSON data")
            finally:
                return list_data
        else:
            return None
