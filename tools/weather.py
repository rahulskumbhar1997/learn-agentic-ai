from langchain.tools import tool
import requests
from langsmith import traceable

weather_schema = {
    "type": "object",
    "properties": {
        "latitude": {"type": "string", "description": "Latitude of the location"},
        "longitude": {"type": "string", "description": "Longitude of the location"},
        "current_fields": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Allowed values are ['temperature_2m', 'relative_humidity_2m', 'apparent_temperature', 'is_day', 'precipitation', 'rain', 'showers', 'snowfall', 'weather_code', 'cloud_cover', 'pressure_msl', 'surface_pressure', 'wind_speed_10m', 'wind_direction_10m', 'wind_gusts_10m']",
        },
        "hourly_fields": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Allowed values are ['temperature_2m', 'relative_humidity_2m', 'dew_point_2m', 'apparent_temperature', 'precipitation', 'rain', 'showers', 'snowfall', 'snow_depth', 'precipitation_probability', 'weather_code', 'cloud_cover', 'cloud_cover_low', 'cloud_cover_mid', 'cloud_cover_high', 'visibility', 'wind_speed_10m', 'wind_direction_10m', 'wind_gusts_10m', 'wind_speed_80m', 'wind_direction_80m', 'wind_speed_120m', 'wind_direction_120m', 'wind_speed_180m', 'wind_direction_180m', 'shortwave_radiation', 'direct_radiation', 'diffuse_radiation', 'direct_normal_irradiance', 'uv_index', 'uv_index_clear_sky', 'pressure_msl', 'surface_pressure', 'soil_temperature_0cm', 'soil_temperature_6cm', 'soil_temperature_18cm', 'soil_temperature_54cm', 'soil_moisture_0_1cm', 'soil_moisture_1_3cm', 'soil_moisture_3_9cm', 'soil_moisture_9_27cm', 'soil_moisture_27_81cm']",
        },
        "daily_fields": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Allowed values are ['temperature_2m_max', 'temperature_2m_min', 'apparent_temperature_max', 'apparent_temperature_min', 'sunrise', 'sunset', 'daylight_duration', 'sunshine_duration', 'precipitation_sum', 'rain_sum', 'showers_sum', 'snowfall_sum', 'precipitation_hours', 'precipitation_probability_max', 'wind_speed_10m_max', 'wind_gusts_10m_max', 'wind_direction_10m_dominant', 'weather_code', 'uv_index_max', 'uv_index_clear_sky_max']",
        },
    },
    "required": ["latitude", "longitude"],
}


@tool(
    args_schema=weather_schema,
    description="Get the weather details for provided coordinates.",
)
def get_weather(
    latitude: str,
    longitude: str,
    current_fields=None,
    hourly_fields=None,
    daily_fields=None,
):
    """
    Get the weather details for provided coordinates.
    """
    base_url = "https://api.open-meteo.com/v1/forecast"

    params = {"latitude": latitude, "longitude": longitude, "timezone": "auto"}

    # Add optional fields
    if current_fields:
        params["current"] = ",".join(current_fields)
    if hourly_fields:
        params["hourly"] = ",".join(hourly_fields)
    if daily_fields:
        params["daily"] = ",".join(daily_fields)

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error: {response.status_code} - {response.text}")
