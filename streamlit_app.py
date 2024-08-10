import streamlit as st
import requests
from bs4 import BeautifulSoup

# Title of the application
st.title("Doctor Availability Scraper")

# Input for location
location = st.text_input("Enter the location:")

# Dropdown for specialization
specializations = ["General Physician", "Dentist", "Dermatologist", "Cardiologist", "Gynecologist", "Pediatrician"]
specialization = st.selectbox("Select specialization:", specializations)

# Scrape button
scrape_button = st.button("Scrape")


# Function to scrape Practo
def scrape_practo(location, specialization):
    # Format location and specialization to match URL format
    location = location.lower().replace(" ", "-")
    specialization = specialization.lower().replace(" ", "-")

    # URL construction
    url = f"https://www.practo.com/{location}/doctors?specialization={specialization}"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract the number of doctors
        try:
            total_doctors = soup.find('h1').get_text().strip()
            total_doctors = int(total_doctors.split()[0])
        except:
            total_doctors = 0
    else:
        total_doctors = 0

    return total_doctors


# Trigger the scraping when the button is clicked
if scrape_button:
    if location and specialization:
        with st.spinner("Scraping data..."):
            total_doctors = scrape_practo(location, specialization)
            st.success(f"Total number of available doctors: {total_doctors}")
    else:
        st.warning("Please enter both location and specialization.")
