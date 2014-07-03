#
# Coinkite API: Make requests of the API easily.
#
# Full docs at: https://docs.coinkite.com/
# 
# Copyright (C) 2014 Coinkite Inc. (https://coinkite.com) ... See LICENSE.md
# 
#
import os, sys, datetime, logging, itertools
from decimal import Decimal
from http_client import new_default_http_client
from json import json_decoder, json_encoder
from hmac import HMAC
from hashlib import sha256
from urlparse import urljoin, urlparse
from urllib import urlencode
from exc import CKArgumentError, CKServerSideError, CKMissingError

logger = logging.getLogger('ckapi')

class CKRequestor(object):

    def __init__(self, api_key = None, api_secret = None, host = 'https://api.coinkite.com', client=None):
        self.api_key = api_key or os.environ.get('CK_API_KEY', None)
        self.api_secret = api_secret or os.environ.get('CK_API_SECRET', None)
        self.host = host

        self.client = client or new_default_http_client(verify_ssl_certs=True)

    def request(self, method, endpt, **kws):
        "Low level method to perform API request: provide HTTP method and endpoint"
        assert method in ('GET', 'PUT'), method

        url = urljoin(self.host, endpt)
        endpt = urlparse(url).path

        hdrs = {}

        if '_headers' in kws:
            # User may supply some headers? Probably not useful
            hdrs.update(kws.pop('_headers'))

        if not endpt.startswith('/public'):
            # Almost always add AUTH headers
            hdrs.update(self._auth_headers(endpt))

        data = None
        if kws:
            assert '?' not in url, "Please don't mix keyword args and query string in URL"

            if method == 'GET':
                # encode as query args.
                url += '?' + urlencode(kws)
            else:
                # submit a JSON document
                data = json_encoder.encode(kws)
                hdrs['Content-Type'] = 'application/json'

        print url
        body, status = self.client.request(method, url, hdrs, data)
        
        # decode JSON
        body = json_decoder.decode(body)

        if status == 400:
            raise CKArgumentError(body)
        if status == 404:
            raise CKMissingError(body)
        elif status != 200:
            raise CKServerSideError(body)

        return body

    def _make_signature(self, endpoint, force_ts=None):
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

    def _auth_headers(self, endpoint, force_ts=None):
        #
        # Make the authorization headers that are needed to access indicated endpoint
        #

        if not self.api_key:
            raise RuntimeError("API Key for Coinkite is required. "
                                "We recommend setting CK_API_KEY in environment")
        if not self.api_secret:
            raise RuntimeError("API Secret for Coinkite is required. "
                        "We recommend setting CK_API_SECRET in environment!")

        signature, timestamp = self._make_signature(endpoint, force_ts=force_ts)

        return {
            'X-CK-Key': self.api_key,
            'X-CK-Timestamp': timestamp,
            'X-CK-Sign': signature,
        }

    def get(self, endpt, **kws):
        "Perform a GET on indicated resource (endpoint) with optional arguments"
        return self.request('GET', endpt, **kws)

    def put(self, endpt, **kws):
        "Perform a PUT on indicated resource (endpoint) with optional arguments"
        return self.request('PUT', endpt, **kws)

    def get_iter(self, endpoint, offset=0, limit=None, batch_size=25, safety_limit=500, **kws):
        '''Return a generator that will iterate over all results, regardless of how many.
    
           This should work on any endpoint that has a offset/limit argument and
           returns paging data. Can provide offset or limit as well.
        '''

        def doit(offset, limit, batch_size):
            args = dict(kws)

            while 1:
                # Fetch as many results as we can at this offset
                if limit and limit < batch_size:
                    batch_size = limit

                rv = self.get(endpoint, offset=offset, limit=batch_size, **args)

                # look at paging situation
                here = rv.paging.count_here
                total = rv.paging.total_count

                # rescue drowning programs.
                if total > safety_limit:
                    raise Exception("Too many results (%d); consider another approach" % total)

                # are we done?
                if not here:
                    return

                # give up the results for the page of values
                for i in rv.results:
                    yield i

                # on to next page of data
                offset += here
                if limit != None:
                    limit -= here
                    if limit <= 0:
                        return

        return itertools.chain(doit(offset, limit, batch_size))

    #
    # Simple wrappers / convenience functions.
    #

    def check_myself(self):
        # ... before you wreck yourself.
        return r.get('/v1/my/self')

    def get_detail(self, refnum):
        "Get detailed-view of any CK object by reference number"
        return self.get('/v1/detail/' + refnum).detail

    def get_accounts(self, balances=False):
        "Get a list of accounts, doesn't include balances"
        return self.get('/v1/my/accounts').results

    def get_balance(self, account):
        "Get account details, including balance, by account name, number or refnum"
        return self.get('/v1/account/' + str(account)).account

    def get_list(self, what, account=None, **kws):
        '''Get a list of objects, using /v1/list/WHAT endpoints, where WHAT is:
                activity
                credits
                debits
                events
                notifications
                receives
                requests
                sends
                transfers
                unauth_sends

            This is a generator, so keep that in mind.
        '''
        ep = '/v1/list/%s' % what

        if account != None:
            kws['account'] = str(account)

        return self.get_iter(ep, **kws)

    def get_count(self, what, **kws):
        "Similar to get_list(), but this returns just the count of the # of objects"
        return self.get('/v1/list/' + what, limit=0, **kws).paging.total_count


if 1:
    r = CKRequestor()
    #print r.get('/public/endpoints')
    #print r.get('/v1/my/self')
    #print r.get_detail('512069325D-AB194F')
    #print r.get_detail('512069325D-AB1942')
    #print r.put('/v1/list/activity', limit=1)
    #print r.get_count('activity', account=1)
    #print r.get_accounts()
    #print r.get_balance(0)
    #print r.get_list('requests', limit=1, account=0)
    #print list(r.get_list('requests', account=0))
    #print list(r.get_list('requests', account=0, limit=5))
    print [str(i) for i in r.get_list('requests', account=0, limit=7)]

# EOF
