import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))

import pytest
import requests
from flask import request
from resources.project import Project
import src.config as config

config.TEST = True
base = config.BASE

def test_query_projects():
    response = requests.get(base + 'project/')
    project = Project()