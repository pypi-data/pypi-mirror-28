#!bin/python
from __future__ import print_function, unicode_literals

try:
    from urllib.request import urlopen, Request, HTTPError
    import configparser as cp
except ImportError:
    import ConfigParser as cp
    from urllib2 import urlopen, Request, HTTPError
import argparse
from colorama import init, Fore
import json
import os

init(autoreset=True)

# constants
description = "Your friendly, no-nonsense tool to instantaneously check cryptocurrency prices"
epilog = "hodl.py: helping you HODL one day at a time :)"
__version__ = "v.1.0.0a1"
cryptos = ['btc', 'bch', 'eth', 'ltc']

# load config file
config_filename = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                               'conf', 'config.ini')
config = cp.ConfigParser()
config.read(config_filename)


def get_price(crypto="BTC", fiat=config.get("currency", "FIAT")):
    """Returns the conversion price between the supplied crypto and fiat currencies"""
    try:
        url = 'https://api.coinbase.com/v2/prices/{}-{}/spot'.format(crypto.upper(),
                                                                     fiat)
        req = Request(url)
        r = urlopen(req).read()
        data = json.loads(r.decode('utf-8'))
        return "1 {} = {} {} | ".format(data['data']['base'],
                                        data['data']['amount'],
                                        data['data']['currency'])
    except HTTPError:
        return "[*] error, check you are using correct crypto and fiat symbols"


def get_majors(fiat=config.get("currency", "FIAT")):
    """Returns the conversion prices for all supported crypto-currencies"""
    return [get_price(crypto.upper(), fiat) for crypto in
            cryptos]


def set_fiat(fiat):
    """Sets the default fiat currency for the user"""
    # todo: data sanitisation, restrict fiat to ISO 4217 codes
    try:
        config.set('currency', 'FIAT', fiat)
        with open(config_filename, 'w') as configfile:
            config.write(configfile)
        return "[*] {} configured as standard fiat".format(fiat)
    except Exception as e:
        return "[*] error while configuring fiat, report: ", e


def record_data(section, base, amount):
    """Helper function to sanitise and save data to config.ini"""
    try:
        if float(amount) >= 0:
            config.set(section, base, str(amount))
            with open(config_filename, 'w') as configfile:
                config.write(configfile)
            if section == "portfolio":
                print("[*] {} portfolio value set at {} coins".format(base.upper(), amount))
        else:
            print("HODL: error: invalid choice: {} (please supply a positive number)".format(amount))
    except ValueError:
        print("HODL: error: invalid choice: {} (please supply a number)".format(amount))


def print_portfolio_value(base=None):
    """Prints the value of the user's portfolio holdings"""
    portfolio_currency = config.get("currency", "FIAT")
    if base:
        holding = float(config.get("portfolio", base)) * float(config.get("readings", base))
        print("[*] {} portfolio value: ".format(base.upper()) +
              "{0:.2f} ".format(holding) +
              "{}".format(portfolio_currency))
    else:
        for base in ["btc", "bch", "eth", "ltc"]:
            holding = float(config.get("portfolio", base)) * float(config.get("readings", base))
            print("[*] {} portfolio value: ".format(base.upper()) +
                  "{0:.2f} ".format(holding) +
                  "{}".format(portfolio_currency))


def print_report(report):
    """Prints a crypto-currency exchange rate report"""
    try:
        if "[*] error, check you are using correct crypto and fiat symbols" in report:
            print(report)
        else:
            base = report.split("=")[0].split(" ")[1]
            current_amount = float(report.split("=")[1].split(" ")[1])
            # recover cached record
            previous_amount = float(config.get("readings", base.upper()))
            if current_amount > previous_amount:
                change = Fore.GREEN + "{0:.2f}% increase".format(100.0 * current_amount / previous_amount - 100)
                print(report + change)
            elif current_amount < previous_amount:
                change = Fore.RED + "{0:.2f}% decrease".format(100.0 * current_amount / previous_amount - 100)
                print(report + change)
            elif current_amount == previous_amount:
                change = Fore.YELLOW + "no change"
                print(report + change)
            record_data("readings", base, str(current_amount))
    except ZeroDivisionError:
        base = report.split("=")[0].split(" ")[1]
        current_amount = float(report.split("=")[1].split(" ")[1])
        record_data("readings", base, str(current_amount))
        print_report(report=report)


def main():
    """Main program entry point; parses and interprets command line arguments"""
    parser = argparse.ArgumentParser(prog="HODL", description=description, epilog=epilog)
    group = parser.add_mutually_exclusive_group()
    parser.add_argument("-cp", "--configure_portfolio", help="configure portfolio command",
                        nargs=2, metavar=('CRYPTOCURRENCY', 'AMOUNT'))
    parser.add_argument("-vp", "--view_portfolio", help="view portfolio command", const='all', nargs="?")
    parser.add_argument('-c', '--crypto',
                        help='set the crypto-currency you wish to price check',
                        choices=cryptos)
    group.add_argument('-f', '--fiat',
                       help='set the fiat currency you wish to use for comparison')
    group.add_argument('-sf', '--set_fiat',
                       help='set your preferred fiat currency')
    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s {version}'.format(
                            version=__version__))
    args = parser.parse_args()

    if args.crypto and args.fiat:
        print_report(get_price(args.crypto, args.fiat))
    elif (args.set_fiat and args.crypto) or (args.crypto and args.set_fiat):
        print(set_fiat(args.set_fiat))
        print_report(get_price(args.crypto))
    elif args.crypto:
        print_report(get_price(args.crypto))
    elif args.set_fiat:
        print(set_fiat(args.set_fiat))
    elif args.configure_portfolio:
        if args.configure_portfolio[0] in cryptos:
            record_data("portfolio", args.configure_portfolio[0], args.configure_portfolio[1])
        else:
            print("HODL: error: argument -cp/--configure_portfolio: invalid choice:"
                  " '{}' (choose from 'btc', 'bch', 'eth', 'ltc')".format(args.configure_portfolio[0]))
    elif args.view_portfolio:
        if args.view_portfolio == "all":
            print_portfolio_value()
        else:
            if args.view_portfolio in cryptos:
                print_portfolio_value(args.view_portfolio)
            else:
                print("HODL: error: argument -vp/--view_portfolio: invalid choice:"
                      " '{}' (choose from 'btc', 'bch', 'eth', 'ltc')".format(args.view_portfolio))
    else:
        for report in get_majors():
            print_report(report)


if __name__ == '__main__':
    main()
