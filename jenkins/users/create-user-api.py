import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Jenkins URL and credentials
jenkins_url = "https://localhost:8080" # Add your jenkins URL 
username = "username"
api_token = "YOUR_API_TOKEN"

# User details
new_username = "johndoe"
new_password = "password"
new_fullname = "John Doe"
new_email = "john.doe@example.com"

# Create user API endpoint
api_endpoint = f"{jenkins_url}/securityRealm/createAccountByAdmin"

# JSON payload for creating the user
payload = {
    "username": new_username,
    "password1": new_password,
    "password2": new_password,
    "fullname": new_fullname,
    "email": new_email,
}

# Make the API request
response = requests.post(api_endpoint, data=payload, auth=(username, api_token), verify=False)

# Check the response status
if response.status_code == 200:
    print(f"User '{new_username}' created successfully.")
else:
    print(f"Failed to create user. Error: {response.text}")