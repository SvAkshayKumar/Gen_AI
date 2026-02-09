import streamlit as st
import requests
from groq import Groq
import os

# KEYS
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

client = Groq(api_key=GROQ_API_KEY)

def ask_llm(prompt):
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.1-8b-instant"
    )
    return response.choices[0].message.content

st.title("✈️ AI Travel Planner Agent (Groq Powered)")

user_prompt = st.text_input("Enter your trip request:")

if st.button("Plan Trip"):

    # Extract city
    city_prompt = f"Extract only the city name from: {user_prompt}"
    city = ask_llm(city_prompt).strip()

    # Weather API
    weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
    weather_data = requests.get(weather_url).json()

    if "main" in weather_data:
        temp = weather_data["main"]["temp"]
        description = weather_data["weather"][0]["description"]
    else:
        temp = "N/A"
        description = "Weather not available"

    # Trip Plan
    plan_prompt = f"""
    Plan the trip based on: {user_prompt}
    Include:
    - Cultural significance
    - 3-day itinerary
    - Best attractions
    """

    trip_plan = ask_llm(plan_prompt)

    st.subheader("Destination")
    st.write(city)

    st.subheader("Current Weather")
    st.write(f"{temp}°C, {description}")

    st.subheader("Trip Plan")
    st.write(trip_plan)
