from __future__ import annotations

import sys
from datetime import (
    date as _date,
    datetime as _datetime,
    time as _time,
    timedelta as _timedelta,
    tzinfo as _tzinfo,
)
from time import struct_time
from typing import (
    Any,
    ClassVar,
    NamedTuple,
    Protocol,
    TYPE_CHECKING,
    TypeVar,
    cast,
    overload,
    runtime_checkable,
)

_D = TypeVar("_D", bound="Date")
_GMaybeTZT = TypeVar("_GMaybeTZT", bound=None | _tzinfo, covariant=True)
_GMaybeTZDT = TypeVar("_GMaybeTZDT", bound=None | _tzinfo, covariant=True)
_PMaybeTZ = TypeVar("_PMaybeTZ", bound=None | _tzinfo)
Self = TypeVar("Self")
AnyDateTime = TypeVar("AnyDateTime", "AwareDateTime", "NaiveDateTime")
AnyTime = TypeVar("AnyTime", "AwareTime", "NaiveTime")

if sys.version_info >= (3, 9):

    class _IsoCalendarDate(NamedTuple):
        year: int
        week: int
        weekday: int


if not TYPE_CHECKING:

    class _CheckableProtocolMeta(type(Protocol)):
        def __instancecheck__(self, instance: object) -> bool:
            """
            'AwareDateTime' objects are datetimes with a timezone.
            """
            return self._subclass_check_hook(instance)

    class _CheckableProtocol(Protocol, metaclass=_CheckableProtocolMeta):
        pass

else:

    class _CheckableProtocol(Protocol):
        pass


@runtime_checkable
class Date(_CheckableProtocol, Protocol):
    @classmethod
    def _subclass_check_hook(cls, instance: object) -> bool:
        return type(instance) is _date

    min: ClassVar[Date]
    max: ClassVar[Date]
    resolution: ClassVar[_timedelta]

    @classmethod
    def fromtimestamp(cls, __timestamp: float) -> Date:
        return date_only(_date.today())

    @classmethod
    def today(cls) -> Date:
        return date_only(_date.today())

    @classmethod
    def fromordinal(cls, __n: int) -> Date:
        return date_only(_date.fromordinal(__n))

    if sys.version_info >= (3, 7):

        @classmethod
        def fromisoformat(cls, __date_string: str) -> Date:
            return date_only(_date.fromisoformat(__date_string))

    if sys.version_info >= (3, 8):

        @classmethod
        def fromisocalendar(cls, year: int, week: int, day: int) -> Date:
            return date_only(_date.fromisocalendar(year, week, day))

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

    def __le__(self, __other: Date) -> bool:
        ...

    def __lt__(self, __other: Date) -> bool:
        ...

    def __ge__(self, __other: Date) -> bool:
        ...

    def __gt__(self, __other: Date) -> bool:
        ...

    if sys.version_info >= (3, 8):

        def __add__(self: Self, __other: _timedelta) -> Self:
            ...

        def __radd__(self: Self, __other: _timedelta) -> Self:
            ...

        @overload
        def __sub__(self: Self, __other: _timedelta) -> Self:
            ...

        @overload
        def __sub__(self: _D, __other: _D) -> _timedelta:
            ...

    else:
        # Prior to Python 3.8, arithmetic operations always returned `_date`, even in subclasses
        def __add__(self, __other: _timedelta) -> Date:
            ...

        def __radd__(self, __other: _timedelta) -> Date:
            ...

        @overload
        def __sub__(self, __other: _timedelta) -> Date:
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


class _GenericTime(Protocol[_GMaybeTZT]):
    min: ClassVar[NaiveDateTime]
    max: ClassVar[NaiveDateTime]
    resolution: ClassVar[_timedelta]

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

    def strftime(self, __format: str) -> str:
        ...

    def __format__(self, __fmt: str) -> str:
        ...

    def utcoffset(self) -> _timedelta | None:
        ...

    def tzname(self) -> str | None:
        ...

    def dst(self) -> _timedelta | None:
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
        tzinfo: _tzinfo,
        fold: int = ...,
    ) -> AwareTime:
        ...

    @overload
    def replace(
        self,
        hour: int = ...,
        minute: int = ...,
        second: int = ...,
        microsecond: int = ...,
        *,
        tzinfo: None,
        fold: int = ...,
    ) -> NaiveTime:
        ...

    @overload
    def replace(
        self,
        hour: int,
        minute: int,
        second: int,
        microsecond: int,
        tzinfo: None,
        *,
        fold: int,
    ) -> NaiveTime:
        ...

    @overload
    def replace(
        self,
        hour: int,
        minute: int,
        second: int,
        microsecond: int,
        tzinfo: _tzinfo,
        *,
        fold: int,
    ) -> AwareTime:
        ...

    if sys.version_info >= (3, 7):

        @classmethod
        def fromisoformat(cls, __time_string: str) -> NaiveTime | AwareTime:
            return cast(NaiveTime | AwareTime, _time.fromisoformat(__time_string))


@runtime_checkable
class NaiveTime(_GenericTime[None], _CheckableProtocol, Protocol):
    """
    Time with a timezone.
    """

    if not TYPE_CHECKING:

        @classmethod
        def _subclass_check_hook(cls, instance: object) -> bool:
            return isinstance(instance, _time) and instance.tzinfo is None


@runtime_checkable
class AwareTime(_GenericTime[_tzinfo], _CheckableProtocol, Protocol):
    """
    Time without a timezone.
    """

    if not TYPE_CHECKING:

        @classmethod
        def _subclass_check_hook(cls, instance: object) -> bool:
            return isinstance(instance, _time) and instance.tzinfo is not None


DTSelf = TypeVar("DTSelf", bound="_GenericDateTime")


class _GenericDateTime(Protocol[_GMaybeTZDT]):
    resolution: ClassVar[_timedelta]

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

    def date(self) -> Date:
        ...

    def time(self) -> NaiveTime:
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
    ) -> AwareDateTime:
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
    ) -> AwareDateTime:
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
    ) -> NaiveDateTime:
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
    ) -> NaiveDateTime:
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
    def astimezone(self, tz: _tzinfo) -> AwareDateTime:
        ...

    @overload
    def astimezone(self, tz: None) -> NaiveDateTime:
        ...

    @overload
    def astimezone(self: Self) -> Self:
        ...

    def ctime(self) -> str:
        ...

    def isoformat(self, sep: str = ..., timespec: str = ...) -> str:
        ...

    def strftime(self, __format: str) -> str:
        ...

    def utcoffset(self) -> _timedelta | None:
        ...

    def tzname(self) -> str | None:
        ...

    def dst(self) -> _timedelta | None:
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
    def __sub__(self: Self, __other: _timedelta) -> Self:
        ...

    @overload
    def __sub__(self: DTSelf, __other: DTSelf) -> _timedelta:
        ...

    def __add__(self: Self, __other: _timedelta) -> Self:
        ...

    def __radd__(self: Self, __other_t: _timedelta) -> Self:
        ...

    if sys.version_info >= (3, 9):

        def isocalendar(self) -> _IsoCalendarDate:
            ...

    else:

        def isocalendar(self) -> tuple[int, int, int]:
            ...


@runtime_checkable
class NaiveDateTime(_GenericDateTime[None], _CheckableProtocol, Protocol):
    def timetz(self) -> NaiveTime:
        ...

    # NaiveDateTime-*only* methods
    @classmethod
    def utcfromtimestamp(cls: type[Self], __t: float) -> NaiveDateTime:
        return naive(_datetime.utcfromtimestamp(__t))

    @classmethod
    def utcnow(cls: type[Self]) -> NaiveDateTime:
        return naive(_datetime.utcnow())

    # Common Methods

    @classmethod
    def fromtimestamp(
        cls: type[Self], __timestamp: float, tz: None = None
    ) -> NaiveDateTime:
        return naive(_datetime.fromtimestamp(__timestamp, tz))

    @classmethod
    def now(
        cls: type[Self],
        tz: None = None,
    ) -> NaiveDateTime:
        return naive(_datetime.now(tz))

    @overload
    @classmethod
    def combine(
        cls, date: Date, time: NaiveTime | AwareTime, tzinfo: None
    ) -> NaiveDateTime:
        ...

    @overload
    @classmethod
    def combine(cls, date: Date, time: NaiveTime) -> NaiveDateTime:
        ...

    @classmethod
    def combine(
        cls, date: Date, time: NaiveTime | AwareTime, tzinfo: None | _tzinfo = None
    ) -> NaiveDateTime:
        return naive(_datetime.combine(concrete(date), concrete(time), tzinfo))

    if not TYPE_CHECKING:

        @classmethod
        def _subclass_check_hook(cls, instance: object) -> bool:
            return isinstance(instance, _datetime) and instance.tzinfo is None


@runtime_checkable
class AwareDateTime(_GenericDateTime[_tzinfo], _CheckableProtocol, Protocol):
    def timetz(self) -> AwareTime:
        ...

    @classmethod
    def fromtimestamp(
        cls: type[Self], __timestamp: float, tz: _tzinfo
    ) -> AwareDateTime:
        return aware(_datetime.fromtimestamp(__timestamp, tz))

    @classmethod
    def now(cls, tz: _tzinfo) -> AwareDateTime:
        return aware(_datetime.now(tz))

    @overload
    @classmethod
    def combine(
        cls, date: Date, time: NaiveTime | AwareTime, tzinfo: _tzinfo
    ) -> AwareDateTime:
        ...

    @overload
    @classmethod
    def combine(cls, date: Date, time: AwareTime) -> AwareDateTime:
        ...

    @classmethod
    def combine(
        cls, date: Date, time: NaiveTime | AwareTime, tzinfo: None | _tzinfo = None
    ) -> AwareDateTime:
        return aware(_datetime.combine(concrete(date), concrete(time), tzinfo))

    if not TYPE_CHECKING:

        @classmethod
        def _subclass_check_hook(cls, instance: object) -> bool:
            return isinstance(instance, _datetime) and instance.tzinfo is not None


# Parsers where the tzinfo is optionally embedded in the string cannot be
# present as classmethods, because the classmethods would then inaccurately
# describe the returned concrete type


def strptime(__date_string: str, __format: str) -> AwareDateTime | NaiveDateTime:
    return cast(NaiveDateTime, _datetime.strptime(__date_string, __format))


if sys.version_info >= (3, 7):

    def fromisoformat(__date_string: str) -> AwareDateTime | NaiveDateTime:
        return cast(NaiveDateTime, _datetime.fromisoformat(__date_string))


def date_only(d: _date | Date) -> Date:
    if isinstance(d, _datetime):
        raise TypeError(f"{type(d)} is a datetime, not a date")
    elif not isinstance(d, Date):
        raise TypeError(f"{type(d)} is not a date")
    return cast(Date, d)


@overload
def aware(t: _datetime | AwareDateTime) -> AwareDateTime:
    ...


@overload
def aware(t: _time | AwareTime) -> AwareTime:
    ...


def aware(
    t: _datetime | _time | AwareDateTime | AwareTime,
) -> AwareDateTime | AwareTime:
    if not isinstance(t, (AwareDateTime, AwareTime)):
        if hasattr(t, "tzinfo") and t.tzinfo is None:
            raise TypeError(f"{t} is naive, not aware")
        raise TypeError(f"expected tz-aware datetime or tz-aware time: {t}")
    return cast(AwareDateTime, t)


@overload
def naive(t: _datetime | NaiveDateTime) -> NaiveDateTime:
    ...


@overload
def naive(t: _time | NaiveTime) -> NaiveTime:
    ...


def naive(
    t: _datetime | _time | NaiveDateTime | NaiveTime,
) -> NaiveDateTime | NaiveTime:
    if not isinstance(t, (NaiveDateTime, NaiveTime)):
        if getattr(t, "tzinfo", None) is not None:
            raise TypeError(f"{t} is aware, not naive")
        raise TypeError(f"expected naive datetime or naive time: {t}")
    return cast(NaiveDateTime, t)


@overload
def concrete(dt: AwareDateTime | NaiveDateTime) -> _datetime:
    ...


@overload
def concrete(dt: Date) -> _date:
    ...


@overload
def concrete(dt: AwareTime | NaiveTime) -> _time:
    ...


def concrete(
    dt: Date | AwareDateTime | AwareTime | NaiveDateTime | NaiveTime,
) -> _datetime | _date | _time:
    if isinstance(dt, (_date, _time, _datetime)):
        return dt
    else:
        raise TypeError("Unreachable")
