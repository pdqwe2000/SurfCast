# # pip install openmeteo-requests

# import openmeteo_requests

# openmeteo = openmeteo_requests.Client()

# # Make sure all required weather variables are listed here
# # The order of variables in hourly or daily is important to assign them correctly below
# url = "https://api.open-meteo.com/v1/forecast"
# params = {
# 	"latitude": [52.52, 50.1155],
# 	"longitude": [13.41, 8.6842],
# 	"hourly": "temperature_2m",
# 	"models": ["icon_global", "icon_eu"],
# }
# responses = openmeteo.weather_api(url, params=params)
# for response in responses:
# 	print(f"\nCoordinates: {response.Latitude()}°N {response.Longitude()}°E")
# 	print(f"Elevation: {response.Elevation()} m asl")
# 	print(f"Timezone difference to GMT+0: {response.UtcOffsetSeconds()}s")
# 	print(f"Model Nº: {response.Model()}")

# # # Process current data. The order of variables needs to be the same as requested.
# # current = response.Current()
# # current_temperature_2m = current.Variables(0).Value()
# # current_relative_humidity_2m = current.Variables(1).Value()

# # print(f"Current time: {current.Time()}")
# # print(f"Current temperature_2m: {current_temperature_2m}")
# # print(f"Current relative_humidity_2m: {current_relative_humidity_2m}")

from datetime import datetime, timezone
import openmeteo_requests

import pandas as pd
import requests_cache
from retry_requests import retry

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

# Make sure all required weather variables are listed here
# The order of variables in hourly or daily is important to assign them correctly below
url = "https://api.open-meteo.com/v1/forecast"
params = {
	"latitude": 41.5165,
	"longitude": -8.7848,
	"daily": ["sunrise", "sunset", "uv_index_max", "daylight_duration"],
	"hourly": ["temperature_2m", "apparent_temperature", "precipitation_probability", "uv_index", "wind_speed_10m", "wind_direction_10m", "wind_gusts_10m"],
	"models": "best_match",
	"current": "temperature_2m",
	"forecast_days": 3,
}
responses = openmeteo.weather_api(url, params=params)

# Process first location. Add a for-loop for multiple locations or weather models
response = responses[0]
print(f"Coordinates: {response.Latitude()}°N {response.Longitude()}°E")
print(f"Elevation: {response.Elevation()} m asl")
print(f"Timezone difference to GMT+0: {response.UtcOffsetSeconds()}s")

# Process current data. The order of variables needs to be the same as requested.
current = response.Current()
current_temperature_2m = current.Variables(0).Value()

print(f"\nCurrent time: {current.Time()}")
print(f"Current temperature_2m: {current_temperature_2m}")

# Process hourly data. The order of variables needs to be the same as requested.
hourly = response.Hourly()
hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
hourly_apparent_temperature = hourly.Variables(1).ValuesAsNumpy()
hourly_precipitation_probability = hourly.Variables(2).ValuesAsNumpy()
hourly_uv_index = hourly.Variables(3).ValuesAsNumpy()
hourly_wind_speed_10m = hourly.Variables(4).ValuesAsNumpy()
hourly_wind_direction_10m = hourly.Variables(5).ValuesAsNumpy()
hourly_wind_gusts_10m = hourly.Variables(6).ValuesAsNumpy()

hourly_data = {"date": pd.date_range(
	start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
	end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
	freq = pd.Timedelta(seconds = hourly.Interval()),
	inclusive = "left"
)}

hourly_data["temperature_2m"] = hourly_temperature_2m
hourly_data["apparent_temperature"] = hourly_apparent_temperature
hourly_data["precipitation_probability"] = hourly_precipitation_probability
hourly_data["uv_index"] = hourly_uv_index
hourly_data["wind_speed_10m"] = hourly_wind_speed_10m
hourly_data["wind_direction_10m"] = hourly_wind_direction_10m
hourly_data["wind_gusts_10m"] = hourly_wind_gusts_10m

hourly_dataframe = pd.DataFrame(data = hourly_data)
print("\nHourly data\n", hourly_dataframe)

# Process daily data. The order of variables needs to be the same as requested.
daily = response.Daily()
daily_sunrise = daily.Variables(0).ValuesInt64AsNumpy()
daily_sunset = daily.Variables(1).ValuesInt64AsNumpy()
daily_uv_index_max = daily.Variables(2).ValuesAsNumpy()
daily_daylight_duration = daily.Variables(3).ValuesAsNumpy()

daily_data = {"date": pd.date_range(
    start=pd.to_datetime(daily.Time(), unit="s", utc=True),
    end=pd.to_datetime(daily.TimeEnd(), unit="s", utc=True),
    freq=pd.Timedelta(seconds=daily.Interval()),
    inclusive="left"
)}

# ✅ Convert Unix timestamps to datetime with timezone
daily_data["sunrise"] = [datetime.fromtimestamp(ts, tz=timezone.utc) for ts in daily_sunrise]
daily_data["sunset"] = [datetime.fromtimestamp(ts, tz=timezone.utc) for ts in daily_sunset]

daily_data["uv_index_max"] = daily_uv_index_max
daily_data["daylight_duration"] = [
    f"{int(sec // 3600)}h {int((sec % 3600) // 60)}m"
    for sec in daily_daylight_duration
]

# Create the DataFrame
daily_dataframe = pd.DataFrame(data=daily_data)
print("\nDaily data\n", daily_dataframe)

hourly_dataframe.columns = [c.split()[0] for c in hourly_dataframe.columns]

import json
from pathlib import Path

# Create an output directory (optional)
output_dir = Path("surf_data")
output_dir.mkdir(exist_ok=True)

# Convert hourly data to JSON
hourly_json = hourly_dataframe.to_json(orient="records", date_format="iso")

# Save to file
with open(output_dir / "hourly_data.json", "w", encoding="utf-8") as f:
    f.write(hourly_json)

# Convert daily data to JSON
daily_json = daily_dataframe.to_json(orient="records", date_format="iso")

# Save to file
with open(output_dir / "daily_data.json", "w", encoding="utf-8") as f:
    f.write(daily_json)

print("\n✅ JSON files saved in 'surf_data/' folder:")
print(" - hourly_data.json")
print(" - daily_data.json")
