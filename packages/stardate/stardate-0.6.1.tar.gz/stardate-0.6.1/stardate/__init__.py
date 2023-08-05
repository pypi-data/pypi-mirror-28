import datetime
import dateutil.tz
import os

__year_cache = {}
__tz_cache = {}
__utc = dateutil.tz.tzutc()

def __gettz(tz):
    if tz in __tz_cache:
        return __tz_cache[tz]
    z = dateutil.tz.gettz(tz)
    if z.__class__.__name__ != 'tzfile':
        raise ValueError("No such time zone: {}".format(tz))
    __tz_cache[tz] = z
    return(z)

def __year2datetime(y):
    if y in __year_cache:
        return __year_cache[y]
    z = datetime.datetime(y, 1, 1, 0, 0, 0, 0, tzinfo=__utc)
    __year_cache[y] = z
    return z

def datetime2stardate(x):
    a = x.astimezone(__utc)
    y0 = a.year
    t0 = __year2datetime(y0)
    t1 = __year2datetime(y0 + 1)
    sd = y0 + (a - t0)/(t1 - t0)
    return sd    

def stardate2datetime(x, tz):
    y0 = int(x)
    t0 = __year2datetime(y0)
    t1 = __year2datetime(y0 + 1)
    return (t0 + (x - y0) * (t1 - t0)).astimezone(__gettz(tz))

def getmtime(p):
    m = os.path.getmtime(p)
    dt = datetime.datetime.utcfromtimestamp(m).replace(tzinfo=__utc)
    return datetime2stardate(dt)

def stardate(*,
        year, month, day,
        hour=12, minute=0, second=0, microsecond=0,
        digits=None,
        tz):
    x = datetime.datetime(
        int(year),
        int(month),
        int(day),
        int(hour),
        int(minute),
        int(second),
        int(microsecond),
        tzinfo = __gettz(tz))
    sd = datetime2stardate(x)
    if not digits:
        return sd
    else:
        fmt = "{0:." + str(digits) + "f}"
        return fmt.format(sd)

