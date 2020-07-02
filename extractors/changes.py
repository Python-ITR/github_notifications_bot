class ChangeItem:
    def __init__(self, commit_sha: str, date: str, file: str):
        self.commit_sha = commit_sha
        self.date = date
        self.file = file
