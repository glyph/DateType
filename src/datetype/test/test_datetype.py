from unittest import TestCase
from datetype import Aware, Naive
from datetime import datetime, timezone
from os import popen


class DateTypeTests(TestCase):
    """
    Tests for datetype module.
    """

    def test_constructors(self) -> None:
        """
        Some constructors.
        """
        aware = Aware.now(timezone.utc)
        naive = Naive.now()
        self.assertIsInstance(aware, datetime)
        self.assertIsInstance(aware, Aware)
        self.assertNotIsInstance(aware, Naive)
        self.assertIsInstance(naive, datetime)
        self.assertIsInstance(naive, Naive)
        self.assertNotIsInstance(naive, Aware)

    def test_mypy_output(self) -> None:
        """
        Make sure that we get expected mypy errors.
        """
        with popen("mypy tryit.py") as f:
            actual = f.read()
        with open("expected_mypy.txt") as f:
            expected = f.read()
        self.maxDiff = 9999
        self.assertEqual(actual, expected)
