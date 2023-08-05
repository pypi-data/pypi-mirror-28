# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging
import hashlib
import hmac
import urllib
import requests

# Set version for API
from .exception import KhipuError

VERSION_KHIPU_SERVICE = '2.0'


class Transaction(object):
    def __init__(self, method, service, data, params):
        self.method = method
        self.service = service
        self.data = data
        self.params = params
        self.headers = ""


class KhipuService(object):
    def __init__(self, receiver_id, secret):
        self.receiver_id = receiver_id
        self.secret = secret

        # Services
        self.CREATE_PAYMENT = 'payments'
        self.GET_PAYMENT_TOKEN = 'payments'
        self.GET_PAYMENT_ID = 'payments/{id}'
        self.REFUND_PAYMENT = '/payments/{id}/refunds'
        self.DELETE_PAYMENT = ''
        self.CREATE_RECEIVER = ''

        # Set url to API
        self.API_URL = 'https://khipu.com/api/%s/' % VERSION_KHIPU_SERVICE

        # Declare status error
        self.STATUS_ERRORS = {
            400: 'Invalid Data.',
            403: 'Authorization Error.',
            503: 'Operation Error.'
        }

        # Init logger
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)
        logging.getLogger("tbk.service").setLevel(logging.DEBUG)

    def request(self, method, service, data, params=None):
        transaction = Transaction(method=method, service=self.API_URL + service, data=data, params=params)
        headers = self.create_headers(transaction)
        transaction.headers = headers
        response = self.do_request(transaction)
        self.validate_response(response)
        return response.json()

    def validate_response(self, response):
        if response.status_code in self.STATUS_ERRORS.keys():
            raise KhipuError(
                message="Status Code {0}: {1}".format(response.status_code, self.STATUS_ERRORS[response.status_code]),
                error_code=response.status_code)

    def create_headers(self, transaction):
        # Set headers
        headers = {
            'Authorization': '%s:%s' % (self.receiver_id, self.do_hash(transaction),),
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        return headers

    def do_request(self, transaction):

        try:
            return requests.request(transaction.method, transaction.service, params=transaction.params,
                                    data=transaction.data, headers=transaction.headers)
        except Exception as e:
            self.logger.error(e.message)
            raise KhipuError(message=e.message, error_code=500)

    def do_hash(self, transaction):
        """
        Generate hash specific for Khipu
        """
        return hmac.new(self.secret.encode(),
                        self.create_concatenated_data(transaction).encode(),
                        hashlib.sha256).hexdigest()

    @classmethod
    def create_concatenated_data(cls, transaction):
        # Init vars
        all_data = {}
        cad = '%s&%s' % (transaction.method, cls.__url_encode(transaction.service))

        if transaction.params is not None:
            for key, value in transaction.params.iteritems():
                all_data[key] = value

        if transaction.data is not None:
            for key, value in transaction.data.iteritems():
                all_data[key] = value

        # Remove amount of all_data and set in cad
        if 'amount' in all_data:
            cad += '&{0}={1}'.format('amount', all_data['amount'])
            all_data.pop('amount', None)

        if all_data is not None or len(all_data) > 0:
            for key, value in iter(sorted(all_data.iteritems())):
                value = cls.__url_encode(value)
                cad += '&{0}={1}'.format(key, value)

        return cad

    @classmethod
    def __url_encode(cls, s):
        if s is None:
            return ''
        return urllib.quote_plus(s).replace("+", "%20").replace("*", "%2A").replace("%7E", "~")
