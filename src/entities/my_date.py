from datetime import datetime, timedelta

class MyDate():
    def __init__(self, year=None, month=None, day=None, date_text=None):
        if date_text != None:
            [year, month, day] = map(int, date_text.split('/'))
        self.datetime = datetime(year=year, month=month, day=day)

    @property
    def date_text(self):
        return self.datetime.strftime('%Y/%m/%d')

    def smaller_than(self, other):
        return self.datetime < other.datetime

    def next_day(self):
        self.datetime += timedelta(days=1)
        

