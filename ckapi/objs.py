

#
# Wrappers for Coinkite objects which you might see.
#

CK_DB_OBJECTS = [
    'CKUser',
    'CKEvent',
    'CKUserRequest',
    'CKCard',
    'CKActivityLog',
    'CKMagicCoin',
    'CKEmailAddress',
    'CKInvoice',
    'CKReqSend',
    'CKAccount',
    'CKReqReceive',
    'CKMembershipLevel',
    'CKPublicTxn',
    'CKBlockInfo',
    'CKTxnOutput',
    'CKReqTransfer',
    'CKBillPay',
    'CKEmailMessage',
    'CKTerminal',
    'CKTerminalLog',
    'CKVoucher',
    'CKNotification',
    'CKInvoiceState',
    'CKForwarding',
    'CKRevenuePayout',
    'CKRevShareLink',
    'CKRevShareHit',
    'CKPhoneNumber',
    'CKSMSMessage',
    'CKApiKey'
]

__all__ = CK_DB_OBJECTS + ['CKDBObject']

class CKDBObject(dict):
    #
    # Act like a dictionary, but also an object. Keys are attributes, attributes
    # are keys and so on.
    #
    _CK_type = None

    @property
    def ref_number(self):
        return self.CK_refnum

    def __getattr__(self, name):
        if name in self:
            return self[name]
        else:
            raise AttributeError('No such attribute: %s\nKnown attrs: %s' 
                                        % (name, ', '.join(self.keys())))

    def __setattr__(self, name, value):
        self[name] = value

    def __delattr__(self, name):
        del self[name]

    def __repr__(self):
        ret =  '<%s:' % self.get('CK_type', self._CK_type or self.__class__.__name__)
        for k,v in self.items():
            ret += ' %s=%r' % (k, v)
        return ret + '>'

# Declare a trival subclass of CKDBObject() for each of those names.
#
def onetime_setup():
    for _name in CK_DB_OBJECTS:
        _a = dict(CKDBObject.__dict__)
        _a['_CK_type'] = _name
        globals()[_name] = type(_name, (CKDBObject,), _a)

# I like clean namespaces
onetime_setup()
del onetime_setup

# EOF

