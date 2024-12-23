from datetime import datetime, timedelta
import utils
from icecream import ic

# Get today's date
due_date = datetime.today()

# If its a weekday
if due_date.weekday() <= 4:
    # Print the date
    print(f"Sysdoc release notification: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# # Add 2 years to today's date
# two_years_later = today + timedelta(days=365*2)

# # Format the date as a string
# date_string = two_years_later.strftime('%Y-%m-%d')

# print(date_string)

# due_date = datetime.today() + timedelta(weeks=12)
# due_date = due_date.replace(day=1)
# print(due_date)


# # Friday
# if due_date.weekday() == 3:
#     replacement_date = due_date - timedelta(days=3)
#     due_date = replacement_date
#     print(f"Move back 3 days: {due_date}")
# # Saturday
# elif due_date.weekday() == 4:
#     replacement_date = due_date - timedelta(days=4)
#     due_date = replacement_date
#     print(f"Move back 4 days: {due_date}")


# Calculate the first day of the next year
first_day_next_year = datetime(datetime.today().year + 1, 1, 1)

# Calculate the first day of next July
first_day_next_july = datetime(datetime.today().year, 7, 1)
if datetime.today() >= first_day_next_july:
    first_day_next_july = datetime(datetime.today().year + 1, 7, 1)

# Determine which date comes first
earliest_date = min(first_day_next_year, first_day_next_july)
ic(earliest_date)

# Calculate the first day of the next standard quarter
# (January, April, July, October)
if datetime.today().month < 4:
    next_quarter = datetime(datetime.today().year, 4, 1)
elif datetime.today().month < 7:
    next_quarter = datetime(datetime.today().year, 7, 1)
elif datetime.today().month < 10:
    next_quarter = datetime(datetime.today().year, 10, 1)
else:
    next_quarter = datetime(datetime.today().year + 1, 1, 1)
ic(next_quarter)

