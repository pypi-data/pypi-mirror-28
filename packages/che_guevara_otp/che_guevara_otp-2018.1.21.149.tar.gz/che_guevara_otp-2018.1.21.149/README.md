# che_guevara_otp

![](https://raw.githubusercontent.com/wdbm/che_guevara_otp/master/2017_Che_Guevara_Éire_stamp.png)

This module generates one-time passcodes that are based either on a counter or time using a secret key that is assumed known by server and client.

The counter-based passcodes are hash-based one-time passcodes (HOTP) and are defined in [RFC 4226](https://tools.ietf.org/html/rfc4226). The time-based passcodes are time-based one-time passcodes (TOTP) and are defined in [RFC 6238](https://tools.ietf.org/html/rfc6238). For HOTP, the pseudorandom function used is HMAC-SHA-1 and the associated counter should be incremented after each passcode generation. TOTP is HOTP with a specified time interval for validity. A common time interval is 30 seconds.

# setup

```Bash
pip install che_guevara_otp
```

# module

HOTP passcodes can be generated in a way like the following:

```Python
>>> import che_guevara_otp
>>> secret = "XXXXXXXXXXXXXXXX"
>>> for nonce in range(0, 3):
...     print(che_guevara_otp.HOTP(secret = secret, nonce = nonce))
... 
561452
686073
840123
```

TOTP passcodes can be generated in a way like the following, where the default time interval is 30 seconds:

```Python
>>> import che_guevara_otp
>>> secret = "XXXXXXXXXXXXXXXX"
>>> print(che_guevara_otp.TOTP(secret = secret))
826402
```

# display_che_guevara_otp.py

![](https://raw.githubusercontent.com/wdbm/che_guevara_otp/master/display_che_guevara_otp.png)

The script `display_che_guevara_otp.py` displays time-based one-time passcodes at 30 second intervals based on secrets stored in a specified file. The file is unencrypted plaintext so userspace encryption combined with other security is assumed. The contents of the secrets file should be of the following form:

```
OmegaBay:         XXXXXXXXXXXXXXXXXXXXXXXX
Missile Emporium: YYYYYYYYYYYYYYYYYYYYYYYY
```
