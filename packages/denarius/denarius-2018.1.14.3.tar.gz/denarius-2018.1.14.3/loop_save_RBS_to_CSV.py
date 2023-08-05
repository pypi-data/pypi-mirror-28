#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
################################################################################
#                                                                              #
# loop_save_RBS_to_CSV                                                         #
#                                                                              #
################################################################################
#                                                                              #
# LICENCE INFORMATION                                                          #
#                                                                              #
# This program gets the recent transactions of an RBS account using Firefox    #
# and Selenium and saves them, together with the current balance, to CSV.      #
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
    -h, --help              display help message
    --version               display version and exit

    --CSV=FILEPATH          bank account CSV             [default: ./RBS.csv]
    --interval=INT          time between recordings (s)  [default: 180]
"""

import dataset
import docopt
import os
import time
import sys

import numpy as np
import pandas as pd
import RBS

name    = "loop_save_RBS_to_CSV"
version = "2018-01-14T0003Z"

def main(options):

    filepath_CSV = os.path.expanduser(options["--CSV"])
    interval     =                int(options["--interval"])

    while True:

        try:
            print("access account")
            status = RBS.account_status()
            df = status["transactions"]
            df["balance"] = np.nan
            # add balance only to top transaction
            df.at[0, "balance"] = status["balance"]
            print("--------------------------------------------------------------------------------")
            print("current account status:\n")
            print(df)

            # check existing recorded data to avoid saving previously-saved data
            if os.path.isfile(filepath_CSV):
                print("merge current account status with previously-recorded states")
                df_old = pd.read_csv(filepath_CSV)
                print("--------------------------------------------------------------------------------")
                print("previous account status:\n")
                print(df_old)
                df = pd.concat([df_old, df], ignore_index = True).drop_duplicates().reset_index(drop = True)
                print("--------------------------------------------------------------------------------")
                print("merged account status:\n")
                print(df)

            with open(filepath_CSV, "a") as file_CSV:
                print("save account status to CSV {filepath}".format(filepath = filepath_CSV))
                df.to_csv(file_CSV, header = True, index = False)
        except:
            print("error getting transactions")
            pass

        print("sleep {interval} s".format(interval = interval))
        time.sleep(interval)

if __name__ == "__main__":
    options = docopt.docopt(__doc__)
    if options["--version"]:
        print(version)
        exit()
    main(options)
