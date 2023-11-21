import streamlit as st
import http.client
import json

# Set up the HTTP connection
conn = http.client.HTTPSConnection("api.collectapi.com")
headers = {
    'content-type': "application/json",
    'authorization': "apikey 2UAd7wewYfEGYFFsnRBvN7:75rYVYNWqAgQqIgEVroiB9"
    }

# Make the API request to get state codes
conn.request("GET", "/gasPrice/usaStateCode", headers=headers)
res = conn.getresponse()
st.write(res)
state_data = res.read()
state_data = json.loads(state_data)

# Extract the list of states
states = state_data["result"]

# Create the Streamlit web app
st.set_page_config(page_title="Fuelish Choices: Gas Price & Consumption Calculator", page_icon=None, layout="centered", initial_sidebar_state="auto", menu_items=None)
st.title("Gas Price Calculator")
st.header("Fuel Prices")

# Select a state
selected_state = st.selectbox("Select a state:", [state["name"] for state in states])

# Retrieve state code based on selected state
state_code = None
for state in states:
    if selected_state == state["name"]:
        state_code = state["code"]
        break

# If a state code is found, proceed to get city data
if state_code:
    # Make the API request to get city data
    conn.request("GET", f"/gasPrice/stateUsaPrice?state={state_code}", headers=headers)
    res = conn.getresponse()
    data = res.read()
    data = json.loads(data)

    # Extract city data
    cities = data["result"]["cities"]

    # Select a city
    selected_city = st.selectbox("Select a city:", [city["name"] for city in cities])

    # Display city details when button is clicked
    if st.button("Show Details"):
        for city in cities:
            if selected_city == city["name"]:
                st.subheader("Selected City: " + selected_city)
                st.write(f"Gasoline Price: {city['gasoline']} USD")
                st.write(f"Mid-Grade Price: {city['midGrade']} USD")
                st.write(f"Premium Price: {city['premium']} USD")
                st.write(f"Diesel Price: {city['diesel']} USD")
                break

    # Fuel Consumption Calculation based on distance and fuel efficiency
    st.header("Fuel Consumption Calculator")
    distance_miles = st.number_input("Enter the distance in miles:", min_value=0.0, value=0.0, step=1.0)
    fuel_efficiency = st.number_input("Enter fuel efficiency in miles per gallon (MPG):", min_value=0.0, value=20.0, step=1.0)

    if distance_miles > 0 and fuel_efficiency > 0:
        selected_fuel_price = None
        for city in cities:
            if selected_city == city["name"]:
                selected_fuel_price = city["gasoline"]  # You can change this to the desired fuel type
                break

        if selected_fuel_price:
            fuel_amount = distance_miles / fuel_efficiency
            fuel_cost = fuel_amount * float(selected_fuel_price)

            st.subheader("Fuel Consumption Details:")
            st.write(f"Distance: {distance_miles} miles")
            st.write(f"Fuel Efficiency: {fuel_efficiency} miles per gallon")
            st.write(f"Fuel Price: ${selected_fuel_price} per gallon")
            st.write(f"Fuel Amount Required: {fuel_amount:.2f} gallons")
            st.write(f"Total Fuel Cost: ${fuel_cost:.2f}")

else:
    st.error("Please select a valid state.")
