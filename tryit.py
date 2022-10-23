from typing import cast
from datetime import datetime, timezone, date, time
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

x: NaiveDateTime = naive(datetime.now())  # ok
y: AwareDateTime = aware(datetime.now(timezone.utc))  # ok
x < x  # ok
y > y  # ok

x < y  # error: we can't compare naive and aware

a: NaiveDateTime = aware(  # error: it's aware and we want naive
    datetime.now(timezone.utc)
)
b: AwareDateTime = naive(  # error: it's naive and we want aware
    datetime.now(timezone.utc)
)

adate: Date = date_only(date.today())  # success
bdate: Date = date_only(datetime.now(timezone.utc))  # runtime error only, sadly


cdate: Date = a  # error because datetimes aren't dates
ddate: Date = b  # error for aware too

naive_time: NaiveTime = naive(time(0))  # ok
aware_time: AwareTime = aware(time(0))  # error

AwareDateTime.combine(cdate, naive_time)  # error because sometime is naive
AwareDateTime.combine(cdate, aware_time)  # ok because b is aware


def try_nested_composition() -> None:
    # the casts should be composable
    composed_date: Date = date_only(date_only(date.today()))  # ok
    composed_naive_dt: NaiveDateTime = naive(naive(datetime.now()))  # ok
    composed_aware_dt: AwareDateTime = aware(aware(datetime.now(timezone.utc)))  # ok
    composed_naive_time: NaiveTime = naive(naive(time(0)))  # ok
    composed_aware_time: AwareTime = aware(aware(time(0, tzinfo=timezone.utc)))  # ok

    composed_date2: Date = date_only(composed_date)  # ok
    composed_naive_dt2: NaiveDateTime = naive(composed_naive_dt)  # ok
    composed_aware_dt2: AwareDateTime = aware(composed_aware_dt)  # ok
    composed_naive_time2: NaiveTime = naive(composed_naive_time)  # ok
    composed_aware_time2: AwareTime = aware(composed_aware_time)  # ok


try_nested_composition()
