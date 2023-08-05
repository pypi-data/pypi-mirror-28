# -*- coding: utf-8 -*-

"""
################################################################################
#                                                                              #
# che_guevara_otp                                                              #
#                                                                              #
################################################################################
#                                                                              #
# LICENCE INFORMATION                                                          #
#                                                                              #
# This program generates one-time passcodes that are based either on a counter #
# or time using a secret key that is assumed known by server and client.       #
#                                                                              #
# copyright (C) 2018 William Breaden Madden                                    #
#                                                                              #
# This software is released under the terms of the GNU General Public License  #
# version 3 (GPLv3).                                                           #
#                                                                              #
# This program is free software: you can redistribute it and/or modify it      #
# under the terms of the GNU General Public License as published by the Free   #
# Software Foundation, either version 3 of the License, or (at your option)    #
# any later version.                                                           #
#                                                                              #
# This program is distributed in the hope that it will be useful, but WITHOUT  #
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or        #
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for     #
# more details.                                                                #
#                                                                              #
# For a copy of the GNU General Public License, see                            #
# <http://www.gnu.org/licenses/>.                                              #
#                                                                              #
################################################################################
"""

import base64
import hashlib
import hmac
import struct
import sys
import time

name    = "che_guevara_otp"
version = "2018-01-07T2354Z"

def HOTP(
    secret = None, # secret value known to both server and client
    nonce  = 0     # number incremented between each token generation
    ):

    """
    Generate and return a hash-based one-time passcode.
    """

    key     = base64.b32decode(secret, True)
    message = struct.pack(">Q", nonce)
    HMAC    = hmac.new(key, message, hashlib.sha1).digest()
    o       = (HMAC[19] if sys.version_info >= (3,) else ord(HMAC[19])) & 15
    HMAC    = (struct.unpack(">I", HMAC[o:o + 4])[0] & 0x7fffffff) % 1000000

    return HMAC

def TOTP(
    secret   = None, # secret value known to both server and client
    interval = 30    # number of seconds between each token generation
    ):

    """
    Generate and return a time-based one-time passcode, changed at an interval
    of a specified number of seconds.
    """

    return HOTP(
        secret = secret,
        nonce  = int(int(time.time()) / 30)
    )
