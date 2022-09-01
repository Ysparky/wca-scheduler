class Competition:
    def __init__(self, name, dates, schedules):
        self.days = len(dates)
        self.dates = dates
        self.name = name
        self.schedules = schedules
