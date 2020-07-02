"""
"""
from datetime import datetime
from sqlite3 import (
    Connection,
    Cursor,
    connect as sqlite3_connet,
    PARSE_DECLTYPES,
    PARSE_COLNAMES,
)
from abc import ABC


class Journal(ABC):
    def prepare(self):
        raise NotImplementedError()

    def add_repository(self, name: str, last_commit: datetime, last_pr: datetime):
        raise NotImplementedError()

    def get_last_commit(self, name: str) -> datetime:
        raise NotImplementedError()

    def get_last_pr(self, name: str) -> datetime:
        raise NotImplementedError()

    def update_last_commit(self, name: str, timestamp: datetime):
        raise NotImplementedError()

    def update_last_pr(self, name: str, timestamp: datetime):
        raise NotImplementedError()


class SqliteJournal(Journal):
    conn: Connection
    cur: Cursor

    def __init__(self, path: str):
        self.conn = sqlite3_connet(path, detect_types=PARSE_DECLTYPES | PARSE_COLNAMES)
        self.cur = self.conn.cursor()

    def prepare(self):
        self.prepare_schema()

    def check_table_exist(self) -> bool:
        self.cur.execute(
            "select count(*) from sqlite_master where type='table' and tbl_name='repositories';"
        )
        (count,) = self.cur.fetchone()
        return count == 1

    def prepare_schema(self):
        if not self.check_table_exist():
            self.cur.execute(
                """
            CREATE TABLE repositories (
	            name VARCHAR(255),
                last_commit TIMESTAMP,
                last_pr TIMESTAMP
            );
            """
            )

    def check_repository_existence(self, name: str) -> bool:
        self.cur.execute("select count(*) from repositories where name=?;", (name,))
        (count,) = self.cur.fetchone()
        return count == 1

    def add_repository(self, name: str, last_commit: datetime, last_pr: datetime):
        if not self.check_repository_existence(name):
            self.cur.execute(
                """
               INSERT INTO repositories (name, last_commit, last_pr)
		            values(?, ?, ?);
            """,
                (name, last_commit, last_pr),
            )
        else:
            self.update_last_commit(last_commit)
            self.update_last_pr(last_pr)

    def get_last_commit(self, name) -> datetime:
        self.cur.execute(
            """
               SELECT last_commit from repositories WHERE name=?;
            """,
            (name,),
        )
        (last_commit,) = self.cur.fetchone()
        return last_commit

    def get_last_pr(self, name) -> datetime:
        self.cur.execute(
            """
               SELECT last_pr from repositories WHERE name=?;
            """,
            (name,),
        )
        (last_pr,) = self.cur.fetchone()
        return last_pr

    def update_last_commit(self, name: str, timestamp: datetime):
        self.cur.execute(
            """
               UPDATE repositories SET last_commit=? WHERE name=?;
            """,
            (timestamp, name),
        )

    def update_last_pr(self, name: str, timestamp: datetime):
        self.cur.execute(
            """
               UPDATE repositories SET last_pr=? WHERE name=?;
            """,
            (timestamp, name),
        )

