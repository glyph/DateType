from unittest import TestCase
from datetype import AwareDateTime, NaiveDateTime
from datetime import datetime, timezone
from os import popen
from typing import runtime_checkable


class DateTypeTests(TestCase):
    """
    Tests for datetype module.
    """

    def test_constructors(self) -> None:
        """
        Some constructors.
        """
        aware = AwareDateTime.now(timezone.utc)
        naive = NaiveDateTime.now()
        self.assertIsInstance(aware, datetime)
        self.assertIsInstance(aware, AwareDateTime)
        self.assertNotIsInstance(aware, NaiveDateTime)
        self.assertIsInstance(naive, datetime)
        self.assertIsInstance(naive, NaiveDateTime)
        self.assertNotIsInstance(naive, AwareDateTime)

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
