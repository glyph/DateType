from unittest import TestCase
from datetype import (
    Date,
    naive,
    aware,
    date_only,
    NaiveDateTime,
    AwareDateTime,
    NaiveTime,
    AwareTime,
)
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
        self.assertNotIsInstance(naive, (Date, NaiveTime, AwareTime))
        self.assertNotIsInstance(aware, (Date, NaiveTime, AwareTime))

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

    def test_date_only_runtime_errors(self) -> None:
        """
        Make sure date_only() returns runtime errors when passed something that
        isn't a bare date
        """
        aware_dt = datetime.now(timezone.utc)
        naive_dt = datetime.now()
        self.assertRaises(TypeError, date_only, aware_dt)
        self.assertRaises(TypeError, date_only, naive_dt)
        self.assertRaises(TypeError, date_only, naive_dt.time())
        self.assertRaises(TypeError, date_only, aware_dt.time())
        self.assertRaises(TypeError, date_only, naive_dt.timetz())
        self.assertRaises(TypeError, date_only, aware_dt.timetz())
        self.assertEqual(naive_dt.date(), date_only(naive_dt.date()))
        self.assertEqual(aware_dt.date(), date_only(aware_dt.date()))

    def test_aware_runtime_errors(self) -> None:
        """
        Make sure aware() returns runtime errors when passed something that
        isn't a timezone-aware time or datetime
        """
        aware_dt = datetime.now(timezone.utc)
        naive_dt = datetime.now()
        self.assertIs(aware_dt, aware(aware_dt))
        self.assertRaises(TypeError, aware, naive_dt)
        self.assertRaises(TypeError, aware, naive_dt.time())
        self.assertRaises(TypeError, aware, aware_dt.time())
        self.assertRaises(TypeError, aware, naive_dt.timetz())
        self.assertEqual(aware_dt.timetz(), aware(aware_dt.timetz()))
        self.assertRaises(TypeError, aware, naive_dt.date())
        self.assertRaises(TypeError, aware, aware_dt.date())

    def test_naive_runtime_errors(self) -> None:
        """
        Make sure naive() returns runtime errors when passed something that
        isn't a naive time or datetime
        """
        aware_dt = datetime.now(timezone.utc)
        naive_dt = datetime.now()
        self.assertRaises(TypeError, naive, aware_dt)
        self.assertIs(naive_dt, naive(naive_dt))
        self.assertEqual(naive_dt.time(), naive(naive_dt.time()))
        self.assertEqual(aware_dt.time(), naive(aware_dt.time()))
        self.assertEqual(naive_dt.time(), naive(naive_dt.timetz()))
        self.assertRaises(TypeError, naive, aware_dt.timetz())
        self.assertRaises(TypeError, naive, naive_dt.date())
        self.assertRaises(TypeError, naive, aware_dt.date())

    def test_aware_combine_runtime(self):
        aware_dt = datetime.now(timezone.utc)
        self.assertEqual(
            aware_dt,
            AwareDateTime.combine(aware_dt.date(), aware_dt.time(), aware_dt.tzinfo),
        )
        self.assertRaises(
            TypeError, AwareDateTime.combine, aware_dt.date(), aware_dt.time()
        )

    def test_naive_combine_runtime(self):
        aware_dt = datetime.now(timezone.utc)
        naive_dt = aware_dt.replace(tzinfo=None)
        self.assertEqual(
            naive_dt, NaiveDateTime.combine(aware_dt.date(), aware_dt.time())
        )
        self.assertRaises(
            TypeError,
            NaiveDateTime.combine,
            aware_dt.date(),
            aware_dt.time(),
            aware_dt.tzinfo,
        )
