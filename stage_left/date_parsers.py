from datetime import datetime, timedelta


def parse_ymd(format_, date_):
    # exact date
    return datetime.strptime(date_, format_).date()


def parse_ym(format_, date_):
    # last day of month

    # fmt: off
    def last_day_of_month(d):
        return (
            (d.replace(day=28) + timedelta(days=4))
            .replace(day=1) + timedelta(days=-1)
        )
    # fmt: on

    return last_day_of_month(datetime.strptime(date_, format_).date())


def parse_y(date_):
    # last day of year
    return datetime.strptime(date_ + "-12-31", "%Y-%m-%d").date()


def parse_w(format_, date_):
    # last day of week
    return datetime.strptime(date_ + " 0", format_ + " %w").date()


def parse_q(date_):
    # last day of quarter
    quarters = {
        "1": "-03-31",
        "2": "-06-30",
        "3": "-09-30",
        "4": "-12-31",
    }
    try:
        return datetime.strptime(date_[:4] + quarters[date_[6]], "%Y-%m-%d").date()
    except KeyError:
        raise ValueError("Q must be in the range 1..4")
