from flask import Flask, render_template
from datetime import datetime, date, time, UTC

from price_checker import get_daily_price_change
from holiday_checker import is_today_holiday

app = Flask(__name__)

@app.route('/')
def home():
    today = date.today().strftime("%d/%m/%Y")
    display_time = datetime.now().time().strftime('%H:%M')

    is_trading_day = datetime.isoweekday(date.today()) <= 5 and not is_today_holiday()

    session_start_time = datetime.combine(datetime.now(UTC).date(), time(14, 30), UTC)
    session_end_time = datetime.combine(datetime.now(UTC).date(), time(21), UTC)
    now = datetime.now(UTC)

    did_session_start = now > session_start_time and now < session_end_time

    time_to_session_end = session_end_time - now
    time_to_session_start = session_start_time - now

    hours, remainder = divmod(time_to_session_end.seconds if did_session_start else time_to_session_start.seconds, 3600)
    minutes, _ = divmod(remainder, 60)

    nq_price_change = get_daily_price_change("QQQ")
    es_price_change = get_daily_price_change("SPY")

    # Convert datetime to UNIX timestamps
    session_start_timestamp = int(session_start_time.timestamp())
    session_end_timestamp = int(session_end_time.timestamp())

    did_session_end = now > session_end_time

    data = {
        'today': today,
        'display_time': display_time,
        'is_trading_day': is_trading_day,
        'did_session_start': did_session_start,
        'session_start_timestamp': session_start_timestamp,
        'session_end_timestamp': session_end_timestamp,
        'hours': hours,
        'minutes': minutes,
        'nq_price_change': nq_price_change,
        'es_price_change': es_price_change,
        'did_session_end': did_session_end
    }

    return render_template('home_page.html', **data)

app.run()
