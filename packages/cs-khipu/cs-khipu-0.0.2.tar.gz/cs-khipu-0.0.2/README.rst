=========================================
Unofficial Khipu Web Services Python SDK
=========================================

Installation
============

Just run::

    $ python setup.py install


Usage
=====
.. code:: python

    from khipu.api import KhipuApi

    api = KhipuApi('receiver_id', 'secret_key')
    data = {
        'subject': 'Asunto',
        'body': 'Descripci?n',
        'amount': '10000',
        'payer_email': 'email',
        'bank_id': '',
        'expires_date': 'Unix timestamp',
        'transaction_id': 'T-1000',
        'custom': '',
        'notify_url': 'http://yourwebsite.cl/notificame/',
        'return_url': 'http://yourwebsite.cl/exito/',
        'cancel_url': '',
        'picture_url': ''
    }
    result = api.create_payment(**data)
    print result

Documentation
=============
You can refer to https://khipu.com/page/api for official API documentation.