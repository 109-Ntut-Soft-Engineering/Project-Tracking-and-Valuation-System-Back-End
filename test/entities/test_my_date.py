import sys
import os.path

import pytest
from datetime import datetime
from src.entities.my_date import MyDate

class TestMyDate():
    @classmethod
    def setup_class(self):
        self.date1 = MyDate(2020, 12, 29)
        self.date2 = MyDate(2021, 1, 2)

    def test_constructor_with_text(self):
        date = MyDate(date_text='2020/12/31')
        assert date.datetime.date() == datetime(year=2020, month=12, day=31).date()

    def test_constructor_with_date(self):
        date = MyDate(2020, 12, 31)
        assert date.datetime.date() == datetime(year=2020, month=12, day=31).date()

    def test_date_text(self):
        assert self.date1.date_text == '2020/12/29'
        
    def test_smaller_then(self):
        assert self.date1.smaller_than(self.date2) == True
        assert self.date2.smaller_than(self.date1) == False

    def test_next_day(self):
        self.date1.next_day()
        assert self.date1.date_text == '2020/12/30'

    