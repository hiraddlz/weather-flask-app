from flask import Flask, render_template
import requests

app = Flask(__name__)

# The base URL for Open-Meteo API
API_URL = "https://api.open-meteo.com/v1/forecast"

# Function to get weather data from Open-Meteo API
def get_weather_data(latitude, longitude, weather_type='current'):
    params = {
        'latitude': latitude,
        'longitude': longitude,
        'current': 'temperature_2m,wind_speed_10m',
        'hourly': 'temperature_2m,relative_humidity_2m,wind_speed_10m' if weather_type == 'hourly' else ''
    }
    response = requests.get(API_URL, params=params)
    return response.json()

# Home route to show current weather
@app.route('/')
def index():
    latitude = 36.7783  # California
    longitude = -119.4179  # California

    current_weather = get_weather_data(latitude, longitude, weather_type='current')
    return render_template('index.html', current_weather=current_weather)

# Route to show hourly forecast
@app.route('/hourly')
def hourly():
    latitude = 36.7783  # California
    longitude = -119.4179  # California
    
    hourly_forecast = get_weather_data(latitude, longitude, weather_type='hourly')
    time_temp_data = zip(
        hourly_forecast['hourly']['time'],
        hourly_forecast['hourly']['temperature_2m'],
        hourly_forecast['hourly']['wind_speed_10m'] 
    ) 
    return render_template('index.html', hourly_forecast=time_temp_data)

if __name__ == '__main__':
    app.run(debug=True)
