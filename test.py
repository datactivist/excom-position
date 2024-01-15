from grist_api import GristDocAPI
import os

SERVER = "https://docs.getgrist.com"
DOC_ID = "nSV5r7CLQCWzKqZCz7qBor"
API_KEY = st.secrets["grist_api_key"]

# Initialize GristDocAPI with document ID, server, and API key
api = GristDocAPI(DOC_ID, server=SERVER, api_key=API_KEY)

# Fetch data from the "Form2" table
data = api.fetch_table("Form2")
print(data)
