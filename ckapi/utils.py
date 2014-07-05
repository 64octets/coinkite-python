#
# Coinkite API: Make requests of the API easily.
#
# Full docs at: https://docs.coinkite.com/
# 
# Copyright (C) 2014 Coinkite Inc. (https://coinkite.com) ... See LICENSE.md
# 
#
import logging
from objs import make_db_object
from decimal import Decimal

try:
    # We prefer simple json.
    import simplejson

    json_encoder = simplejson.JSONEncoder(use_decimal=True, for_json=True)
    json_decoder = simplejson.JSONDecoder(object_hook=make_db_object, parse_float=Decimal)

except ImportError:
    # We need Decimal to be encoded corrected both for read and write! Not simple.
    import json
    json_decoder = json.JSONDecoder(object_hook=make_db_object, parse_float=Decimal)

    # Taken from http://stackoverflow.com/questions/1960516
    class DecimalEncoder(json.JSONEncoder):
        # NOTE: only required for python < 2.7 ??
        def _iterencode(self, o, markers=None):
            if isinstance(o, Decimal):
                return (str(o) for o in [o])
            return super(DecimalEncoder, self)._iterencode(o, markers)

        def default(self, o):
            if hasattr(o, 'for_json'):
                return o.for_json()
            return json.JSONEncoder.default(self, o)

    json_encoder = DecimalEncoder()


def test_json_encoding():
    # Verify code above is working.

    a = Decimal('0.3333333333333333333333333333')

    aa = json_decoder.decode(json_encoder.encode(a))

    assert a == aa


# EOF
