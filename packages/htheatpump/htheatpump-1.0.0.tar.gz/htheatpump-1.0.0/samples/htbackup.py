#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#  htheatpump - Serial communication module for Heliotherm heat pumps
#  Copyright (C) 2018  Daniel Strigl

#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

""" Command line tool to create a backup of the Heliotherm heat pump data points.

    Example:

    .. code-block:: shell

       $ python3 htbackup.py --baudrate 9600 --csv backup.csv
       'SP,NR=0' [Language]: 0
       'SP,NR=1' [TBF_BIT]: 0
       'SP,NR=2' [Rueckruferlaubnis]: 1
       ...
       'MP,NR=0' [Temp. Aussen]: 0.1
       'MP,NR=1' [Temp. Aussen verzoegert]: 0.1
       'MP,NR=2' [Temp. Brauchwasser]: 50.2
       ...
"""

import sys
import argparse
import textwrap
import re
import json
import csv
from htheatpump.htheatpump import HtHeatpump
from timeit import default_timer as timer
import logging
_logger = logging.getLogger(__name__)


# Main program
def main():
    parser = argparse.ArgumentParser(
        description = textwrap.dedent('''\
            Command line tool to create a backup of the Heliotherm heat pump settings.

            Example:

              $ python3 %(prog)s --baudrate 9600 --csv backup.csv
              'SP,NR=0' [Language]: 0
              'SP,NR=1' [TBF_BIT]: 0
              'SP,NR=2' [Rueckruferlaubnis]: 1
              ...
            '''),
        formatter_class = argparse.RawDescriptionHelpFormatter,
        epilog = textwrap.dedent('''\
            DISCLAIMER
            ----------

              Please note that any incorrect or careless usage of this program as well as
              errors in the implementation can damage your heat pump!

              Therefore, the author does not provide any guarantee or warranty concerning
              to correctness, functionality or performance and does not accept any liability
              for damage caused by this program or mentioned information.

              Thus, use it on your own risk!
            ''') + "\r\n")

    parser.add_argument(
        "-d", "--device",
        default = "/dev/ttyUSB0",
        type = str,
        help = "the serial device on which the heat pump is connected, default: %(default)s")

    parser.add_argument(
        "-b", "--baudrate",
        default = 115200,
        type = int,
        # the supported baudrates of the Heliotherm heat pump (HP08S10W-WEB):
        choices = [9600, 19200, 38400, 57600, 115200],
        help = "baudrate of the serial connection (same as configured on the heat pump), default: %(default)s")

    parser.add_argument(
        "-j", "--json",
        type = str,
        help="write the result to the specified JSON file")

    parser.add_argument(
        "-c", "--csv",
        type = str,
        help="write the result to the specified CSV file")

    parser.add_argument(
        "-t", "--time",
        action = "store_true",
        help = "measure the execution time")

    parser.add_argument(
        "-v", "--verbose",
        action = "store_true",
        help = "increase output verbosity by activating logging")

    args = parser.parse_args()

    # activate logging with level INFO in verbose mode
    if args.verbose:
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.ERROR)

    hp = HtHeatpump(args.device, baudrate=args.baudrate)
    start = timer()
    try:
        hp.open_connection()
        hp.login()

        rid = hp.get_serial_number()
        if args.verbose:
            _logger.info("connected successfully to heat pump with serial number {:d}".format(rid))
        ver = hp.get_version()
        if args.verbose:
            _logger.info("software version = {} ({:d})".format(ver[0], ver[1]))

        result = {}
        for dp_type in ("SP", "MP"):  # for all known data point types
            result.update({dp_type: {}})
            i = -1
            while True:
                i += 1
                data_point = "{},NR={:d}".format(dp_type, i)
                # send request for data point to the heat pump
                hp.send_request(data_point)
                # ... and wait for the response
                try:
                    resp = hp.read_response()
                    # search for pattern "NAME=..." and "VAL=..." inside the answer
                    m = re.match("^{},.*NAME=([^,]+).*VAL=([^,]+).*$".format(data_point), resp)
                    if not m:
                        raise IOError("invalid response for query of data point {!r} [{}]".format(data_point, resp))
                    name, value = m.group(1, 2)  # extract name and value
                    print("{!r} [{}]: {}".format(data_point, name, value))
                    # store the determined data in the result dict
                    result[dp_type].update({i: {"name": name, "value": value}})
                except Exception as e:
                    _logger.warning("query of data point {!r} failed: {!s}".format(data_point, e))
                    # hp.reconnect()  # perform a reconnect
                    break

        if args.json:  # write result to JSON file
            with open(args.json, 'w') as jsonfile:
                json.dump(result, jsonfile, indent=4, sort_keys=True)

        if args.csv:  # write result to CSV file
            with open(args.csv, 'w') as csvfile:
                fieldnames = ["type", "number", "name", "value"]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for dp_type, content in result.items():
                    for i, data in content.items():
                        writer.writerow({"type": dp_type, "number": i, "name": data["name"], "value": data["value"]})

    except Exception as ex:
        _logger.error(ex)
        sys.exit(1)
    finally:
        hp.logout()  # try to logout for an ordinary cancellation (if possible)
        hp.close_connection()
    end = timer()

    # print execution time only if desired
    if args.time:
        print("execution time: {:.2f} sec".format(end - start))

    sys.exit(0)


if __name__ == "__main__":
    main()
