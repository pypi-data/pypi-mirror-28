#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
################################################################################
#                                                                              #
# loop_display_arbitrage_data                                                  #
#                                                                              #
################################################################################
#                                                                              #
# LICENCE INFORMATION                                                          #
#                                                                              #
# This program loop records Kraken LocalBitcoins UK arbitrage data.            #
#                                                                              #
# copyright (C) 2017 Will Breaden Madden, wbm@protonmail.ch                    #
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
    -h, --help      display help message
    --version       display version and exit

    --CSV=FILEPATH  filepath of CSV data         [default: arbitrage_Kraken_LocalBitcoins_UK.csv]

    --interval=INT  time between recordings (s)  [default: 60]
"""

import docopt
import os
import sys
import time

import denarius
import pandas as pd

name    = "loop_display_arbitrage_data"
version = "2018-01-05T1727Z"
logo    = None

def main(options):

    filepath_CSV = os.path.expanduser(options["--CSV"])
    interval     = int(options["--interval"])

    if not os.path.isfile(filepath_CSV):

        print("no CSV file {filepath_CSV} found".format(filepath_CSV = filepath_CSV))
        sys.exit()

    while True:

        try:

            _df = pd.read_csv(filepath_CSV)

            v = 5000 # EUR volume
            g = 100  # EUR minimum gain

            # loss factor is number by which volume amount can be multipled to get voluming resulting after fees etc.
            loss_factor = (v - (0.016 * v) - (6) - (0.01 * v) - (0.0035 * v + 0.90)) / v
            required_arbitrage_factor = 2 - loss_factor + g/v

            current_arbitrage_factor = _df["arbitrage_Kraken_LBC_2"].values[-1]
            profit_with_current_arbitrage_factor = current_arbitrage_factor * (v * loss_factor) - v

            prices = denarius.prices_Bitcoin_Ethereum()

            text =\
"""

{datetime}

arbitrage_Kraken_LBC_3:   {arbitrage_Kraken_LBC_3} <---
arbitrage_Kraken_LBC_2:   {arbitrage_Kraken_LBC_2}
arbitrage_Kraken_LBC_1:   {arbitrage_Kraken_LBC_1}

LBC_1:                    {LBC_1_GBP}
LBC_2:                    {LBC_2_GBP}
LBC_3:                    {LBC_3_GBP} <---
LBC_4:                    {LBC_4_GBP}
LBC_5:                    {LBC_5_GBP}

Kraken_last_price_GBP:    {Kraken_last_price_GBP}
Kraken_last_price_EUR:    {Kraken_last_price_EUR}

BTC_EUR:                  {BTC_EUR_last}
BTC_USD:                  {BTC_USD_last}
ETH_EUR:                  {ETH_EUR_last}
ETH_USD:                  {ETH_USD_last}
ETH_BTC:                  {ETH_BTC_last}

required arbitrage
factor:                   {required_arbitrage_factor}

profit with current
arbitrage factor:         {profit_with_current_arbitrage_factor}

trade?                    {conditional} <---
""".format(
    datetime                             = _df["datetime"].values[-1],
    arbitrage_Kraken_LBC_3               = _df["arbitrage_Kraken_LBC_3"].values[-1],
    arbitrage_Kraken_LBC_2               = _df["arbitrage_Kraken_LBC_2"].values[-1],
    arbitrage_Kraken_LBC_1               = _df["arbitrage_Kraken_LBC_1"].values[-1],
    gain                                 = g,
    volume                               = v,
    required_arbitrage_factor            = required_arbitrage_factor,
    profit_with_current_arbitrage_factor = profit_with_current_arbitrage_factor,
    LBC_1_GBP                            = _df["LBC_1_GBP"].values[-1],
    LBC_2_GBP                            = _df["LBC_2_GBP"].values[-1],
    LBC_3_GBP                            = _df["LBC_3_GBP"].values[-1],
    LBC_4_GBP                            = _df["LBC_4_GBP"].values[-1],
    LBC_5_GBP                            = _df["LBC_5_GBP"].values[-1],
    Kraken_last_price_GBP                = _df["Kraken_last_price_GBP"].values[-1],
    Kraken_last_price_EUR                = _df["Kraken_last_price_EUR"].values[-1],
    conditional                          = "YES" if _df["arbitrage_Kraken_LBC_3"].values[-1] >= required_arbitrage_factor else "NO",
    BTC_EUR_last                         = prices["BTC_EUR"]["last"],
    BTC_USD_last                         = prices["BTC_USD"]["last"],
    ETH_EUR_last                         = prices["ETH_EUR"]["last"],
    ETH_USD_last                         = prices["ETH_USD"]["last"],
    ETH_BTC_last                         = prices["ETH_BTC"]["last"]
)

            print(text)

        except:

            print("error")
            pass

        time.sleep(interval)
        os.system("clear")

if __name__ == "__main__":
    options = docopt.docopt(__doc__)
    if options["--version"]:
        print(version)
        exit()
    main(options)
