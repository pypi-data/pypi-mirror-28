import requests
import json

currencies = {
    "usd": u"\u0024",
    "eur": u"\u20AC",
    "aud": u"\u0024",
    "gbp": u"\u00A3",
    "jpy": u"\u00A5",
    "brl": u"R\u0024",
    "cad": u"\u0024",
    "chf": u"CHF",
    "clp": u"\u0024",
    "cny": u"\u00A5",
    "czk": "CZK",
    "dkk": "DKK",
    "hkd": u"HK\u0024",
    "huf": "HUF",
    "idr": "Rp",
    "ils": u"\u20AA",
    "inr": u"\u20B9",
    "krw": u"\u20A9",
    "mxn": u"\u0024",
    "myr": "MYR",
    "nok": "NOK",
    "nzd": "NZD",
    "php": u"\u20B1",
    "pkr": u"\u20A8",
    "pln": u"\u007A\u0142",
    "rub": u"\u20BD",
    "sek": "SEK",
    "sgd": u"S\u0024",
    "thb": u"\u0E3F",
    "try": u"\u20BA",
    "twd": u"NT\u0024",
    "zar": "ZAR",
    "btc": u"\u0243"
}


def get_price(*args):
    url = "https://min-api.cryptocompare.com/data/price?fsym=ARK&tsyms="
    try:
        for currency in args:
            url += currency.upper() + ','
        r = json.loads(requests.get(url[:-1]).text)
        return r
    except requests.ConnectionError:
        return 1


def output_price(*args):
    for currency in args:
        print("{0} {1}".format(get_price(currency)[currency.upper()], currencies.get(currency)))