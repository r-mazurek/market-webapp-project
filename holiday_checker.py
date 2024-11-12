import requests
from datetime import datetime

today = datetime.today().strftime("%Y-%m-%d")

def is_today_holiday(today = today, country_code="US"):
    response = requests.get(f"https://date.nager.at/api/v3/PublicHolidays/{today[:4]}/{country_code}")
    holidays = response.json()

    return any(holiday['date'] == today and ('Bank' in holiday['types'] or 'Public' in holiday['types']) for holiday in holidays)