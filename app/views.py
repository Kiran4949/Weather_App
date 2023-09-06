from django.shortcuts import render
import requests
from datetime import datetime, timedelta




# Create your views here.

def home(request):
    default_city = "solapur"
    default_date = datetime.now() - timedelta(days=3)  # Get the date 3 days ago

    if request.method == 'POST':
        city_name = request.POST.get('city_name', default_city)
        date = request.POST.get('date', default_date)
    else:
        city_name = default_city
        date = default_date

    # Fetch current weather data
    current_weather = fetch_current_weather(city_name)

    # Fetch forecast data for the next day
    forecast_data = fetch_3_day_forecast(city_name)

    # Fetch historical weather data for the last three days
    historical_weather_data = fetch_last_3_days_historical_weather(city_name)

    # Precompute icon URL for current weather
    current_weather['icon_url'] = get_weather_icon_url(current_weather['icon_code'])

    # Precompute icon URLs for forecast data
    for forecast in forecast_data:
        forecast['icon_url'] = get_weather_icon_url(forecast['icon_code'])

    if current_weather and forecast_data and historical_weather_data:
        return render(request, 'home.html', {'current_weather': current_weather, 'forecast_data': forecast_data, 'historical_weather_data': historical_weather_data})
    else:
        error_message = "City not found or data not available. Please try again."
        return render(request, 'home.html', {'error_message': error_message})



def fetch_current_weather(city_name):
    try:
        API_KEY = '89ee8309b2154bc883654402230509'
        url = f'http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city_name}&aqi=no'
        response = requests.get(url)
        data = response.json()
        
        icon_code = data['current']['condition']['icon']

        current_weather = {
            'location': data['location']['name'],
            'temperature': data['current']['temp_c'],
            'condition': data['current']['condition']['text'],
            'humidity': data['current']['humidity'],
            'wind_speed': data['current']['wind_kph'],
            'icon_code': icon_code,   # Include the icon_code in the current dictionary  
        }
        # Return the current data
        return current_weather
    except Exception as e:
        print(str(e))
        return None



def fetch_3_day_forecast(city_name):
    try:
        API_KEY = '89ee8309b2154bc883654402230509'
        url = f'http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={city_name}&days=3&aqi=no&alerts=no'
        response = requests.get(url)
        data = response.json()
        
        # Extract forecast data for the next 3 days
        forecast_data = []
        for day in data['forecast']['forecastday']:
            icon_code = day['day']['condition']['icon']

            forecast = {
                'date': day['date'],
                'max_temp': day['day']['maxtemp_c'],
                'min_temp': day['day']['mintemp_c'],
                'condition': day['day']['condition']['text'],
                'precipitation': day['day']['totalprecip_mm'],
                'icon_code': icon_code,  # Include the icon_code in the forecast dictionary
            }
            forecast_data.append(forecast)
        # Return the forecast data for the next 3 days
        return forecast_data
    except Exception as e:
        print(str(e))
        return None



def fetch_last_3_days_historical_weather(city_name):
    try:
        API_KEY = '89ee8309b2154bc883654402230509'
        end_date = datetime.now() - timedelta(days=1)  # Get the end date (yesterday)
        start_date = end_date - timedelta(days=2)  # Calculate the start date (3 days ago)
        
        # Format dates for the API request
        formatted_start_date = start_date.strftime('%Y-%m-%d')
        formatted_end_date = end_date.strftime('%Y-%m-%d')
        
        url = f'http://api.weatherapi.com/v1/history.json?key={API_KEY}&q={city_name}&dt={formatted_start_date}&end_dt={formatted_end_date}&aqi=no'
        response = requests.get(url)
        data = response.json()
        
        historical_weather_data = []

        for forecast in data['forecast']['forecastday']:
            icon_code = forecast['day']['condition']['icon']
            icon_url = get_weather_icon_url(icon_code)
            historical_weather = {
                'date': forecast['date'],
                'max_temp': forecast['day']['maxtemp_c'],
                'min_temp': forecast['day']['mintemp_c'],
                'condition': forecast['day']['condition']['text'],
                'precipitation': forecast['day']['totalprecip_mm'],
                'icon_url': icon_url,  # Make sure the icon_url is correctly set
            }
            historical_weather_data.append(historical_weather)
        # Return the historical data
        return historical_weather_data
    except Exception as e:
        print(str(e))
        return None



def get_weather_icon_url(icon_code):
    API_KEY = '89ee8309b2154bc883654402230509'
    return f'http:{icon_code}?apiKey={API_KEY}'












