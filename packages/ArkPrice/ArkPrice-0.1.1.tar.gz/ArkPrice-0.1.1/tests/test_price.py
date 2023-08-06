import unittest
from ArkPrice.price import get_price, output_price


class TestPrice(unittest.TestCase):
    def test_get_price(self):
        self.assertEqual(type(get_price()), dict)

    def test_output_price(self):
        s = output_price("eur")
        self.assertEqual(s.endswith("€"), True)

if __name__ == '__main__':
    unittest.main()