from sys import version_info
from datetime import date, datetime, time, timezone
from os import popen
from typing_extensions import runtime_checkable
from unittest import TestCase

from datetype import (
    AwareDateTime,
    AwareTime,
    NaiveDateTime,
    NaiveTime,
    Time,
    aware,
    naive,
)


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
        expectNaiveTime: NaiveTime = naiveDT.timetz()
        self.assertEqual(expectNaiveTime, naive(time(5, 4, 3)))
        awareDT = aware(datetime(2023, 11, 1, 5, 4, 3, tzinfo=timezone.utc), timezone)
        expectAwareTime: Time[timezone] = awareDT.timetz()
        self.assertEqual(
            expectAwareTime, aware(time(5, 4, 3, tzinfo=timezone.utc), timezone)
        )

    def test_mypy_output(self) -> None:
        """
        Make sure that we get expected mypy errors.
        """
        mypy_command = "mypy"
        expected_file_name = "expected_mypy"
        if version_info < (3, 9):
            mypy_command += " --ignore-missing-imports"
        if version_info[:2] == (3, 7):
            expected_file_name += "_37"

        with popen(f"{mypy_command} tryit.py") as f:
            actual = f.read()
        with open(f"{expected_file_name}.txt") as f:
            expected = f.read()
        self.maxDiff = 9999
        self.assertEqual(expected, actual)
