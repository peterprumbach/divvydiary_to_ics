import os
import json
from ics import Calendar, Event
import arrow
from dateutil import tz
import datetime
import dividends

def createCalendar(dividends):
    c = Calendar()
    for asset in dividends:
        e = Event()
        e.name = asset['name']
        e.begin = arrow.get(asset['payDate'], tzinfo='Europe/Berlin')
        e.duration = {"hours": 24}
        payment = round((float(asset['amount'])*float(asset['quantity'])*float(asset['exchangeRate'])), 2)
        exDate = arrow.get(asset['exDate'], tzinfo='Europe/Berlin').format('DD.MM.YYYY')
        payDate = arrow.get(asset['payDate'], tzinfo='Europe/Berlin').format('DD.MM.YYYY')
        e.description = f"Dividende: " + str(payment).replace(".", ",") + " EUR" + "\n\nEx-Dividende: " + exDate + "\n\nZahltag: " + payDate
        e.make_all_day
        c.events.add(e)

    with open("dividends.ics", 'w') as f:
        f.writelines(c)
