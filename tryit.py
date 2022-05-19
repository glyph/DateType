from typing import cast
from datetime import datetime, timezone, date
from datetype import date_t, as_naive, as_aware, date_only, Naive, Aware, time_t

# success
x: Naive = as_naive(datetime.now())
y: Aware = as_aware(datetime.now(timezone.utc))
x < x
y > y

# error: we can't compare naive and aware
x < y

# error: it's aware and we want naive
a: Naive = as_aware(datetime.now(timezone.utc))
b: Aware = as_naive(datetime.now(timezone.utc))

# success
adate: date_t = date_only(date.today())

# runtime error only, sadly
bdate: date_t = date_only(datetime.now(timezone.utc))

# error because once we're in more-strictly-typed we can prevent confusion
cdate: date_t = a
ddate: date_t = b

sometime: time_t[None] = cast(time_t[None], None)

what = Aware.combine(cdate, sometime)

reveal_type(what)

