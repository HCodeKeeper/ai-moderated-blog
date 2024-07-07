from datetime import date


def start_date_not_future(start_date: date):
    if start_date > date.today():
        raise ValueError("Start date cannot be in the future")
    return start_date


def end_date_not_future(end_date: date):
    if end_date > date.today():
        raise ValueError("End date cannot be in the future")
    return end_date


def end_date_not_before_start_date(start_date: date, end_date: date):
    if end_date < start_date:
        raise ValueError("End date cannot be before start date")
    return end_date


def validate_date_range(start_date: date, end_date: date):
    start_date_not_future(start_date)
    end_date_not_future(end_date)
    end_date_not_before_start_date(start_date, end_date)
