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
    Type,
    TypeVar,
    cast,
    overload,
    runtime_checkable,
)


_D = TypeVar("_D", bound="Date")
_GMaybeTZT = TypeVar("_GMaybeTZT", bound=None | _tzinfo, covariant=True)
_GMaybeTZDT = TypeVar("_GMaybeTZDT", bound=None | _tzinfo, covariant=True)
_PMaybeTZ = TypeVar("_PMaybeTZ", bound=None | _tzinfo)
_FuncTZ = TypeVar("_FuncTZ", bound=_tzinfo)
_FuncOptionalTZ = TypeVar("_FuncOptionalTZ", bound=None | _tzinfo)


Self = TypeVar("Self")
AnyDateTime = TypeVar("AnyDateTime", bound="DateTime[_tzinfo | None]")
AnyTime = TypeVar("AnyTime", bound="Time[_tzinfo | None]")

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
    """
    A protocol that describes L{datetime.date}.

    (This is really just a copy of the stub for L{datetime.date} but is
    necessary to make it a C{Protocol}.)
    """

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


class Time(Protocol[_GMaybeTZT]):
    min: ClassVar[Time[None]]
    max: ClassVar[Time[None]]
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
        tzinfo: _FuncTZ,
        fold: int = ...,
    ) -> Time[_FuncTZ]:
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
    ) -> Time[None]:
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
    ) -> Time[None]:
        ...

    @overload
    def replace(
        self,
        hour: int,
        minute: int,
        second: int,
        microsecond: int,
        tzinfo: _FuncTZ,
        *,
        fold: int,
    ) -> Time[_FuncTZ]:
        ...

    if sys.version_info >= (3, 7):

        @classmethod
        def fromisoformat(cls, __time_string: str) -> Time[None | _tzinfo]:
            return cast(Time[Any], _time.fromisoformat(__time_string))


@runtime_checkable
class NaiveTime(Time[None], _CheckableProtocol, Protocol):
    """
    Time without a timezone.
    """

    if not TYPE_CHECKING:

        @classmethod
        def _subclass_check_hook(cls, instance: object) -> bool:
            return isinstance(instance, _time) and instance.tzinfo is None


@runtime_checkable
class AwareTime(Time[_tzinfo], _CheckableProtocol, Protocol):
    """
    Time with a timezone.
    """

    if not TYPE_CHECKING:

        @classmethod
        def _subclass_check_hook(cls, instance: object) -> bool:
            return isinstance(instance, _time) and instance.tzinfo is not None


DTSelf = TypeVar("DTSelf", bound="DateTime")


class DateTime(Protocol[_GMaybeTZDT]):
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

    def _date(self) -> Date:
        ...

    def time(self) -> NaiveDateTime:
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
        tzinfo: _FuncTZ,
        fold: int = ...,
    ) -> DateTime[_FuncTZ]:
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
        tzinfo: _FuncTZ,
        *,
        fold: int,
    ) -> DateTime[_FuncTZ]:
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

    def astimezone(self, tz: _FuncTZ) -> DateTime[_FuncTZ]:
        ...

    def ctime(self) -> str:
        ...

    def isoformat(self, sep: str = ..., timespec: str = ...) -> str:
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

    def timetz(self) -> DateTime[_GMaybeTZDT]:
        ...

    @classmethod
    def fromtimestamp(
        cls: type[Self], __timestamp: float, tz: _FuncOptionalTZ
    ) -> DateTime[_FuncOptionalTZ]:
        result = _datetime.fromtimestamp(__timestamp, tz)
        return result  # type: ignore[return-value]

    @overload
    @classmethod
    def now(cls, tz: _FuncOptionalTZ) -> DateTime[_FuncOptionalTZ]:
        ...

    @overload
    @classmethod
    def now(cls) -> DateTime[None]:
        ...

    @classmethod
    def now(cls, tz: _tzinfo | None = None) -> DateTime[None | _tzinfo]:
        return _datetime.now(tz)  # type: ignore[return-value]

    @overload
    @classmethod
    def combine(
        cls, date: Date, time: Time[_FuncOptionalTZ]
    ) -> DateTime[_FuncOptionalTZ]:
        ...

    @overload
    @classmethod
    def combine(
        cls, date: Date, time: Time[_tzinfo | None], tzinfo: _FuncOptionalTZ
    ) -> DateTime[_FuncOptionalTZ]:
        ...

    @classmethod
    def combine(
        cls, date: Date, time: Time[_tzinfo | None], tzinfo: _tzinfo | None = None
    ) -> DateTime[_tzinfo | None]:
        return _datetime.combine(
            concrete(date), concrete(time), tzinfo
        )  # type:ignore[return-value]

    @classmethod
    def utcfromtimestamp(cls: type[Self], __t: float) -> DateTime[None]:
        return naive(_datetime.utcfromtimestamp(__t))

    @classmethod
    def utcnow(cls: type[Self]) -> DateTime[None]:
        return naive(_datetime.utcnow())


@runtime_checkable
class NaiveDateTime(DateTime[None], _CheckableProtocol, Protocol):
    if not TYPE_CHECKING:

        @classmethod
        def _subclass_check_hook(cls, instance: object) -> bool:
            return isinstance(instance, _datetime) and instance.tzinfo is None


@runtime_checkable
class AwareDateTime(DateTime[_tzinfo], _CheckableProtocol, Protocol):
    if not TYPE_CHECKING:

        @classmethod
        def _subclass_check_hook(cls, instance: object) -> bool:
            return isinstance(instance, _datetime) and instance.tzinfo is not None


# Parsers where the tzinfo is optionally embedded in the string cannot be
# present as classmethods, because the classmethods would then inaccurately
# describe the returned concrete type


def strptime(__date_string: str, __format: str) -> DateTime[_tzinfo | None]:
    return cast(NaiveDateTime, _datetime.strptime(__date_string, __format))


if sys.version_info >= (3, 7):

    def fromisoformat(__date_string: str) -> DateTime[_tzinfo | None]:
        return cast(NaiveDateTime, _datetime.fromisoformat(__date_string))


def date_only(d: _date) -> Date:
    if isinstance(d, _datetime):
        raise TypeError(f"{type(d)} is a datetime, not a date")
    return cast(Date, d)


@overload
def aware(t: _datetime, tztype: Type[_FuncTZ]) -> DateTime[_FuncTZ]:
    ...


@overload
def aware(t: _datetime) -> AwareDateTime:
    ...


@overload
def aware(t: _time) -> AwareTime:
    ...


@overload
def aware(t: _time, tztype: Type[_FuncTZ]) -> Time[_FuncTZ]:
    ...


def aware(
    t: _datetime | _time, tztype: Type[_FuncTZ] | None = None
) -> DateTime[_FuncTZ] | Time[_FuncTZ]:
    tzcheck: Type[_tzinfo] = tztype if tztype is not None else _tzinfo
    if not isinstance(t.tzinfo, tzcheck):
        raise TypeError(f"{t} is naive, not aware")
    return t  # type: ignore[return-value]


@overload
def naive(t: _datetime) -> NaiveDateTime:
    ...


@overload
def naive(t: _time) -> NaiveTime:
    ...


def naive(t: _datetime | _time) -> NaiveDateTime | NaiveTime:
    if t.tzinfo is not None:
        raise TypeError(f"{t} is aware, not naive")
    return cast(NaiveDateTime, t)


@overload
def concrete(dt: DateTime[_tzinfo | None]) -> _datetime:
    ...


@overload
def concrete(dt: Date) -> _date:
    ...


@overload
def concrete(dt: Time[_tzinfo | None]) -> _time:
    ...


def concrete(
    dt: Date | DateTime[_tzinfo | None] | Time[_tzinfo | None],
) -> _datetime | _date | _time:
    if isinstance(dt, (_date, _time, _datetime)):
        return dt
    else:
        raise TypeError("Unreachable")
