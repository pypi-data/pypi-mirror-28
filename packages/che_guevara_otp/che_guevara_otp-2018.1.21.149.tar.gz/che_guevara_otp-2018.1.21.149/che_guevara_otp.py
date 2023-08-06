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
import datetime
import hashlib
import hmac
import os
import struct
import sys
import time

import che_guevara_otp

name    = "che_guevara_otp"
version = "2018-01-21T0149Z"

def HOTP(
    secret        = None, # secret value known to both server and client
    nonce         = 0,    # number incremented between each token generation
    leading_zeros = True  # return a string with leading zeros
    ):

    """
    Generate and return a hash-based one-time passcode.
    """

    key     = base64.b32decode(secret, True)
    message = struct.pack(">Q", nonce)
    HMAC    = hmac.new(key, message, hashlib.sha1).digest()
    o       = (HMAC[19] if sys.version_info >= (3,) else ord(HMAC[19])) & 15
    HMAC    = (struct.unpack(">I", HMAC[o:o + 4])[0] & 0x7fffffff) % 1000000

    if leading_zeros:
        HMAC = str(HMAC).zfill(6)

    return HMAC

def TOTP(
    secret        = None, # secret value known to both server and client
    interval      = 30,   # number of seconds between each token generation
    leading_zeros = True  # return a string with leading zeros
    ):

    """
    Generate and return a time-based one-time passcode, changed at an interval
    of a specified number of seconds.
    """

    return HOTP(
        secret        = secret,
        nonce         = int(int(time.time()) / interval),
        leading_zeros = leading_zeros
    )

def loop_display_TOTP_passcodes(
    filepath_secrets  = "~/.secrets",
    set_terminal_size = True
    ):

    """
    Access secrets stored in specified file and loop display time-based one-time
    passcodes based on those secrets every 30 seconds.
    """

    filepath_secrets = os.path.expanduser(filepath_secrets)
    if not os.path.isfile(filepath_secrets):
        print("no secrets file {filepath_secrets} found".format(
            filepath_secrets = filepath_secrets)
        )
        sys.exit()

    while True:
        secrets = {}
        for line in open(filepath_secrets):
            data = line.rstrip("\n").split(":")
            secrets[data[0].strip()] = data[1].strip()
        os.system("clear")
        for key, value in secrets.items():
            print(key + "\n" + che_guevara_otp.TOTP(secret = value) + "\n")
        seconds = datetime.datetime.now().second
        while seconds != 0 and seconds != 31:
            if set_terminal_size:
                resize_terminal(
                    width  = len(max(list(secrets.keys()), key = len)),
                    height = len(secrets) * 3 + 1
                )
            seconds = datetime.datetime.now().second
            sys.stdout.write("\r")
            if seconds >= 0 and seconds <= 30:
                seconds_remaining = 30 - seconds
            else:
                seconds_remaining = 60 - seconds
            sys.stdout.write("{seconds_remaining} s".format(
                seconds_remaining = str(seconds_remaining).zfill(2)
            ))
            sys.stdout.flush()
            time.sleep(0.5)

def resize_terminal(
    width  = None,
    height = None
    ):

    sys.stdout.write(
        "\x1b[8;{height};{width}t".format(height = height, width = width)
    )
