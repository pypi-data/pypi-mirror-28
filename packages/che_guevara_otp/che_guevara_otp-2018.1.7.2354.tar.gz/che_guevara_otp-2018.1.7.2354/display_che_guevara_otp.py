#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
################################################################################
#                                                                              #
# display_che_guevara_otp                                                      #
#                                                                              #
################################################################################
#                                                                              #
# LICENCE INFORMATION                                                          #
#                                                                              #
# This program displays time-based one-time passcodes at 30 second intervals   #
# based on secrets stored in a specified file.                                 #
#                                                                              #
# copyright (C) 2018 Will Breaden Madden, wbm@protonmail.ch                    #
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

usage:
    program [options]

options:
    -h, --help          display help message
    --version           display version and exit

    --secrets=FILEPATH  filepath of secrets  [default: ~/.secrets]
"""

import datetime
import docopt
import os
import sys
import time

import che_guevara_otp

name    = "display_che_guevara_otp"
version = "2018-01-07T2354Z"

def main(options):

    filepath_secrets = os.path.expanduser(options["--secrets"])

    if not os.path.isfile(filepath_secrets):
        print("no secrets file {filepath_secrets} found".format(
            filepath_secrets = filepath_secrets)
        )
        sys.exit()

    secrets = {}

    while True:

        secrets = {}

        for line in open(filepath_secrets):
            data = line.rstrip("\n").split(":")
            secrets[data[0].strip()] = data[1].strip()

        os.system("clear")

        for key, value in secrets.items():
            print(key + "\n" + str(che_guevara_otp.TOTP(secret = value)) + "\n")

        seconds = datetime.datetime.now().second

        while seconds != 0 and seconds != 31:

            seconds = datetime.datetime.now().second
            sys.stdout.write("\r")
            if seconds >= 0 and seconds <= 30:
                seconds_remaining = 30 - seconds
            else:
                seconds_remaining = 60 - seconds
            sys.stdout.write("{seconds_remaining} seconds to change".format(
                seconds_remaining = str(seconds_remaining).zfill(2)
            ))
            sys.stdout.flush()
            time.sleep(0.5)

if __name__ == "__main__":
    options = docopt.docopt(__doc__)
    if options["--version"]:
        print(version)
        exit()
    main(options)
