from flask import Flask, render_template
from datetime import datetime, date, time, UTC

from price_checker import get_daily_price_change


app = Flask(__name__)

@app.route('/')
def home():

    today = date.today().strftime("%d/%m/%Y")
    time_now = datetime.now().time().strftime('%H:%M')
    
    is_trading_day = datetime.isoweekday(date.today()) ## and no bank holday

    did_session_start = 1 if datetime.now(UTC).time() > time(14, 30) else 0 

    time_to_session_end = datetime.combine(datetime.now(UTC).date(), time(21, 0), UTC) - datetime.now(UTC) 
    time_to_session_start = datetime.combine(datetime.now(UTC).date(), time(14, 30), UTC) - datetime.now(UTC)

    # Get hours and minutes from the timedelta
    hours, remainder = divmod(time_to_session_end.seconds, 3600)
    minutes, _ = divmod(remainder, 60)

    nq_price_change = get_daily_price_change("QQQ")
    es_price_change = get_daily_price_change("SPY")
    
    data = {
        'today': today,
        'time_now': time_now,
        'is_trading_day': is_trading_day,
        'did_session_start': did_session_start,
        'hours': hours,
        'minutes': minutes,
        'nq_price_change': nq_price_change,
        'es_price_change': es_price_change
    }

    return render_template('home_page.html', **data)

app.run()