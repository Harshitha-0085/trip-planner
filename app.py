import streamlit as st
import google.generativeai as genai

# Load secrets from Streamlit
GEMINI_KEY = st.secrets["GEMINI_API_KEY"]
MAPS_KEY = st.secrets["MAPS_API_KEY"]

# Configure Gemini
genai.configure(api_key=GEMINI_KEY)

st.title("🌍 AI Trip Planner")

destination = st.text_input("Destination", "Goa")
days = st.slider("Number of Days", 1, 10, 3)
budget = st.number_input("Budget (INR)", 1000, 100000, 15000)
theme = st.selectbox("Trip Theme", ["Heritage", "Nightlife", "Adventure", "Relax"])

if st.button("Generate Itinerary"):
    prompt = f"""
    You are a smart trip planner AI. 
    Destination: {destination}
    Days: {days}
    Budget: ₹{budget}
    Theme: {theme}

    Requirements:
    1. Break itinerary day by day (Day 1, Day 2, ...).
    2. Each day must have: Morning, Afternoon, Evening, Food, Cost, Hidden Gem.
    3. Keep total under budget and show total + savings at the end.
    4. Write in simple, clear sentences with emojis.
    """

    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    st.subheader("🗓️ Your Personalized Itinerary")
    st.write(response.text)

    st.subheader("📍 Destination Map")
    maps_url = f"https://www.google.com/maps/embed/v1/place?key={MAPS_KEY}&q={destination}"
    st.components.v1.iframe(maps_url, width=700, height=400)

    if st.button("Book Now 💳"):
        st.success("✅ Booking Confirmed! Payment received.")
        st.balloons()
