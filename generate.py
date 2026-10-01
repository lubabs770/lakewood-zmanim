"""Write one CSV of daily zmanim per year for Lakewood, NJ.

Run: python generate.py [first_year] [last_year]   (default 2026-2125)
Output: data/<year>.csv
"""

import csv
import datetime as dt
import sys
from pathlib import Path

from zmanim.hebrew_calendar.jewish_calendar import JewishCalendar
from zmanim.util.geo_location import GeoLocation
from zmanim.zmanim_calendar import ZmanimCalendar

# Lakewood, NJ (BMG / downtown). Sea-level times, as most Lakewood calendars use.
LAKEWOOD = GeoLocation("Lakewood, NJ", 40.0821, -74.2097, "America/New_York", elevation=0)
CANDLE_LIGHTING_OFFSET = 18  # minutes before sunset

MONTHS = {
    1: "Nissan", 2: "Iyar", 3: "Sivan", 4: "Tammuz", 5: "Av", 6: "Elul",
    7: "Tishrei", 8: "Cheshvan", 9: "Kislev", 10: "Teves", 11: "Shevat",
    12: "Adar", 13: "Adar II",
}

COLUMNS = [
    "date", "weekday", "hebrew_date", "day",
    "alos_16.1", "alos_72", "misheyakir_11.5", "sunrise",
    "sof_zman_shma_mga", "sof_zman_shma_gra",
    "sof_zman_tefila_mga", "sof_zman_tefila_gra",
    "chatzos", "mincha_gedola", "mincha_ketana", "plag_hamincha",
    "sunset", "candle_lighting", "tzais_8.5", "tzais_72", "havdalah_8.5", "havdalah_72",
]


def hhmmss(t):
    return t.strftime("%H:%M:%S") if t else ""


def hebrew_date(jc):
    month = jc.jewish_month
    if month == 12 and jc.months_in_jewish_year() == 13:
        name = "Adar I"
    else:
        name = MONTHS[month]
    return f"{jc.jewish_day} {name} {jc.jewish_date[0]}"


def row(day):
    zc = ZmanimCalendar(geo_location=LAKEWOOD, date=day, candle_lighting_offset=CANDLE_LIGHTING_OFFSET)
    jc = JewishCalendar(day)
    jc.in_israel = False
    tzais = zc.tzais()  # 8.5 degrees below the horizon

    candles = ""
    if jc.has_candle_lighting():
        # Second night of Yom Tov, or Yom Tov right after Shabbos: light after tzais
        # from an existing flame, not before sunset.
        candles = f"after {hhmmss(tzais)}" if jc.has_delayed_candle_lighting() else hhmmss(zc.candle_lighting())

    ends_today = jc.is_assur_bemelacha() and not jc.is_tomorrow_assur_bemelacha()

    return [
        day.isoformat(), day.strftime("%A"), hebrew_date(jc), (jc.significant_day() or "").replace("_", " "),
        hhmmss(zc.alos()), hhmmss(zc.alos_72()),
        hhmmss(zc.sunrise_offset_by_degrees(90 + 11.5)), hhmmss(zc.sunrise()),
        hhmmss(zc.sof_zman_shma_mga()), hhmmss(zc.sof_zman_shma_gra()),
        hhmmss(zc.sof_zman_tfila_mga()), hhmmss(zc.sof_zman_tfila_gra()),
        hhmmss(zc.chatzos()), hhmmss(zc.mincha_gedola()), hhmmss(zc.mincha_ketana()),
        hhmmss(zc.plag_hamincha()), hhmmss(zc.sunset()), candles,
        hhmmss(tzais), hhmmss(zc.tzais_72()),
        hhmmss(tzais) if ends_today else "", hhmmss(zc.tzais_72()) if ends_today else "",
    ]


def main(first=2026, last=2125):
    out = Path(__file__).parent / "data"
    out.mkdir(exist_ok=True)
    for year in range(first, last + 1):
        day, end = dt.date(year, 1, 1), dt.date(year, 12, 31)
        with open(out / f"{year}.csv", "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(COLUMNS)
            while day <= end:
                w.writerow(row(day))
                day += dt.timedelta(days=1)


if __name__ == "__main__":
    main(*map(int, sys.argv[1:3]))
