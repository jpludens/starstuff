from unittest import TestCase
import starstuff


class Test(TestCase):
    def test_get_start_deck(self):
        expected = [
            "Scout",
            "Scout",
            "Scout",
            "Scout",
            "Scout",
            "Scout",
            "Scout",
            "Scout",
            "Viper",
            "Viper"
        ]

        actual = starstuff.get_start_deck()
        self.assertListEqual(expected, actual)