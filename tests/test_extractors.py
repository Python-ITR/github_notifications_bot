import pytest
from github import Github
from extractors import ChangesCommitExtractor

g = Github()

REPO = "VLZH/course-python-basics"
COMMIT_SHA = "4f7ce277547a8f5388bdcf950b696d365cf6a9c9"
FILES = [
    "docs/flask/flask.mdx",
    "docs/flask/flask_hello_world.mdx",
]


@pytest.fixture(scope="module")
def some_commit():
    repo = g.get_repo(REPO)
    commit = repo.get_commit(COMMIT_SHA)
    return commit


def test_changes_count(some_commit):
    extractor = ChangesCommitExtractor(some_commit)
    extractor.extract()
    assert len(extractor.changes) == 2


def test_changes_content(some_commit):
    extractor = ChangesCommitExtractor(some_commit)
    extractor.extract()
    for change in extractor.changes:
        assert change.commit_sha == COMMIT_SHA
        assert change.file in FILES
