from datetime import date, datetime, time, timedelta, timezone
from os import chdir, getcwd, popen
from pathlib import Path
from sys import version_info
from unittest import TestCase, skipIf

from datetype import (
    AwareDateTime,
    NaiveDateTime,
    NaiveTime,
    Time,
    aware,
    naive,
    DateTime,
)

TEST_DATA = (Path(__file__) / "..").resolve()
while not (TEST_DATA / ".git").is_dir():
    TEST_DATA = TEST_DATA / ".."
TEST_DATA = TEST_DATA.resolve()


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

    def test_attributes(self) -> None:
        naiveDT = naive(datetime(2023, 11, 1, 5, 4, 3))
        self.assertEqual(naiveDT.year, 2023)
        self.assertEqual(naiveDT.month, 11)
        self.assertEqual(naiveDT.day, 1)

    def test_mypy_output(self) -> None:
        """
        Make sure that we get expected mypy errors.
        """
        mypy_command = "mypy"
        expected_file_name = (
            TEST_DATA / f"expected_mypy{'_37' if (version_info < (3, 8)) else ''}"
        )
        if version_info < (3, 9):
            mypy_command += " --ignore-missing-imports"  # zoneinfo

        cwd = getcwd()
        try:
            chdir(TEST_DATA)
            it = popen(f"{mypy_command} tryit.py")
        finally:
            chdir(cwd)
        with it as f:
            actual = f.read()
        with expected_file_name.with_suffix(".txt").open() as f:
            expected = f.read()
        self.maxDiff = 9999
        self.assertEqual(expected, actual)

    @skipIf(version_info < (3, 9), "ZoneInfo")
    def test_none_aware(self) -> None:
        """
        L{aware} with no argument will produce a ZoneInfo.
        """
        from zoneinfo import ZoneInfo

        zi = ZoneInfo("US/Pacific")
        stddt = datetime(2025, 2, 13, 15, 35, 13, 574354, tzinfo=zi)
        awareified = aware(stddt)
        self.assertIs(awareified.tzinfo, zi)
        self.assertEqual(awareified.tzinfo.dst(stddt), timedelta(0))

    @skipIf(version_info < (3, 9), "ZoneInfo")
    def test_differing_zone_subtract(self) -> None:
        from zoneinfo import ZoneInfo

        zi = ZoneInfo("US/Pacific")
        stddt = datetime(2025, 2, 13, 15, 35, 13, 574354, tzinfo=zi)
        inutc = stddt.astimezone(timezone.utc)

        dtzi: DateTime[ZoneInfo] = aware(stddt, ZoneInfo)
        dttz: DateTime[timezone] = aware(inutc, timezone)

        self.assertEqual(dtzi - dttz, timedelta(0))
        self.assertEqual(dttz - dtzi, timedelta(0))
