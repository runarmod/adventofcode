from datetime import datetime, timedelta
import pause
import pytz


def format_time_until(now: datetime, time: datetime):
    time_left = (time - now) + timedelta(seconds=1)
    hours = time_left.seconds // 3600
    minutes = (time_left.seconds // 60) % 60
    seconds = time_left.seconds % 60
    return f"{str(hours).zfill(2)} hours, {str(minutes).zfill(2)} minutes, {str(seconds).zfill(2)} seconds"

def countdown(time: datetime): # ENDS ONE SECOND LATE TO MAKE SURE WEBSITE HAS UPDATED
    now = datetime.now(tz=pytz.timezone(time.tzinfo.zone))
    timer = now.replace(microsecond=0) + timedelta(seconds=1)
    pause.until(timer)

    print(f"Waiting for puzzle to be released at {time}")
    while now < time:
        print(f"Time left: {format_time_until(now, time)}", end="\r")
        timer += timedelta(seconds=1)
        pause.until(min(timer, time))
        now = datetime.now(tz=pytz.timezone(time.tzinfo.zone))
    pause.seconds(1)
    print(" " * 60, end="\r")

def main():
    now = datetime.now(tz=pytz.timezone("EST"))
    release = now.replace(microsecond=0, second=30, minute=9) #+ timedelta(seconds=10)
    countdown(release)

if __name__ == "__main__":
    main()
