import requests

api_key = "3a00dc02645f6f36f4e1c9449dd4a8529b5e9149"

headers = {
    "Authorization": f"Bearer {api_key}"
}

subdomain = "docs"
doc_id = "nSV5r7CLQCWzKqZCz7qBor"
table_id = "Form2"


# Construct the URL using the provided variables
url = f"https://{subdomain}.getgrist.com/api/docs/{doc_id}/tables/{table_id}/records"
response = requests.get(url, headers=headers)

# Check the response status code
if response.status_code == 200:
    data = response.json()
    st.write(data)
    print("Houra")
    columns = data['records'][0]['fields'].keys()
    print(list(columns)[0])
    # Process the data as needed
else:
    print(f"Request failed with status code {response.status_code}")







# Send a GET request to the constructed URL
response = requests.get(url)

# Check the response status code
if response.status_code == 200:
    # Request was successful
    data = response.json()  # Get the response data in JSON format
    # Process the data as needed
else:
    # Request failed
    print(f"Request failed with status code {response.status_code}")