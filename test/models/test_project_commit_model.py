import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '../../src'))

import pytest
from src.models.project_commit_model import ProjectCommitModel

class TestProjectCommitModel():
    @classmethod
    def setup_class(self):
        print('a')