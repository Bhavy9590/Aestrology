# તારક Kundli — Production-style Gujarati Vedic Astrology

A Gujarati-first React + Django Vedic astrology application using Swiss Ephemeris for astronomical calculations, location search with timezone data, Lahiri sidereal calculations, houses, Nakshatra, Navamsa and Vimshottari Dasha.

## Quick start — Windows

1. Install Python 3.12/3.13 and Node.js 18+.
2. Because `pyswisseph` may need a compiler on Windows, install Microsoft C++ Build Tools with **Desktop development with C++** and a Windows SDK if pip asks for it.
3. Run `install.bat` once.
4. Run `start.bat` whenever you want the app. It starts Django and React together and opens the browser.

## What is calculated

- Sidereal zodiac with Lahiri Ayanamsha
- Sun, Moon, Mercury, Venus, Mars, Jupiter, Saturn, Rahu and Ketu
- Ascendant/Lagna
- Moon/Sun Rashi
- Nakshatra, Pada and Nakshatra lord
- 12 houses and house lords
- Navamsa/D9 positions
- Vimshottari Mahadasha and Antardasha
- Basic Panchang Tithi
- Location latitude, longitude and timezone

## Location

The development location service uses Open-Meteo geocoding and returns canonical city/state/country, coordinates and IANA timezone. For production, use a provider/database with an appropriate commercial/service agreement and caching/rate limits.

## Important

The astronomical calculation layer is deterministic calculation software. Traditional astrological interpretation is presented as interpretation, not as scientific certainty or medical/financial advice.
