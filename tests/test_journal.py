import sqlite3
import pytest
from datetime import datetime, timedelta
from faker import Faker
from journal import SqliteJournal

REPO_NAME = "vlzh/test"
INIT_NOW = datetime.now()


@pytest.fixture(scope="module")
def faker():
    return Faker()


@pytest.fixture(scope="module")
def journal(faker):
    connection_name = faker.file_name(extension="sqlite")
    print(connection_name)
    return SqliteJournal(f"./tests/connections/{connection_name}")


def test_table_initialization(journal: SqliteJournal):
    assert journal.check_table_exist() == False
    journal.prepare()
    assert journal.check_table_exist() == True


def test_repository_initialization(journal: SqliteJournal):
    assert journal.check_repository_existence(REPO_NAME) == False
    journal.add_repository(REPO_NAME, INIT_NOW, INIT_NOW)
    assert journal.check_repository_existence(REPO_NAME) == True


def test_get_last_commit(journal: SqliteJournal):
    last_commit = journal.get_last_commit(REPO_NAME)
    assert (last_commit - INIT_NOW) < timedelta(seconds=1)


def test_get_last_pr(journal: SqliteJournal):
    last_commit = journal.get_last_pr(REPO_NAME)
    assert (last_commit - INIT_NOW) < timedelta(seconds=1)


def test_set_last_commit(journal: SqliteJournal):
    next_day = datetime.now() + timedelta(days=1)
    journal.update_last_commit(REPO_NAME, next_day)
    last_commit = journal.get_last_commit(REPO_NAME)
    assert (next_day - last_commit) < timedelta(seconds=1)


def test_set_last_pr(journal: SqliteJournal):
    next_day = datetime.now() + timedelta(days=1)
    journal.update_last_pr(REPO_NAME, next_day)
    last_pr = journal.get_last_pr(REPO_NAME)
    assert (next_day - last_pr) < timedelta(seconds=1)
