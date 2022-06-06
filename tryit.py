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

naive_time: NaiveTime = naive(time(0))
aware_time: AwareTime = aware(time(0))

AwareDateTime.combine(cdate, naive_time)  # error because sometime is naive
AwareDateTime.combine(cdate, aware_time)  # ok because b is aware
