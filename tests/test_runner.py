import pytest
from github import Github
from config import Config
from runners import Runner, RunnerException
from journal import SqliteJournal

UNKNOWN_REPO = "VLZH/unknown"


def test_runner_with_one_unknown_repository(monkeypatch):
    with monkeypatch.context() as m:
        m.setenv("GN_REPOSITORIES", UNKNOWN_REPO)
        c = Config()
        g = Github(c.token)
        j = SqliteJournal("./tests/connections/db.sqlite")
        with pytest.raises(RunnerException):
            Runner(c, g, j)
