import openpyxl
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

jenkins_url = "https://localhost:8080" # Add your jenkins host URL here
jenkins_username = "tejasmane"
jenkins_token = "YOUR_JENKINS_API_TOKEN"

excel_file_path = "PATH_TO_YOUR_EXCEL_FILE"
excel_sheet_name = "Jenkins_User_List"

password = "password"

def create_jenkins_user(username, name, email):
    user_data = {
        "username": username,
        "fullname": name,
        "email": email,
        "password1": password, 
        "password2": password,
    }

    create_user_url = f"{jenkins_url}/securityRealm/createAccountByAdmin"
    response = requests.post(
        create_user_url, data=user_data, auth=(jenkins_username, jenkins_token), verify=False
    )

    if response.status_code == 200:
        print(f"Successfully created user: {username}")
    else:
        print(f"Failed to create user: {username}")


wb = openpyxl.load_workbook(excel_file_path)
sheet = wb[excel_sheet_name]

for row in sheet.iter_rows(min_row=2, values_only=True):
    username = row[0]
    name = row[1]
    email = row[2]
    is_migrated = row[3]

    if not is_migrated:
        # check for empty values
        if None in (username, name, email):
            print(f"Error: Missing user details. Skipping user creation. - {username, name, email}")
            continue

        # check if the user already exists in Jenkins
        user_exists_url = f"{jenkins_url}/securityRealm/user/{username}"
        response = requests.get(user_exists_url, auth=(jenkins_username, jenkins_token), verify=False)

        if response.status_code == 200:
            print(f'User already exists: {username}')
            continue

        if response.status_code == 404:
            print(f"Creating new user... details - username = {username}, name = {name}, email = {email}")
            
            # User doesn't exist, create the user
            create_jenkins_user(username, name, email)
        else:
            print(f"User is already Migrated: {username}")

wb.close()