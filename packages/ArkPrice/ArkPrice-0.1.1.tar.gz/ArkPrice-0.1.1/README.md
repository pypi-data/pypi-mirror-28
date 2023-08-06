[![Build Status](https://travis-ci.org/Highjhacker/arkprice.svg?branch=master)](https://travis-ci.org/Highjhacker/arkprice)
[![HitCount](http://hits.dwyl.io/Highjhacker/priceark.svg)](http://hits.dwyl.io/Highjhacker/priceark) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) 
# ArkPrice

Fetch the price of Ark in any (crypto)currency.

## Built with
- [Python](https://www.python.org/)
- [Requests](http://docs.python-requests.org/en/master/)

## Installation

```shell
$ pip install arkprice
```

## Usage

### Fetching the price

You can fetch the price without any parameter, by default the return value will be in USD, 
or specify multiples (crypto)currency you want to use.

```python
from ArkPrice import get_price

print(get_price("eur"))
print(get_price("eur", "btc", "usd"))
>>> {'EUR': 4.41}
>>> {'EUR': 4.41, 'BTC': 0.0004976, 'USD': 5.39}
```

### Output the price

Output the price directly in the console with the correct symbol of the currency.

```python
from ArkPrice import output_price

output_price("eur", "btc", "usd")

>>> 4.46 €
>>> 0.0004994 Ƀ
>>> 5.43 $
```

## TODOS

- [x] Core code.
- [ ] Write documentation.
- [x] Unit testing.
- [x] Package it.
- [x] Travis.
    - [ ] Missing support for python 3.2.
    - [ ] OSX Support ?
    - [ ] Windows support ?
- [ ] More markets ?
    - [x] CryptoCompare
    - [ ] CoinMarketCap
    - ...

## Authors

- Jolan Beer - Highjhacker

## License

ArkPrice is under MIT license. See the [LICENSE file](https://github.com/Highjhacker/arkprice/blob/master/LICENSE) for more informations.