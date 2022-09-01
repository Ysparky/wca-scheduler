import datetime


class Utils:
    @staticmethod
    def get_datetime(comp_time, comp_day):
        return True


def get_datetime(parsed_date: datetime, parsed_time: datetime):
    year = parsed_date.year
    month = parsed_date.month
    day = parsed_date.day
    hour = parsed_time.hour
    minute = parsed_time.minute
    return datetime.datetime(year, month, day, hour + 5, minute)
