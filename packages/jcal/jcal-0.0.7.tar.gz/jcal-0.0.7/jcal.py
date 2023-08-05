import calendar as clndr, datetime, sys

def holiday(year):
    """Japanese holiday @2016"""
    res, t = [], datetime.timedelta(1)
    sp = int(20.8431 + 0.242194 * (year - 1980) - (int)((year - 1980) / 4))
    au = int(23.2488 + 0.242194 * (year - 1980) - (int)((year - 1980) / 4))
    hs = ((1, 1), (1, -2), (2, 11), (3, sp), (4, 29), (5, 3), (5, 4), (5, 5),
          (7, -3), (8, 11), (9, -3), (9, au), (10, -2), (11, 3), (11, 23), (12, 23))
    for m, d in hs:
        dt = datetime.date(year, m, max(1, d))
        if d < 0:
            dt += ((7 - dt.weekday()) % 7 + 7 * (-1 - d)) * t
        if dt.weekday() == 6: dt += t
        while dt in res: dt += t
        res.append(dt)
    res = sorted(res)
    for d1, d2 in zip(res[:-1], res[1:]):
        if (d2 - d1).days == 2: res.append(d1 + datetime.timedelta(1))
    return set(res)

class ColorTextCalendar(clndr.TextCalendar):
    _theyear = -1
    _holiday = {}
    _themonth = -1
    @staticmethod
    def _set_theyear(theyear):
        ColorTextCalendar._theyear = theyear
        ColorTextCalendar._holiday = holiday(theyear)
    @staticmethod
    def _day(day):
        return datetime.date(ColorTextCalendar._theyear, ColorTextCalendar._themonth, day)
    def formatday(self, day, weekday, width):
        return ('' if day == 0 else
                '\x1b[1;31m%2i\x1b[0m'%day if weekday == 6 or 
                    ColorTextCalendar._day(day) in ColorTextCalendar._holiday else
                '\x1b[1;36m%2i\x1b[0m'%day if weekday == 5 else
                '%2i'%day).center(width)
    def formatweekday(self, day, width):
        s = super().formatweekday(day, width)
        return ('\x1b[1;31m%s\x1b[0m'%s if day==6 else
                '\x1b[1;36m%s\x1b[0m'%s if day==5 else s)
    def formatmonth(self, theyear, themonth, width, withyear=True):
        ColorTextCalendar._set_theyear(theyear)
        ColorTextCalendar._themonth = themonth
        return super().formatmonth(theyear, themonth, width, withyear)
    def formatyear(self, theyear, w=2, l=1, c=6, m=3):
        ColorTextCalendar._set_theyear(theyear)
        w = max(2, w)
        l = max(1, l)
        c = max(2, c)
        colwidth = (w + 1) * 7 - 1
        v = []
        a = v.append
        a(repr(theyear).center(colwidth*m+c*(m-1)).rstrip())
        a('\n'*l)
        header = self.formatweekheader(w)
        for (i, row) in enumerate(self.yeardays2calendar(theyear, m)):
            # months in this row
            months = range(m*i+1, min(m*(i+1)+1, 13))
            a('\n'*l)
            names = (self.formatmonthname(theyear, k, colwidth, False)
                     for k in months)
            a(clndr.formatstring(names, colwidth, c).rstrip())
            a('\n'*l)
            headers = (header for k in months)
            a(clndr.formatstring(headers, colwidth, c).rstrip())
            a('\n'*l)
            # max number of weeks for this row
            height = max(len(cal) for cal in row)
            for j in range(height):
                weeks = []
                for k, cal in zip(months, row):
                    if j >= len(cal):
                        weeks.append('')
                    else:
                        ColorTextCalendar._themonth = k
                        weeks.append(self.formatweek(cal[j], w))
                a(clndr.formatstring(weeks, colwidth, c).rstrip())
                a('\n' * l)
        return ''.join(v)

c = ColorTextCalendar()
firstweekday = c.getfirstweekday
def setfirstweekday(firstweekday):
    if not MONDAY <= firstweekday <= SUNDAY:
        raise IllegalWeekdayError(firstweekday)
    c.firstweekday = firstweekday

monthcalendar = c.monthdayscalendar
prweek = c.prweek
week = c.formatweek
weekheader = c.formatweekheader
prmonth = c.prmonth
month = c.formatmonth
calendar = c.formatyear
prcal = c.pryear

def main():
    theyear = int(sys.argv[1]) if len(sys.argv) > 1 else datetime.datetime.today().year
    month = int(sys.argv[2]) if len(sys.argv) > 2 else None
    if 1 <= theyear <= 12:
        month = theyear
        theyear = datetime.datetime.today().year
    if month:
        prmonth(theyear, month)
    else:
        prcal(theyear)
