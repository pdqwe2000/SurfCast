from datetime import datetime, timezone
import openmeteo_requests
import pandas as pd
import requests_cache
from retry_requests import retry
import json
from pathlib import Path

# --- Setup da session  ---
cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)


# MARINE API — Dados do mar

marine_url = "https://marine-api.open-meteo.com/v1/marine"
marine_params = {
    "latitude": 41.5165,
    "longitude": -8.7848,
    "hourly": [
        "wave_height", "wave_direction", "wave_period",
        "wind_wave_height", "wind_wave_direction", "wind_wave_period",
        "swell_wave_height", "swell_wave_direction", "swell_wave_period",
        "sea_surface_temperature"
    ],
    "daily": ["wave_height_max", "wave_direction_dominant"],
    "forecast_days": 7,
    "timezone": "auto"
}

marine_response = openmeteo.weather_api(marine_url, params=marine_params)[0]

# --- Dados horários mar ---
hourly = marine_response.Hourly()
hourly_data = {
    "date": pd.date_range(
        start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
        end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
        freq=pd.Timedelta(seconds=hourly.Interval()),
        inclusive="left"
    ),
    "wave_height": hourly.Variables(0).ValuesAsNumpy(),
    "wave_direction": hourly.Variables(1).ValuesAsNumpy(),
    "wave_period": hourly.Variables(2).ValuesAsNumpy(),
    "wind_wave_height": hourly.Variables(3).ValuesAsNumpy(),
    "wind_wave_direction": hourly.Variables(4).ValuesAsNumpy(),
    "wind_wave_period": hourly.Variables(5).ValuesAsNumpy(),
    "swell_wave_height": hourly.Variables(6).ValuesAsNumpy(),
    "swell_wave_direction": hourly.Variables(7).ValuesAsNumpy(),
    "swell_wave_period": hourly.Variables(8).ValuesAsNumpy(),
    "sea_surface_temperature": hourly.Variables(9).ValuesAsNumpy()
}
marine_hourly_df = pd.DataFrame(hourly_data)

# --- Dados diários mar ---
daily = marine_response.Daily()
marine_daily = {
    "date": pd.date_range(
        start=pd.to_datetime(daily.Time(), unit="s", utc=True),
        end=pd.to_datetime(daily.TimeEnd(), unit="s", utc=True),
        freq=pd.Timedelta(seconds=daily.Interval()),
        inclusive="left"
    ),
    "wave_height_max": daily.Variables(0).ValuesAsNumpy(),
    "wave_direction_dominant": daily.Variables(1).ValuesAsNumpy(),
}
marine_daily_df = pd.DataFrame(marine_daily)


# Dados solares e UV

forecast_url = "https://api.open-meteo.com/v1/forecast"
forecast_params = {
    "latitude": 41.5165,
    "longitude": -8.7848,
    "hourly": [
        "temperature_2m","apparent_temperature","wind_speed_10m","wind_direction_10m","precipitation_probability"
    ],
    "daily": ["sunrise", "sunset", "uv_index_max", "daylight_duration"],
    "forecast_days": 7,
    "timezone": "auto"
}

forecast_response = openmeteo.weather_api(forecast_url, params=forecast_params)[0]

hourly_forecast = forecast_response.Hourly()

forecast_hourly = {
    "date": pd.date_range(
        start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
        end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
        freq=pd.Timedelta(seconds=hourly.Interval()),
        inclusive="left"
    ),
    "temperature_2m": hourly.Variables(0).ValuesAsNumpy(),
    "apparent_temperature": hourly.Variables(1).ValuesAsNumpy(),
    "wind_speed_10m": hourly.Variables(2).ValuesAsNumpy(),
    "wind_direction_10m": hourly.Variables(3).ValuesAsNumpy(),
    "precipitation_probability": hourly.Variables(4).ValuesAsNumpy(),
    }
Forecast_hourly_df = pd.DataFrame(forecast_hourly)

daily_forecast = forecast_response.Daily()
forecast_daily = {
    "date": pd.date_range(
        start=pd.to_datetime(daily_forecast.Time(), unit="s", utc=True),
        end=pd.to_datetime(daily_forecast.TimeEnd(), unit="s", utc=True),
        freq=pd.Timedelta(seconds=daily_forecast.Interval()),
        inclusive="left"
    ),
    "sunrise": [datetime.fromtimestamp(ts, tz=timezone.utc) for ts in daily_forecast.Variables(0).ValuesInt64AsNumpy()],
    "sunset": [datetime.fromtimestamp(ts, tz=timezone.utc) for ts in daily_forecast.Variables(1).ValuesInt64AsNumpy()],
    "uv_index_max": daily_forecast.Variables(2).ValuesAsNumpy(),
    "daylight_duration": [
        f"{int(sec // 3600)}:{int((sec % 3600) // 60)}"
        for sec in daily_forecast.Variables(3).ValuesAsNumpy()
    ],
}
forecast_daily_df = pd.DataFrame(forecast_daily)


# Join

combined_daily = pd.merge(marine_daily_df, forecast_daily_df, on="date", how="inner")
combined_hourly = pd.merge(marine_hourly_df, Forecast_hourly_df, on="date", how="inner")


#  JSON

output_dir = Path("surf_data")
output_dir.mkdir(exist_ok=True)

hourly_json = combined_hourly.to_json(orient="records", date_format="iso")
daily_json = combined_daily.to_json(orient="records", date_format="iso")

with open(output_dir / "hourly_data.json", "w", encoding="utf-8") as f:
    f.write(hourly_json)

with open(output_dir / "daily_data.json", "w", encoding="utf-8") as f:
    f.write(daily_json)

print("\n JSON files saved in 'surf_data/' folder:")
print(" - hourly_data.json")
print(" - daily_data.json")
