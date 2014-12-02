#!/usr/bin/env python
#
# Sign (approve) a multisig transaction, using the Coinkite API and maybe an offline key.
#
# NOTE: If you want to sign without using an API key, and you have the private keys needed,
# consider using the example code at <https://github.com/coinkite/offline-multisig-python>
# instead of this program.
#
# Full docs at: https://docs.coinkite.com/
# 
# Copyright (C) 2014 Coinkite Inc. (https://coinkite.com) ... See LICENSE.md
#
import os, sys, click
try:
    import ckapi
except ImportError:
    # be nice and work even if CK api not yet installed, and we are run from git checkout
    sys.path.append(os.path.realpath(__file__ + '/../..'))
    import ckapi

@click.command()
@click.argument('request')
@click.argument('cosigner', required=False)
@click.option('--key', '-k', type=click.File('r'), default=None,
                    help="Extended private key (base58)")
@click.option('--passphrase', '-p', default=None,
                    help="Passphrase for HSM or Coinkite-stored keys.")
@click.option('--yes', '-y', is_flag=True, default=False,
                    help="Skip confirmation step")
@click.option('--no-pass', is_flag=True, default=False,
                    help="Skip asking for password, it's empty string")
@click.option('--host', 'api_host', default=None, metavar='URL', help="Alternate API host to use")
#
def approve(request, cosigner, key, passphrase, yes, no_pass, api_host):
    '''
        This script will sign the indicated request (by reference number) with the key
        of the indicated co-signer (also by ref num), using either values in HSM, Coinkite or
        provided extended private key.

        Prints current signing status of request if no co-signer is provided.
    '''
    api = ckapi.CKRequestor(host=api_host)

    if not yes or not cosigner:
        # get the particulars of the request
        req = api.get_detail(request)

        explain = u'''
Refnum: {CK_refnum}

>> {desc}

amount: {amount.pretty}
  memo: {memo}
'''.format(**req)

        if cosigner:
            click.confirm(explain + "\nOk to approve?  ", abort=True)
        else:
            click.echo(explain)

        if not cosigner:
            lst = '\n'.join('  %s: %s' % (k, 'Approved' if v else 'tbd')
                                    for k,v in req.cosign.signed_by.items())

            click.echo('Co-signers:\n\n%s\n' % lst)
            sys.exit(0)

    if not key:
        # we will use HSM or stored encrypted private key.
        if not no_pass and not passphrase:
            passphrase = click.prompt("\nPassphrase for signing", hide_input=True)

    try:
        result = api.cosign_request(request, cosigner,
                                        xprvkey_or_wallet=key.read() if key else None,
                                        passphrase=passphrase)
    except Exception, e:
        click.echo('\nFAILED:\n%s\n' % getattr(e, 'help_msg', str(e)))
        sys.exit(1)

    click.echo('\nSUCCESS:\n%s' % result.message)

    

if __name__ == '__main__':
    approve()

# EOF
