import sqlite3
from enum import Enum
from typing import Any

from .config import get_db_path


class SubmissionStatus(Enum):
    CORRECT = 1
    INCORRECT = 2
    ALREADY_GUESSED = 3
    ERROR = 4
    NO_ANSWER = 5
    TOO_HIGH = 6
    TOO_LOW = 7


def create_db():
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute(
        """
        CREATE TABLE
            submissions (
                year INT NOT NULL,
                day INT NOT NULL,
                part INT NOT NULL,
                submission_int INT,
                submission_str TEXT,
                timestamp DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                min_value INT,
                max_value INT,
                PRIMARY KEY (year, day, part),
                CHECK (
                    submission_int IS NULL
                    OR submission_str IS NULL
                )
            )
        """
    )
    c.execute(
        """
        CREATE TABLE
            failed_submissions (
                year INT NOT NULL,
                day INT NOT NULL,
                part INT NOT NULL,
                submission_str TEXT NOT NULL,
                timestamp DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (year, day, part, submission_str)
            )
    """
    )
    c.execute(
        """
        CREATE TABLE
            inputs (
                year INT NOT NULL,
                day INT NOT NULL,
                input TEXT NOT NULL,
                timestamp DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (year, day)
            )
        """
    )

    conn.commit()
    conn.close()


def get_bounds(year: int, day: int, part: int) -> tuple[int | None, int | None]:
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute(
        """
        SELECT
            min_value,
            max_value
        FROM
            submissions
        WHERE
            year = ?
            AND day = ?
            AND part = ?
        """,
        (year, day, part),
    )
    result = c.fetchone()
    conn.close()
    if result is None:
        return (None, None)
    return result


def validate_submission(
    year: int, day: int, part: int, submission: int | str
) -> tuple[bool, str, bool]:
    """
    Validate a submission.
    Returns a tuple of (valid, message, already_correct).
    """
    if already_guessed_failed(year, day, part, submission):
        return (
            False,
            f"You have already guessed this ({submission}) submission (cached).",
            False,
        )
    if has_correct_submission(year, day, part):
        return (False, "You have already submitted the correct answer (cached).", True)
    min_value, max_value = get_bounds(year, day, part)
    message = f"Submission ({submission}) must be in the range ({min_value}, {max_value}) (cached)."
    if min_value is not None and submission < min_value:
        return (False, message, False)
    if max_value is not None and submission > max_value:
        return (False, message, False)
    return (True, "Submission is valid", False)


def get_submission(year: int, day: int, part: int) -> int | str | None:
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute(
        """
        SELECT
            submission_int,
            submission_str
        FROM
            submissions
        WHERE
            year = ?
            AND day = ?
            AND part = ?
        """,
        (year, day, part),
    )
    result: tuple[int | None, str | None] = c.fetchone()
    submission_int, submission_str = result
    conn.close()
    if result is None:
        return None
    if submission_int is not None:
        return submission_int
    return submission_str


def has_correct_submission(year: int, day: int, part: int) -> bool:
    return get_submission(year, day, part) is not None


def already_guessed_failed(year: int, day: int, part: int, submission: Any) -> bool:
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute(
        """
        SELECT
            submission_str
        FROM
            failed_submissions
        WHERE
            year = ?
            AND day = ?
            AND part = ?
            AND submission_str = ?
        """,
        (year, day, part, str(submission)),
    )
    result = c.fetchone()
    conn.close()
    return result is not None


def insert_correct_submission(
    year: int,
    day: int,
    part: int,
    submission: int | str,
):
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    submission_int = None
    submission_str = None
    if isinstance(submission, int):
        submission_int = submission
        min_value, max_value = submission - 1, submission + 1
    else:
        submission_str = str(submission)
        min_value, max_value = None, None

    c.execute(
        """
        INSERT OR REPLACE INTO
            submissions (year, day, part, submission_int, submission_str, min_value, max_value)
        VALUES
            (?, ?, ?, ?, ?, ?, ?)
        """,
        (year, day, part, submission_int, submission_str, min_value, max_value),
    )
    conn.commit()
    conn.close()


def insert_failed_submission(
    year: int,
    day: int,
    part: int,
    submission: Any,
    status: SubmissionStatus = SubmissionStatus.INCORRECT,
):
    if status not in (
        SubmissionStatus.INCORRECT,
        SubmissionStatus.TOO_HIGH,
        SubmissionStatus.TOO_LOW,
    ):
        raise ValueError("status must be INCORRECT or one of its subtypes")

    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    submission_str = str(submission)

    c.execute(
        """
        INSERT INTO
            failed_submissions (year, day, part, submission_str)
        VALUES
            (?, ?, ?, ?)
        ON CONFLICT(year, day, part, submission_str) DO NOTHING
        """,
        (year, day, part, submission_str),
    )
    if status == SubmissionStatus.TOO_HIGH:
        submission_int = int(submission)
        c.execute(
            """
            INSERT INTO
                submissions (year, day, part, max_value)
            VALUES
                (?, ?, ?, ?)
            ON CONFLICT(year, day, part) DO UPDATE SET
                max_value = CASE
                    WHEN max_value IS NULL THEN ?
                    ELSE MIN(max_value, ?)
                END
            """,
            (year, day, part, submission_int, submission_int, submission_int),
        )
    elif status == SubmissionStatus.TOO_LOW:
        submission_int = int(submission)
        c.execute(
            """
            INSERT INTO
                submissions (year, day, part, min_value)
            VALUES
                (?, ?, ?, ?)
            ON CONFLICT(year, day, part) DO UPDATE SET
                min_value = CASE
                    WHEN min_value IS NULL THEN ?
                    ELSE MAX(min_value, ?)
                END
            """,
            (year, day, part, submission_int, submission_int, submission_int),
        )

    conn.commit()
    conn.close()


def get_input(year: int, day: int) -> str:
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute(
        """
        SELECT
            input
        FROM
            inputs
        WHERE
            year = ?
            AND day = ?
        """,
        (year, day),
    )
    result = c.fetchone()
    conn.close()
    if result is None:
        raise KeyError(f"Input for year {year}, day {day} not found")
    return result[0]


def insert_input(year: int, day: int, input: str):
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute(
        """
        INSERT OR REPLACE INTO
            inputs (year, day, input)
        VALUES
            (?, ?, ?)
        """,
        (year, day, input),
    )
    conn.commit()
    conn.close()
