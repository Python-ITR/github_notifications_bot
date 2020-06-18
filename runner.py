import logging
from typing import List
from config import Config
from github import Repository, Github, UnknownObjectException


class RunnerException(Exception):
    pass


class Runner:
    repositories: List[Repository.Repository]
    config: Config
    github: Github

    def __init__(self, config: Config, github: Github):
        self.github = github
        self.config = config
        self.repositories = []
        self.prepare()

    def prepare(self):
        for repo_str in self.config.repositories:
            try:
                self.repositories.append(self.github.get_repo(repo_str))
            except UnknownObjectException:
                logging.error(f"Unknow repo: '{repo_str}'")
        if len(self.repositories) == 0:
            raise RunnerException()

    def run(self):
        while True:
            print("run")
