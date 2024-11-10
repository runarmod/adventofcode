"""
A simple countdown timer that pauses the program until the given time.
The program will end one second after the given time to make sure the website has updated.
"""

from datetime import datetime, timedelta

import pause
import pytz


def format_time_until(now: datetime, time: datetime) -> str:
    """
    Returns a string of the time left until the given time.
    :param now: The current time.
    :param time: The time to count down to.
    :return: A string of the time left until the given time.
    """
    time_left = (time - now) + timedelta(seconds=1)

    hours = str(time_left.seconds // 3600).zfill(2)
    minutes = str((time_left.seconds // 60) % 60).zfill(2)
    seconds = str(time_left.seconds % 60).zfill(2)

    return f"{hours} hours, {minutes} minutes, {seconds} seconds"


def countdown(time: datetime) -> bool:  # ENDS ONE SECOND LATE TO MAKE SURE WEBSITE HAS UPDATED
    """
    Pauses the program until the given time.
    :param time: The time to count down to.
    :return: True if the program was paused until the given time, False otherwise.
    """
    now = datetime.now(tz=pytz.timezone(time.tzinfo.zone))
    timer = now.replace(microsecond=0) + timedelta(seconds=1)

    try:
        pause.until(timer)
        print(f"Waiting for puzzle to be released at {time}")
        while now < time:
            print(f"Time left: {format_time_until(now, time)}", end="\r")
            timer += timedelta(seconds=1)
            pause.until(min(timer, time))
            now = datetime.now(tz=pytz.timezone(time.tzinfo.zone))
        pause.seconds(1)
    except KeyboardInterrupt:
        print(" " * 60, end="\r")
        print("Aborted countdown.")
        return False
    print(" " * 60, end="\r")
    return True


def main() -> None:
    now = datetime.now(tz=pytz.timezone("EST"))
    release = now.replace(microsecond=0, second=30, minute=9)  # + timedelta(seconds=10)
    countdown(release)


if __name__ == "__main__":
    main()
