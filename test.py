from grist_api import GristDocAPI
import os
import streamlit as st

SERVER = "https://docs.getgrist.com"
DOC_ID = "nSV5r7CLQCWzKqZCz7qBor"
API_KEY = "3a00dc02645f6f36f4e1c9449dd4a8529b5e9149"

# Initialize GristDocAPI with document ID, server, and API key
api = GristDocAPI(DOC_ID, server=SERVER, api_key=API_KEY)

# Fetch data from the "Form2" table
data = api.fetch_table("Form2")
print(data)


# Funcon to load data from Grist
def charger_data_position():
    # Example: Fetch all rows from the "Form2" table
    data = api.fetch_table('Form2')
    
    # Display the data in Streamlit
    st.write("Loaded Data:")
    st.write(data)

# Button to trigger the data loading
if st.button("Charger le data position", type="primary", key=1):
    charger_data_position()
