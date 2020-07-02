from typing import List
from github import Commit
from .changes import ChangeItem


class ChangesCommitExtractor:
    changes: List[ChangeItem]
    
    def __init__(self, commit: Commit.Commit):
        self.commit = commit
        self.changes = []

    def extract(self):
        for file in self.commit.files:
            self.changes.append(
                ChangeItem(
                    commit_sha=self.commit.sha,
                    date=self.commit.commit.last_modified,
                    file=file.filename,
                )
            )
        pass
