import logging
from typing import List
from config import Config
from github import Repository, Github, UnknownObjectException, Commit, PullRequest
from journal import Journal


class RunnerException(Exception):
    pass


class Runner:
    def __init__(self, config: Config, github: Github, journal: Journal):
        self.github = github
        self.config = config
        self.repositories = [] # type: List[Repository.Repository]
        self.prepare()
        self.journal = journal

    def prepare(self):
        for repo_str in self.config.repositories:
            try:
                self.repositories.append(self.github.get_repo(repo_str))
            except UnknownObjectException:
                logging.error(f"Unknow repo: '{repo_str}'")
        if len(self.repositories) == 0:
            raise RunnerException()
        self.journal.prepare()
        for repo in self.repositories:
            last_commit = repo.get_commits()[0] # type: Commit.Commit
            last_pr = repo.get_pulls()[0] # type: PullRequest.PullRequest

    def run(self):
        while True:
            for repo in self.repositories:
                pass