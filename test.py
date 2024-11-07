from datetime import datetime, timedelta
import utils

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




# print todays date
