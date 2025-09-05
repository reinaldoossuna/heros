from dataclasses import dataclass, asdict, field
from datetime import datetime, timezone
from dateutil.relativedelta import relativedelta

DATE_TO_STRING = "%Y-%m-%d %H:%M:%S"


def start_of_month(month: datetime):
    return month.replace(day=1, hour=0, minute=0, second=0, microsecond=0)


@dataclass
class Period:
    begin: datetime
    end: datetime

    def __str__(self):
        return (
            f"?start={self.begin.strftime(DATE_TO_STRING)}&end={self.end.strftime(DATE_TO_STRING)}"
        )


def period_of(months: int) -> Period:
    end_lastmonth = datetime.now().replace(
        day=1, hour=0, minute=0, second=0, microsecond=0, tzinfo=timezone.utc
    )
    begin = end_lastmonth + relativedelta(months=-months)
    return Period(begin, end_lastmonth)


def period_of_yearsago(months: int, years: int) -> Period:
    p = period_of(months)
    begin = p.begin - relativedelta(years=years)
    end = p.end - relativedelta(years=years)
    return Period(begin, end)
