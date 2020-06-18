import pytest
from github import Github
from config import Config
from runner import Runner, RunnerException

UNKNOWN_REPO = "VLZH/unknown"


def test_runner_with_one_unknown_repository(monkeypatch):
    with monkeypatch.context() as m:
        m.setenv("GN_REPOSITORIES", UNKNOWN_REPO)
        c = Config()
        g = Github(c.token)
        with pytest.raises(RunnerException):
            Runner(c, g)
