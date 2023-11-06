from datetime import date, datetime, time, timezone
from os import popen
from typing import runtime_checkable
from unittest import TestCase

from datetype import AwareDateTime, NaiveDateTime, Time, naive


class DateTypeTests(TestCase):
    """
    Tests for datetype module.
    """

    def test_constructors(self) -> None:
        """
        Some constructors.
        """
        awareDT = AwareDateTime.now(timezone.utc)
        naiveDT = NaiveDateTime.now()
        self.assertIsInstance(awareDT, datetime)
        self.assertIsInstance(awareDT, AwareDateTime)
        self.assertNotIsInstance(awareDT, NaiveDateTime)
        self.assertIsInstance(naiveDT, datetime)
        self.assertIsInstance(naiveDT, NaiveDateTime)
        self.assertNotIsInstance(naiveDT, AwareDateTime)

    def test_methods(self) -> None:
        """
        Some methods.
        """
        naiveDT = naive(datetime(2023, 11, 1, 5, 4, 3))
        self.assertEqual(naiveDT.date(), date(2023, 11, 1))
        self.assertEqual(naiveDT.time(), naive(time(5, 4, 3)))

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
