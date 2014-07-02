#!/usr/bin/env python
#
# Helper program for using CURL <http://curl.haxx.se/> with the Coinkite API.
#
# Full API documentation available at: https://docs.coinkite.com
#
# This program print out the signed headers that you need for authorization, 
# in a form that can be used directly as the command-line arguments to Curl.
#
# EXAMPLE (bash):
#
#       % export CK_API_KEY=Kabababa-ababababab-abababab
#       % export CK_API_SECRET=S01010101-010101010101-1010101001
#       % curl `./ck-helper.py /v1/my/self`
#
#
import os, sys, datetime
from hmac import HMAC
from hashlib import sha256

# Replace these values.
API_KEY = os.environ.get('CK_API_KEY', None)
API_SECRET = os.environ.get('CK_API_SECRET', None)

API_HOST = 'https://api.coinkite.com'

def make_signature(endpoint, force_ts=None):
    #
    # Pick a timestamp and perform the signature required.
    #
    assert endpoint[0] == '/' and 'api.coinkite.com' not in endpoint, \
                "Expecting abs url, got: %s" % endpoint
     
    ts = force_ts or datetime.datetime.utcnow().isoformat()
    data = endpoint + "|" + ts
    hm = HMAC(API_SECRET, msg=data, digestmod=sha256)

    return hm.hexdigest(), ts

def auth_headers(endpoint, force_ts=None):
    #
    # Make the authorization headers that are needed to access indicated endpoint
    #
    if '?' in endpoint:
        endpoint = endpoint.split('?', 1)[0]

    signature, timestamp = make_signature(endpoint, force_ts=force_ts)
    auth_headers = {
        'X-CK-Key': API_KEY,
        'X-CK-Timestamp': timestamp,
        'X-CK-Sign': signature,
    }

    return auth_headers

#print '\n'.join(sign('/example/endpoint', '2014-06-03T17:48:47.774453'))


if __name__ == '__main__':
    #
    # - Expects an endpoint (URL) on the command line and nothing else.
    # - Renders to stdout, the arguments needed to make CURL work well.
    #

    if len(sys.argv) < 2:
        print "Requires an endpoint (URL) as only argument"
        sys.exit(1)

    if not API_KEY or not API_SECRET:
        print "Please define CK_API_KEY and CK_API_SECRET in the environment"
        sys.exit(1)

    # We need to know the endpoint being reached because it's part of the signature.
    endpoint = sys.argv[-1]

    hdrs = auth_headers(endpoint)
    cmd = ' '.join(['-H %s:%s' % j for j in hdrs.items()]) 

    # if you use PUT, you may want these as well, but you can just put them in yourself
    if 0:
        cmd += ' -H Content-type:application/json -X PUT'

    cmd += ' %s%s' % (API_HOST, endpoint)

    print cmd
