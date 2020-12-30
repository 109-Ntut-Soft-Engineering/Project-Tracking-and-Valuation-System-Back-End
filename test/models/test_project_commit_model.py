from test.fake_conn_tool import FakeConnTool
from src.models.project_commit_model import ProjectCommitModel
from src.entities.commit import Commit
from src.entities.commits import Commits
from src.entities.project import Project
from src.common import constant
import datetime, sys, os.path, pytest

sys.path.append(os.path.join(os.path.dirname(__file__), '../../src'))


class TestProjectCommitModel():
    @classmethod
    def setup_class(self):
        self.model = ProjectCommitModel(FakeConnTool())

    def test_constructor(self):
        assert self.model._db != None
        assert self.model._uid == constant.TEST_UID

    def test_transform_commit(self):
        src_commit = {
            'author': {
                'name': None,
                'email': None
            },
            'commit': {
                'author': {
                    'name': 'name',
                    'email': 'abc@gmail.com',
                    'date': '2020/01/01, 01:11:11'
                },
                'message': 'message',
                'html_url': 'https://a/b',
                'url': 'https://b/a'
            },
            'stats': {
                'additions': 1,
                'deletions': 30,
                'total': 31
            }
        }
        dest_commit = self.model._ProjectCommitModel__transform_commit(src_commit)
        expect = Commit(author='name',
                        message='message',
                        lines=31,
                        time='2020/01/01')
        assert dest_commit.author == expect.author
        assert dest_commit.message == expect.message
        assert dest_commit.lines == expect.lines
        assert dest_commit.time == expect.time

    def test_build_commits(self):
        pro_name = 'pname'
        commit1 = Commit(author='name1',
                         message='message1',
                         lines=31,
                         time='2020/01/01')
        commit2 = Commit(author='name2',
                         message='message2',
                         lines=32,
                         time='2020/01/02')
        cmt_list = [commit1, commit2]
        dest_cmts = self.model._ProjectCommitModel__build_commits(pro_name, cmt_list)
        expect = Commits(pro_name, ['name1', 'name2'], cmt_list)

        assert dest_cmts.name == expect.name
        assert set(dest_cmts.member) == set(expect.member)
        assert dest_cmts.commit_list == expect.commit_list

    def test_sort_commits_by_time_desc(self):
        commit1 = Commit(author='name1',
                         message='message1',
                         lines=31,
                         time='2020/01/01')
        commit2 = Commit(author='name2',
                         message='message2',
                         lines=32,
                         time='2020/01/02')
        commit3 = Commit(author='name3',
                         message='message3',
                         lines=34,
                         time='2020/01/03')

        commits = Commits('pname', ['name2', 'name3', 'name1'], [commit2, commit3, commit1])
        self.model._ProjectCommitModel__sort_commits_by_time(commits, 'desc')
        expect = Commits('pname', ['name3', 'name2', 'name1'], [commit3, commit2, commit1])
        assert commits.commit_list == expect.commit_list

    def test_sort_commits_by_time_asc(self):
        commit1 = Commit(author='name1',
                         message='message1',
                         lines=31,
                         time='2020/01/01')
        commit2 = Commit(author='name2',
                         message='message2',
                         lines=32,
                         time='2020/01/02')
        commit3 = Commit(author='name3',
                         message='message3',
                         lines=34,
                         time='2020/01/03')

        commits = Commits('pname', ['name2', 'name3', 'name1'], [commit2, commit3, commit1])
        self.model._ProjectCommitModel__sort_commits_by_time(commits, 'asc')
        expect = Commits('pname', ['name1', 'name2', 'name3'], [commit1, commit2, commit3])
        assert commits.commit_list == expect.commit_list

    def test_sort_commits_by_time_error(self):
        commit1 = Commit(author='name1',
                         message='message1',
                         lines=31,
                         time='2020/01/01')
        commit2 = Commit(author='name2',
                         message='message2',
                         lines=32,
                         time='2020/01/02')
        commit3 = Commit(author='name3',
                         message='message3',
                         lines=34,
                         time='2020/01/03')

        commits = Commits('pname', ['name2', 'name3', 'name1'], [commit2, commit3, commit1])
        with pytest.raises(SystemExit) as cm:
            self.model._ProjectCommitModel__sort_commits_by_time(commits, 'whatever')
        assert cm.match('sort type only have "desc" & "asc"')

    def test_get_commits(self):
        project = Project(name='test_name',
                          owner=constant.TEST_UID,
                          repositories={'Github': [324982851]},
                          updated=datetime.datetime(2020, 1, 1,
                                                    1, 11, 11, 0,
                                                    tzinfo=datetime.timezone.utc)
                          ).to_dict()

        commits = self.model._ProjectCommitModel__get_commits(project)
        expect = Commits(name='test_name',
                         member=['gougon'],
                         commit_list=[
                             Commit(
                                 author='gougon',
                                 message='Create README.md',
                                 lines=2,
                                 time='2020/12/28'
                             )
                         ])
        assert commits.name == expect.name
        assert commits.member == expect.member
        assert commits.commit_list == expect.commit_list

    def test_get_project_commit_info(self):
        res = self.model.get_project_commit_info(constant.TEST_PID1)
        expect = {
            'commits': {
                'name': 'test_name',
                'member': ['gougon'],
                'commit_list': [
                    {
                        'author': 'gougon',
                        'message': 'Create README.md',
                        'lines': 2,
                        'time': '2020/12/28'
                    }
                ]
            }
        }

        assert res == expect
