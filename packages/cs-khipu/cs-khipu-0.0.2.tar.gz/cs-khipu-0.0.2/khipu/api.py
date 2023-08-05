# -*- coding: utf-8 -*-
from collections import OrderedDict

from .service import KhipuService

from .exception import KhipuError


class KhipuApi(KhipuService):
    def create_payment(self, **kwargs):
        required = frozenset(['subject', 'currency', 'amount'])
        optionals = [
            'transaction_id',
            'custom',
            'body',
            'bank_id',
            'return_url',
            'cancel_url',
            'picture_url',
            'notify_url',
            'notify_api_version',
            'expires_date',
            'send_email',
            'payer_name',
            'payer_email',
            'send_reminders',
            'responsible_user_email',
            'fixed_payer_personal_identifier',
            'integrator_fee'
        ]

        if not required.issubset(frozenset(kwargs.keys())):
            raise KhipuError(message="Create Payment should have this data: %s" % ', '.join(required),
                             error_code=500)

        data = {
            'subject': kwargs.pop('subject'),
            'currency': kwargs.pop('currency'),
            'amount': kwargs.pop('amount').replace('$', '')
        }

        for v in optionals:
            if v in kwargs:
                valor = kwargs.pop(v)
                if valor is not None:
                    data[v] = valor

        return self.request('POST', self.CREATE_PAYMENT, data)

    def get_payment_by_token(self, notification_token):
        if notification_token is None:
            raise KhipuError(message="Get Payment by Token should have this data: notification token",
                             error_code=500)

        params = {
            'notification_token': notification_token,
        }

        return self.request('GET', self.GET_PAYMENT_TOKEN, data=None, params=params)

    def get_payment_id(self, payment_id):
        if payment_id is None or payment_id == "":
            raise KhipuError(message="Invalid PaymentID", error_code=500)

        return self.request('GET', self.GET_PAYMENT_ID.format(id=payment_id), data=None, params=None)

    def refund_payment(self, payment_id):
        if payment_id is None or payment_id == "":
            raise KhipuError(message="Invalid PaymentID", error_code=500)

        return self.request('POST', self.REFUND_PAYMENT.format(id=payment_id), data=None, params=None)
