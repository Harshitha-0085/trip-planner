import streamlit as st
import google.generativeai as genai
import time

# --- Load secrets ---
GEMINI_KEY = st.secrets["GEMINI_API_KEY"]
MAPS_KEY = st.secrets["MAPS_API_KEY"]

# Configure Gemini
genai.configure(api_key=GEMINI_KEY)

st.title("🌍 AI Trip Planner Demo")

# --- User Inputs ---
destination = st.text_input("Destination", "Goa")
days = st.slider("Number of Days", 1, 10, 3)
num_people = st.number_input("Number of People", 1, 10, 2)
budget = st.number_input("Budget (INR)", 1000, 100000, 15000)
theme = st.selectbox("Trip Theme", ["Heritage", "Nightlife", "Adventure", "Relax"])
food_pref = st.selectbox("Food Preference", ["Vegetarian", "Non-Veg", "Vegan", "Mixed"])

# --- Generate Itinerary ---
if st.button("Generate Itinerary"):
    st.info("Fetching optimized recommendations via Vertex AI...")
    time.sleep(1)  # simulate AI processing

    prompt = f"""
    You are a smart trip planner AI. 
    Destination: {destination}
    Days: {days}
    Number of People: {num_people}
    Budget: ₹{budget}
    Theme: {theme}
    Food Preference: {food_pref}

    Requirements:
    1. Break itinerary day by day (Day 1, Day 2, ...).
    2. Each day must have: Morning, Afternoon, Evening, Food, Cost, Hidden Gem.
    3. Adjust food recommendations based on Food Preference.
    4. Keep total under budget and show total + savings at the end.
    5. Write in simple, clear sentences with emojis.
    """

    try:
        model = genai.GenerativeModel("gemini-1.5-flash-latest")
        response = model.generate_content([prompt])
        st.subheader("🗓️ Personalized Itinerary (Gemini AI)")
        st.write(response.text)

        # Maps
        st.subheader("📍 Destination Map")
        maps_url = f"https://www.google.com/maps/embed/v1/place?key={MAPS_KEY}&q={destination}"
        st.components.v1.iframe(maps_url, width=700, height=400)

    except Exception as e:
        st.error(f"⚠️ Error generating itinerary: {e}")

# --- Demo Booking (Firebase simulation) ---
st.subheader("💳 Book Your Trip")
card_input = st.text_input("Enter mock card number (any number works)")

# In-memory Firebase simulation
if "bookings" not in st.session_state:
    st.session_state.bookings = []

if st.button("Book Now 💳"):
    if card_input.strip() == "":
        st.warning("Please enter a card number to proceed!")
    else:
        # Save booking to “Firebase” (simulated)
        st.session_state.bookings.append({
            "destination": destination,
            "days": days,
            "num_people": num_people,
            "budget": budget,
            "food_pref": food_pref
        })
        st.success("✅ Payment successful! Booking confirmed.")
        st.balloons()
        st.info(f"Trip to {destination} for {days} days ({num_people} people, {food_pref}) under ₹{budget} is booked!")

# --- BigQuery analytics simulation ---
st.subheader("📊 Trip Analytics (BigQuery Demo)")
popular_dest = "Goa"
avg_cost = 12500
total_bookings = len(st.session_state.bookings)

st.metric("Most popular destination", popular_dest)
st.metric("Average 3-day trip cost", f"₹{avg_cost}")
st.metric("Total bookings", total_bookings)
