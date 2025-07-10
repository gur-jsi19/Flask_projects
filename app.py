# Import necessary tools from Flask and the 'requests' library
from flask import Flask, render_template, request  # Flask tools for web app and templates
import requests  # To fetch data from the OpenWeatherMap API
import os

# Initialize the Flask application
app = Flask(__name__)  # Creates the Flask app object

# Route for the homepage (http://localhost:5000/)
@app.route('/')
def home():
    # Renders 'index.html' from the 'templates' folder
    return render_template('index.html')  # Sends HTML to the browser

@app.route('/weather')  # This decorator tells Flask to call this function when the '/weather' URL is visited
def get_weather():
    # STEP 1: Get the city name from the URL query parameters
    # Example: For "/weather?city=Noida", request.args.get('city') returns "Noida"
    city = request.args.get('city')  
    
    # STEP 2: API configuration
    API_KEY = os.environ.get('API_KEY')  # Add 'import os' at top
    #API_KEY = "15cc95f3b40b463ba47a89eacac9e4cd"  # Replace with your actual OpenWeatherMap API key
    
    try:  # Start error handling block
        # STEP 3: Build the API request URL
        # - q={city}: Specifies the city to search for
        # - units=metric: Returns temperature in Celsius
        # - appid: Your API key for authentication
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        
        # STEP 4: Make the API request and convert response to Python dictionary
        response = requests.get(url).json()  # .json() parses the API's JSON response
        
        # STEP 5: Check if the API returned an error
        # Successful responses have 'cod' (status code) 200
        # Failed responses have codes like 404 (city not found) or 401 (invalid API key)
        if response.get('cod') != 200:  
            # Get the error message from API or use default
            error_message = response.get('message', 'City not found')  
            # Render error template with HTTP status code 404
            return render_template('error.html', 
                                message=f"Error: {error_message.capitalize()}"), 404
        
        # STEP 6: Extract weather data from successful response
        weather_data = {
            'city': city,  # City name from user input
            'temperature': response['main']['temp'],  # Temperature from 'main' object
            'description': response['weather'][0]['description'],  # First weather condition
            'icon': response['weather'][0]['icon'],  # Icon code (e.g., "04d" for clouds)
        }
        
        # STEP 7: Render the weather template with the extracted data
        return render_template('weather.html', weather=weather_data)
        
    except Exception as e:  # Catch any unexpected errors (network issues, etc.)
        # STEP 8: Handle all other errors with a generic message
        return render_template('error.html', 
                           message="Unable to fetch weather data. Please try again."), 500

# Run the app if this script is executed directly
if __name__ == '__main__':
    app.run(debug=True)  # Enables auto-reload and debug mode