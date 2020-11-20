import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))

import pytest
from src.db import Database
import src.config as config

config.TEST = True

def test_get_db_should_return_initialized_db():
    db = Database().db
    assert db != None