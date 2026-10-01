# Lakewood zmanim

Daily zmanim for Lakewood, NJ, for 100 years: 2026 through 2125. Each year is one CSV in `data/`, one row per day.

## Columns

| Column | Meaning |
|---|---|
| `date`, `weekday` | Civil date |
| `hebrew_date` | e.g. `21 Tishrei 5787` |
| `day` | Yom Tov, fast day or other notable day (diaspora calendar) |
| `alos_16.1` | Dawn, sun 16.1° below the horizon |
| `alos_72` | Dawn, 72 minutes before sunrise |
| `misheyakir_11.5` | Earliest tallis and tefillin, sun 11.5° below the horizon |
| `sunrise` | Sea-level sunrise (netz) |
| `sof_zman_shma_mga`, `sof_zman_shma_gra` | Latest Shema, Magen Avraham (from alos 72 to tzais 72) and Gra (sunrise to sunset) |
| `sof_zman_tefila_mga`, `sof_zman_tefila_gra` | Latest Shacharis, same two opinions |
| `chatzos` | Midday |
| `mincha_gedola`, `mincha_ketana`, `plag_hamincha` | Gra hours |
| `sunset` | Sea-level sunset (shkia) |
| `candle_lighting` | 18 minutes before sunset on Fridays and erev Yom Tov. On a second night of Yom Tov, or Yom Tov right after Shabbos, it reads `after HH:MM:SS`: light after tzais, from an existing flame. |
| `tzais_8.5` | Nightfall, sun 8.5° below the horizon |
| `tzais_72` | Nightfall, 72 minutes after sunset (Rabbeinu Tam) |
| `havdalah_8.5`, `havdalah_72` | Filled in only on the day Shabbos or Yom Tov ends |

All times are local (`America/New_York`) and given to the second. Round them the safe way for the zman: earlier for a deadline, later for a start.

## How it's made

`generate.py` uses the [`zmanim`](https://pypi.org/project/zmanim/) Python library, a port of KosherJava. The location is 40.0821 N, 74.2097 W, at sea level.

```sh
python -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python generate.py            # 2026-2125
.venv/bin/python generate.py 2030 2030  # just one year
```

## Caveats

- Daylight saving time follows today's US rules for every year. If Congress changes them, re-run the script with an updated `tzdata`.
- These are computed times. For practical halacha, follow your rav and add a margin before the deadlines.
