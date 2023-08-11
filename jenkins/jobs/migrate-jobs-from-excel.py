import openpyxl
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Source jenkins server details
source_jenkins_url = "https://localhost:8080"
source_username = "username"
source_token = "JENKINS_SOURCE_TOKEN"

# Target server details
target_jenkins_url = "https://sw4jenkins01.dvms.local:8080"
target_username = "tejasmane"
target_token = "JENKINS_TARGET_TOKEN"

# Excel sheet path and sheet name
excel_file_path = "ADD_PATH_TO_YOUR_EXCEL_SHEET_FILE"
excel_sheet_name = "Sheet1" # Replace your sheet name here


wb = openpyxl.load_workbook(excel_file_path)
sheet = wb[excel_sheet_name]

for row in sheet.iter_rows(min_row=2, values_only=True):
    job_name = row[1]

    source_job_api_url = f"{source_jenkins_url}/job/{job_name}/api/json"
    source_headers = {
        "Authorization": f"Bearer {source_token}",
        "Jenkins-Crumb": "your_source_jenkins_crumb",
    }
    source_response = requests.get(
        source_job_api_url,
        headers=source_headers,
        auth=(source_username, source_token),
        verify=False,
    )

    if source_response.status_code != 200:
        print(f"Job '{job_name}' does not exist on the source Jenkins server. Skipping...")
        continue


    target_job_api_url = f"{target_jenkins_url}/job/{job_name}/api/json"
    target_headers = {
        "Authorization": f"Bearer {target_token}",
        "Jenkins-Crumb": "your_target_jenkins_crumb",
    }
    target_response = requests.get(
        target_job_api_url,
        headers=target_headers,
        auth=(target_username, target_token),
        verify=False,
    )

    if target_response.status_code == 200:
        print(f"Job '{job_name}' already exists on the target Jenkins server. Skipping...")
        continue

  
    source_job_api_url = f"{source_jenkins_url}/job/{job_name}/config.xml"
    source_headers["Accept"] = "application/xml"
    source_response = requests.get(
        source_job_api_url,
        headers=source_headers,
        auth=(source_username, source_token),
        verify=False,
    )

    if source_response.status_code != 200:
        print(
            f"Failed to retrieve job '{job_name}' from the source Jenkins server. Error: {source_response.text}"
        )
        continue


    target_job_create_api_url = f"{target_jenkins_url}/createItem?name={job_name}"
    target_headers["Content-Type"] = "application/xml"
    target_response = requests.post(
        target_job_create_api_url,
        headers=target_headers,
        data=source_response.content,
        auth=(target_username, target_token),
        verify=False,
    )

    if target_response.status_code == 200:
        print(f"Job '{job_name}' migrated successfully!")
    else:
        print(
            f"Failed to migrate job '{job_name}' to the target Jenkins server. Error: {target_response.text}"
        )

wb.close()
