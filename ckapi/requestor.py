#
# Coinkite API: Make requests of the API easily.
#
# Full docs at: https://docs.coinkite.com/
# 
# Copyright (C) 2014 Coinkite Inc. (https://coinkite.com) ... See LICENSE.md
# 
#
import logging
from objs import CKDBObject
from decimal import Decimal

try:
    import simplejson
except ImportError:
    # Sorry, but we cannot make do with the stock json library, because
    # we need Decimal to be encoded corrected both for read and write
    raise RuntimeError("Coinkite API requires the 'simplejson' package")

# Use only these two for encoding and decoding JSON.
#
json_encoder = simplejson.JSONEncoder(default = CKDBObject, use_decimal = True)
json_decoder = simplejson.JSONDecoder(object_hook = CKDBObject, parse_float = Decimal)

logger = logging.getLogger('ckapi')

class CKRequestor:
    pass
