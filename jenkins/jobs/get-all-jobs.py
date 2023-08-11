import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Source Jenkins server details
source_jenkins_url = "https://localhost:8080"
username = "username"
api_token = "JENKINS_SOURCE_TOKEN"

# Get all jobs from the source Jenkins server
source_api_url = f"{source_jenkins_url}/api/json"
source_jobs_response = requests.get(source_api_url, auth=(username, api_token), verify=False)
if source_jobs_response.status_code != 200:
    print(
        f"Failed to retrieve jobs from the source Jenkins server. Error: {source_jobs_response.text}"
    )
    exit(1)

source_jobs = source_jobs_response.json()["jobs"]

# Iterate over the source jobs and create them on the target Jenkins server
for source_job in source_jobs:
    job_name = source_job["name"]
    print(job_name)
    source_job_api_url = f"{source_jenkins_url}/job/{job_name}/config.xml"
    print(source_job_api_url)
    source_job_response = requests.get(source_job_api_url, auth=(username, api_token), verify=False)
    if source_job_response.status_code != 200:
        print(
            f"Failed to retrieve job '{job_name}' from the source Jenkins server. Error: {source_job_response.text}"
        )
        continue
