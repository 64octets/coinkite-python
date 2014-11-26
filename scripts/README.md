# Usage

	Usage: approve.py [OPTIONS] REQUEST [COSIGNER]

	  This script will sign the indicated request (by reference number) with the
	  key of the indicated co-signer (also by ref num), using either values in
	  HSM, Coinkite or provided extended private key.

	  Prints current signing status of request if no co-signer is provided.

	Options:
	  -k, --key FILENAME     Extended private key (base58)
	  -p, --passphrase TEXT  Passphrase for HSM or Coinkite-stored keys.
	  -y, --yes              Skip confirmation step
	  --no-pass              Skip asking for password, it's empty string
	  --host URL             Alternate API host to use
	  --help                 Show this message and exit.

# Examples

### Query Signing Status

    % ./approve.py 5B54BE8C16-991CFA 

    Refnum: 5B54BE8C16-991CFA

    >> Transfer funds

    amount: ❀ 0.2 XTN
      memo: Multiuser XTN → Testnet Fun

    Co-signers:

      4B9974FABC-4D0F0C: tbd
      90250FAFB7-7ADFBF: tbd
      0E6937B2E7-780A32: tbd
      2122D9549A-23E4DB: tbd
      36F304BDF5-E63212: tbd
      0CB6066482-C71359: tbd
      43FE9D8E6A-D87098: tbd
      C83F35FF74-8465AF: tbd


### Add Signature from Private Key file

    % cat key-90250FAFB7-7ADFBF-J5CRVzjv.pkey
    tprv8ZgxMBicQKsPeSjTkDwz3zcZ7cu95xpQGJA....ctTswa8LW9UyTVzRCKz7koqm6S6ukyKE2HeiMb3jjj3C5

    % ./approve.py 5B54BE8C16-991CFA 90250FAFB7-7ADFBF --key key-90250FAFB7-7ADFBF-J5CRVzjv.pkey 

    Refnum: 5B54BE8C16-991CFA

    >> Transfer funds

    amount: ❀ 0.2 XTN
      memo: Multiuser XTN → Testnet Fun

    Ok to approve?   [y/N]: y

    SUCCESS:
    Signature added, but further signatures are required.

### Add Signature from HSM

    % ./approve.py 5B54BE8C16-991CFA 2122D9549A-23E4DB --no-pass

    Refnum: 5B54BE8C16-991CFA

    >> Transfer funds

    amount: ❀ 0.2 XTN
      memo: Multiuser XTN → Testnet Fun

    Ok to approve?   [y/N]: y

    SUCCESS:
    Signature added, but further signatures are required.

### Updated Status

    % ./approve.py 5B54BE8C16-991CFA 

    Refnum: 5B54BE8C16-991CFA

    >> Transfer funds

    amount: ❀ 0.2 XTN
      memo: Multiuser XTN → Testnet Fun

    Co-signers:

      4B9974FABC-4D0F0C: tbd
      90250FAFB7-7ADFBF: Approved
      0E6937B2E7-780A32: tbd
      2122D9549A-23E4DB: Approved
      36F304BDF5-E63212: tbd
      0CB6066482-C71359: tbd
      43FE9D8E6A-D87098: tbd
      C83F35FF74-8465AF: tbd

