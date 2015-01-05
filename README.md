# Coinkite API Tools for Python 

[Learn more about Coinkite's API here](https://docs.coinkite.com/)
and visit the [Coinkite Main Site](https://coinkite.com/) to open your
account today!

Easy install via pip from the Cheese Shop: [coinkite-api package](https://pypi.python.org/pypi/coinkite-api)

## Requirements

- [datautils](http://labix.org/python-dateutil) is required to parse ISO 8601 format dates.

- [SimpleJSON](http://simplejson.readthedocs.org/en/latest/) is
  *very strongly* recommended. It's best because we have to control how decimals are
  encoded and decoded into JSON. We do have some workaround code in place to use the
  stock `json` module, but it's a ugly hack that can only work some of the time.

- [Requests module](http://docs.python-requests.org/en/latest/) is strongly
  recommended, but not required.

- [py.test](http://pytest.org/) is needed, but only if you want to
  run the test code in `test_code.py`

- [PubNub python library](https://github.com/pubnub/python) is needed,
  if you want to monitor real-time events.

- This code should work directly on Google App Engine without changes.

See version numbers in the `requirements.txt` file, which should
be ready to use with `pip install -r requirements.txt`. It includes
the full compliment of dependances.

## Standalone vs. `ckapi` Library

`standalone/ck-helper.py` is a simple cURL helper program that calculates the
authentication headers you will need. It provides a great way to quickly test
requests. Feel free to pull the authentication code from there or the library.

`ckapi` is a module you can incorporate into your server-side code.
It handles authentication and HTTPS traffic (including the all-important
certificate verification), plus provides wrappers for some of the
most useful API resources. It does magic in the JSON decoding to
provide more realistic objects to your programs, and correctly
decodes `decimal.Decimal` numbers.

Also included in the library:

- Testing code which can be a source of examples (see `test_code.py`).

- `paper.py` which simplifies the rendering of receipts for terminals.

- `multisig.py` providing code for signing (authorizing) multisig transactions.

## Getting Started

````python
>>> from ckapi import CKRequestor
>>> r = CKRequestor('Kxxxx-xxxx-xxx', 'Sxxxx-xxxx-xxx')
>>> r.get('/v1/my/self')
<CKObject: supported_cct=<CKObject: USD='US Dollar' AUD='Australian Dollar' CHF='Swiss Franc' KRW='Won' CNY='Yuan Renminbi' LTC='Litecoin' BLK='Blackcoin' NZD='New Zealand Dollar' XTN='Bitcoin Testnet' EUR='Euro' RUB='Russian Ruble' JPY='Yen' BRL='Brazilian Real' BTC='Bitcoin' PLN='Zloty' CAD='Canadian Dollar' SEK='Swedish Krona' GBP='Pound Sterling'>
 member_since='2014-06-12' membership='Personal Plan (pre-paid annually)'
 api_key=<CKApiKey: funds_limit=<CKObject: currency='XTN' string='100' pretty=u'\u2740 100.0 XTN' integer_scale=8 integer=10000000000 decimal=100> CK_refnum='09B724B100-9A3B47' max_request_rate=0 memo='All access' source_ip=None CK_type='CKApiKey' api_key='Kxxx-xxx-xxx' permissions=['term', 'read', 'send2', 'send', 'xfer', 'recv', 'events']>
 username='xxx'>
>>> r.put('/v1/new/voucher', account=0, amount=3)
````


## More about Coinkite

_Join The Most Powerful Bitcoin Platform_

Coinkite is the leading [bitcoin wallet](https://coinkite.com/faq/features) with
[multi-signature](https://coinkite.com/faq/multisig),
[bank-grade security](https://coinkite.com/faq/security),
[developer's API](https://coinkite.com/faq/developers) and [hardcore privacy](https://coinkite.com/privacy).

[Get Your Account Today!](https://coinkite.com/)


