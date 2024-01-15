# Import necessary libraries
import requests  # Library for making HTTP requests
import os  # Library for interacting with the operating system
from datetime import datetime, timedelta  # Libraries for working with dates and times
import streamlit as st  # Library for creating web applications
import pandas as pd  # Library for data manipulation
from dotenv import load_dotenv  # Library for loading environment variables

# Load environment variables from a .env file
load_dotenv()

# Retrieve API key and URL from environment variables
api_key = os.getenv("API_KEY")  # Get the API key from environment variables
url = os.getenv("URL")  # Get the API URL from environment variables

# Define a function to get weather information for a given city
def getweather(city):
    # Make a GET request to the OpenWeatherMap API
    result = requests.get(url.format(city, api_key))
    
    # Check if the request was successful
    if result:
        # Convert the API response to JSON format
        api_dataa = result.json()
        
        # Extract relevant information from the API response
        country = api_dataa['sys']['country']  # Extract country information
        temp_city = ((api_dataa['main']["temp"]) - 273.15)  # Convert temperature to Celsius
        weather_desc = api_dataa['weather'][0]['description']  # Extract weather description
        hmdt = api_dataa['main']['humidity']  # Extract humidity
        wind_speed = api_dataa['wind']['speed']  # Extract wind speed
        icon = api_dataa['weather'][0]['icon']  # Extract weather icon code
        lon = api_dataa['coord']['lon']  # Extract longitude
        lat = api_dataa['coord']['lat']  # Extract latitude
        date_time = datetime.now().strftime("%d %b %Y | %I:%M:%S %p")  # Get current date and time
        
        # Create a list with the extracted information
        res = [country, round(temp_city, 1), weather_desc, hmdt, wind_speed,
               icon, lon, lat, date_time]
        
        # Return the list and the full API response for potential further use
        return res, api_dataa
    else: 
        # Print an error message if the request was not successful
        print("Error in search!")

# Streamlit web application code
st.title('Weather Application')  # Set the title of the web application

# Create two columns for the layout
col1, col2 = st.columns(2)

# Accept user input for the city name
with col1:
    place_name = st.text_input("Please enter your city ")  # Get user input for the city name

# Display map and weather information
with col2:  
    if place_name:
        # Call the getweather function to retrieve weather information
        res, api_dataa = getweather(place_name)
        
        # Display the location on a map using latitude and longitude
        st.map(pd.DataFrame({'lat': [res[7]], 'lon': [res[6]]}, columns=['lat', 'lon']))
        
        # Display current weather details using Streamlit components
        st.success("Date & Time : " + str(res[8]))  # Show the current date and time
        st.success("Current : " + str(round(res[1], 2)))  # Display the current temperature
        st.info("Description : " + str(res[2]))  # Show the weather description
        st.info("Humidity : " + str(round(res[3], 2)))  # Display the humidity
        st.info("Wind Speed : " + str(res[4]))  # Display the wind speed
        
        # Display the weather icon using an image link in Markdown format
        web_str = "![Alt Text]" + "(http://openweathermap.org/img/wn/" + str(res[5]) + "@2x.png)"
        st.markdown(web_str)
