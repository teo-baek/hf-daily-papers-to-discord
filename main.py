from datetime import date
from daily import run_daily
from weekly import run_weekly
from monthly import run_monthly

today = date.today()
weekday = today.weekday()  # 0=Mon, 6=Sun

print("🚀 Hugging Face Papers Auto Mode")

if weekday == 6:
    print("📅 Weekly mode activated.")
    run_weekly()
elif today.day == 1:
    print("📅 Monthly mode activated.")
    run_monthly()
else:
    print("📅 Daily mode activated.")
    run_daily()
