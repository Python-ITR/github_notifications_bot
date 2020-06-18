from github import Commit
from changes import ChangeItem


class ChangesCommitExtractor:
    def __init__(self, commit: Commit):
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
