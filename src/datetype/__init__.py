from __future__ import annotations

import sys
from time import struct_time
from typing import ClassVar, NamedTuple, TypeVar, overload, Protocol
from typing import cast, Any

from datetime import datetime, timedelta, tzinfo as _tzinfo, date, time

_D = TypeVar("_D", bound="date_t")
_GMaybeTZT = TypeVar("_GMaybeTZT", bound=None | _tzinfo, covariant=True)
_GMaybeTZDT = TypeVar("_GMaybeTZDT", bound=None | _tzinfo, covariant=True)
_PMaybeTZ = TypeVar("_PMaybeTZ", bound=None | _tzinfo)
Self = TypeVar("Self")

if sys.version_info >= (3, 9):

    class _IsoCalendarDate(NamedTuple):
        year: int
        week: int
        weekday: int


class date_t(Protocol):
    min: ClassVar[date_t]
    max: ClassVar[date_t]
    resolution: ClassVar[timedelta]

    @classmethod
    def fromtimestamp(cls, __timestamp: float) -> date_t:
        return date_only(date.today())

    @classmethod
    def today(cls) -> date_t:
        return date_only(date.today())

    @classmethod
    def fromordinal(cls, __n: int) -> date_t:
        return date_only(date.fromordinal(__n))

    if sys.version_info >= (3, 7):

        @classmethod
        def fromisoformat(cls, __date_string: str) -> date_t:
            return date_only(date.fromisoformat(__date_string))

    if sys.version_info >= (3, 8):

        @classmethod
        def fromisocalendar(cls, year: int, week: int, day: int) -> date_t:
            return date_only(date.fromisocalendar(year, week, day))

    @property
    def year(self) -> int:
        ...

    @property
    def month(self) -> int:
        ...

    @property
    def day(self) -> int:
        ...

    def ctime(self) -> str:
        ...

    def strftime(self, __format: str) -> str:
        ...

    def __format__(self, __fmt: str) -> str:
        ...

    def isoformat(self) -> str:
        ...

    def timetuple(self) -> struct_time:
        ...

    def toordinal(self) -> int:
        ...

    def replace(self: Self, year: int = ..., month: int = ..., day: int = ...) -> Self:
        ...

    def __le__(self, __other: date_t) -> bool:
        ...

    def __lt__(self, __other: date_t) -> bool:
        ...

    def __ge__(self, __other: date_t) -> bool:
        ...

    def __gt__(self, __other: date_t) -> bool:
        ...

    if sys.version_info >= (3, 8):

        def __add__(self: Self, __other: timedelta) -> Self:
            ...

        def __radd__(self: Self, __other: timedelta) -> Self:
            ...

        @overload
        def __sub__(self: Self, __other: timedelta) -> Self:
            ...

        @overload
        def __sub__(self: _D, __other: _D) -> timedelta:
            ...

    else:
        # Prior to Python 3.8, arithmetic operations always returned `date`, even in subclasses
        def __add__(self, __other: timedelta) -> date_t:
            ...

        def __radd__(self, __other: timedelta) -> date_t:
            ...

        @overload
        def __sub__(self, __other: timedelta) -> date_t:
            ...

    def __hash__(self) -> int:
        ...

    def weekday(self) -> int:
        ...

    def isoweekday(self) -> int:
        ...

    if sys.version_info >= (3, 9):

        def isocalendar(self) -> _IsoCalendarDate:
            ...

    else:

        def isocalendar(self) -> tuple[int, int, int]:
            ...


class time_t(Protocol[_GMaybeTZT]):
    min: ClassVar[time_t]
    max: ClassVar[time_t]
    resolution: ClassVar[timedelta]

    @property
    def hour(self) -> int:
        ...

    @property
    def minute(self) -> int:
        ...

    @property
    def second(self) -> int:
        ...

    @property
    def microsecond(self) -> int:
        ...

    @property
    def tzinfo(self) -> _GMaybeTZT:
        ...

    @property
    def fold(self) -> int:
        ...

    def __le__(self: Self, __other: Self) -> bool:
        ...

    def __lt__(self: Self, __other: Self) -> bool:
        ...

    def __ge__(self: Self, __other: Self) -> bool:
        ...

    def __gt__(self: Self, __other: Self) -> bool:
        ...

    def __hash__(self) -> int:
        ...

    def isoformat(self, timespec: str = ...) -> str:
        ...

    if sys.version_info >= (3, 7):

        @classmethod
        def fromisoformat(cls, __time_string: str) -> time_t[None | _tzinfo]:
            return cast(time_t, time.fromisoformat(__time_string))

    def strftime(self, __format: str) -> str:
        ...

    def __format__(self, __fmt: str) -> str:
        ...

    def utcoffset(self) -> timedelta | None:
        ...

    def tzname(self) -> str | None:
        ...

    def dst(self) -> timedelta | None:
        ...

    @overload
    def replace(
        self: Self,
        hour: int = ...,
        minute: int = ...,
        second: int = ...,
        microsecond: int = ...,
        *,
        fold: int = ...,
    ) -> Self:
        ...

    @overload
    def replace(
        self,
        hour: int = ...,
        minute: int = ...,
        second: int = ...,
        microsecond: int = ...,
        *,
        tzinfo: _PMaybeTZ,
        fold: int = ...,
    ) -> time_t[_PMaybeTZ]:
        ...

    @overload
    def replace(
        self,
        hour: int,
        minute: int,
        second: int,
        microsecond: int,
        tzinfo: _PMaybeTZ,
        *,
        fold: int,
    ) -> time_t[_PMaybeTZ]:
        ...


DTSelf = TypeVar("DTSelf", bound="datetime_t")


class datetime_t(Protocol[_GMaybeTZDT]):
    resolution: ClassVar[timedelta]

    @property
    def hour(self) -> int:
        ...

    @property
    def minute(self) -> int:
        ...

    @property
    def second(self) -> int:
        ...

    @property
    def microsecond(self) -> int:
        ...

    @property
    def tzinfo(self) -> _GMaybeTZDT:
        ...

    @property
    def fold(self) -> int:
        ...

    def timestamp(self) -> float:
        ...

    def utctimetuple(self) -> struct_time:
        ...

    def date(self) -> date_t:
        ...

    def time(self) -> time_t[None]:
        ...

    def timetz(self) -> time_t[_GMaybeTZDT]:
        ...

    @overload
    def replace(
        self,
        year: int = ...,
        month: int = ...,
        day: int = ...,
        hour: int = ...,
        minute: int = ...,
        second: int = ...,
        microsecond: int = ...,
        *,
        tzinfo: _tzinfo,
        fold: int = ...,
    ) -> Aware:
        ...

    @overload
    def replace(
        self,
        year: int,
        month: int,
        day: int,
        hour: int,
        minute: int,
        second: int,
        microsecond: int,
        tzinfo: _tzinfo,
        *,
        fold: int,
    ) -> Aware:
        ...

    @overload
    def replace(
        self,
        year: int = ...,
        month: int = ...,
        day: int = ...,
        hour: int = ...,
        minute: int = ...,
        second: int = ...,
        microsecond: int = ...,
        *,
        tzinfo: None,
        fold: int = ...,
    ) -> Naive:
        ...

    @overload
    def replace(
        self: Self,
        year: int,
        month: int,
        day: int,
        hour: int,
        minute: int,
        second: int,
        microsecond: int,
        tzinfo: None,
        *,
        fold: int,
    ) -> Naive:
        ...

    @overload
    def replace(
        self: Self,
        year: int = ...,
        month: int = ...,
        day: int = ...,
        hour: int = ...,
        minute: int = ...,
        second: int = ...,
        microsecond: int = ...,
        *,
        fold: int = ...,
    ) -> Self:
        "If no replacement tz is specified then we inherit"

    @overload
    def astimezone(self, tz: _tzinfo) -> Aware:
        ...

    @overload
    def astimezone(self, tz: None) -> Naive:
        ...

    @overload
    def astimezone(self: Self) -> Self:
        ...

    def ctime(self) -> str:
        ...

    def isoformat(self, sep: str = ..., timespec: str = ...) -> str:
        ...

    def utcoffset(self) -> timedelta | None:
        ...

    def tzname(self) -> str | None:
        ...

    def dst(self) -> timedelta | None:
        ...

    def __le__(self: Self, __other: Self) -> bool:
        ...

    def __lt__(self: Self, __other: Self) -> bool:
        ...

    def __ge__(self: Self, __other: Self) -> bool:
        ...

    def __gt__(self: Self, __other: Self) -> bool:
        ...

    @overload
    def __sub__(self: Self, __other: timedelta) -> Self:
        ...

    @overload
    def __sub__(self: DTSelf, __other: DTSelf) -> timedelta:
        ...

    def __add__(self: Self, __other: timedelta) -> Self:
        ...

    def __radd__(self: Self, __other_t: timedelta) -> Self:
        ...

    if sys.version_info >= (3, 9):

        def isocalendar(self) -> _IsoCalendarDate:
            ...

    else:

        def isocalendar(self) -> tuple[int, int, int]:
            ...


class Naive(datetime_t[None], Protocol):

    # Naive-*only* methods
    @classmethod
    def utcfromtimestamp(cls: type[Self], __t: float) -> Naive:
        return as_naive(datetime.utcfromtimestamp(__t))

    @classmethod
    def utcnow(cls: type[Self]) -> Naive:
        return as_naive(datetime.utcnow())

    # Common Methods

    @classmethod
    def fromtimestamp(cls: type[Self], __timestamp: float, tz: None = None) -> Naive:
        return as_naive(datetime.fromtimestamp(__timestamp, tz))

    @classmethod
    def now(
        cls: type[Self],
        tz: None = None,
    ) -> Naive:
        return as_naive(datetime.now(tz))

    @overload
    @classmethod
    def combine(cls, date: date_t, time: time_t[Any], _tzinfo: None) -> Naive:
        ...

    @overload
    @classmethod
    def combine(cls, date: date_t, time: time_t[None]) -> Naive:
        ...

    @classmethod
    def combine(cls, date: date_t, time: time_t[Any], _tzinfo: None | _tzinfo = None) -> Naive:
        return as_naive(datetime.combine(concrete(date), concrete(time), _tzinfo))


class Aware(datetime_t[_tzinfo], Protocol):
    @classmethod
    def fromtimestamp(cls: type[Self], __timestamp: float, tz: _tzinfo) -> Aware:
        return as_aware(datetime.fromtimestamp(__timestamp, tz))

    @classmethod
    def now(cls, tz: _tzinfo) -> Aware:
        return as_aware(datetime.now(tz))

    @overload
    @classmethod
    def combine(cls, date: date_t, time: time_t[Any], _tzinfo: _tzinfo) -> Aware:
        ...

    @overload
    @classmethod
    def combine(cls, date: date_t, time: time_t[_tzinfo]) -> Aware:
        ...

    @classmethod
    def combine(cls, date: date_t, time: time_t[Any], _tzinfo: None | _tzinfo = None) -> Aware:
        return as_aware(datetime.combine(concrete(date), concrete(time), _tzinfo))


# Parsers where the tzinfo is optionally embedded in the string cannot be
# present as classmethods, because the classmethods would then inaccurately
# describe the returned concrete type

def strptime(__date_string: str, __format: str) -> Aware | Naive:
    return cast(Naive, datetime.strptime(__date_string, __format))


if sys.version_info >= (3, 7):
    def fromisoformat(__date_string: str) -> Aware | Naive:
        return cast(Naive, datetime.fromisoformat(__date_string))

def date_only(d: date) -> date_t:
    if isinstance(d, datetime):
        raise TypeError(f"{type(d)} is a datetime, not a date")
    return cast(date_t, d)


def as_aware(dt: datetime) -> Aware:
    if dt.tzinfo is None:
        raise TypeError(f"{dt} is naive, not aware")
    return cast(Aware, dt)


def as_naive(dt: datetime) -> Naive:
    if dt.tzinfo is not None:
        raise TypeError(f"{dt} is aware, not naive")
    return cast(Naive, dt)

@overload
def concrete(dt: datetime_t[None | _tzinfo]) -> datetime:
    ...

@overload
def concrete(dt: date_t) -> date:
    ...

@overload
def concrete(dt: time_t) -> time:
    ...


def concrete(dt: datetime_t[None | _tzinfo] | date_t | time_t) -> datetime | date | time:
    if isinstance(dt, (date, time)):
        return dt
    else:
        raise TypeError("Unreachable")
