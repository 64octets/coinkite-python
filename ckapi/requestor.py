#
# Coinkite API: Make requests of the API easily.
#
# Full docs at: https://docs.coinkite.com/
# 
# Copyright (C) 2014 Coinkite Inc. (https://coinkite.com) ... See LICENSE.md
# 
#
import os, sys, datetime, logging
from decimal import Decimal
from http_client import new_default_http_client
from json import json_decoder
from hmac import HMAC
from hashlib import sha256
from urlparse import urljoin, urlparse
from exc import CKArgumentError, CKServerSideError, CKMissingError

logger = logging.getLogger('ckapi')

class CKRequestor(object):

    def __init__(self, api_key = None, api_secret = None, host = 'https://api.coinkite.com', client=None):
        self.api_key = api_key or os.environ.get('CK_API_KEY', None)
        self.api_secret = api_secret or os.environ.get('CK_API_SECRET', None)
        self.host = host

        self.client = client or new_default_http_client(verify_ssl_certs=True)

    def request(self, method, endpt, **kws):
        assert method in ('GET', 'PUT')

        url = urljoin(self.host, endpt)
        endpt = urlparse(url).path

        hdrs = {}

        if 'headers' in kws:
            # User may supply some headers
            hdrs.update(kws.pop('headers'))

        if not endpt.startswith('/public'):
            # Almost always add AUTH headers
            hdrs.update(self.auth_headers(endpt))

        body, status = self.client.request(method, url, hdrs)
        
        # decode JSON
        body = json_decoder.decode(body)

        if status == 400:
            raise CKArgumentError(body)
        if status == 404:
            raise CKMissingError(body)
        elif status != 200:
            raise CKServerSideError(body)

        return body

    def get(self, endpt, **kws):
        return self.request('GET', endpt, **kws)

    def put(self, endpt, **kws):
        return self.request('PUT', endpt, **kws)

    def get_detail(self, refnum):
        "Get detailed-view of any CK object"
        return self.get('/v1/detail/' + refnum).detail


    def make_signature(self, endpoint, force_ts=None):
        #
        # Pick a timestamp and perform the signature required.
        #
        assert endpoint[0] == '/' and 'api.coinkite.com' not in endpoint, \
                    "Expecting abs url, got: %s" % endpoint
        assert '?' not in endpoint, endpoint
         
        ts = force_ts or datetime.datetime.utcnow().isoformat()
        data = endpoint + "|" + ts
        hm = HMAC(self.api_secret, msg=data, digestmod=sha256)

        return hm.hexdigest(), ts

    def auth_headers(self, endpoint, force_ts=None):
        #
        # Make the authorization headers that are needed to access indicated endpoint
        #

        if not self.api_key:
            raise RuntimeError("API Key for Coinkite is required. "
                                "We recommend setting CK_API_KEY in environment")
        if not self.api_secret:
            raise RuntimeError("API Secret for Coinkite is required. "
                        "We recommend setting CK_API_SECRET in environment!")

        signature, timestamp = self.make_signature(endpoint, force_ts=force_ts)

        auth_headers = {
            'X-CK-Key': self.api_key,
            'X-CK-Timestamp': timestamp,
            'X-CK-Sign': signature,
        }

        return auth_headers

if 1:
    r = CKRequestor()
    #print r.get('/public/endpoints')
    #print r.get('/v1/my/self')
    #print r.get_detail('512069325D-AB194F')
    print r.get_detail('512069325D-AB1942')

# EOF
