from typing import cast
from datetime import datetime, timezone, date, time
from zoneinfo import ZoneInfo
from datetype import (
    Date,
    DateTime,
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

combined_naive = DateTime.combine(cdate, naive_time)
combined_aware = DateTime.combine(cdate, aware_time)

x < combined_naive              # ok; both naive
y < combined_aware              # ok; aware
x < combined_aware              # error; naive/aware
y < combined_naive              # error; aware/naive

y.tzinfo.key                    # error; no attribute defined

specific: DateTime[ZoneInfo] = DateTime.now(ZoneInfo("America/Los_Angeles"))
specific.tzinfo.key             # ok; ZoneInfo has 'key' attribute
