import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Jenkins URL and credentials
jenkins_url = "https://localhost:8080" # Add your jenkins URL 
username = "username"
api_token = "YOUR_API_TOKEN"

# API endpoint to retrieve global variables
api_url = f'{jenkins_url}/scriptText'

# Jenkins Groovy script to retrieve global variables
groovy_script = """
def globalNodeProperties = hudson.model.Hudson.instance.getGlobalNodeProperties()
def environmentVariablesNodeProperty = globalNodeProperties.get(hudson.slaves.EnvironmentVariablesNodeProperty)
def environmentVariables = environmentVariablesNodeProperty.getEnvVars()
environmentVariables.each { key, value ->
    println "$key: $value"
}
"""

# Send API request to execute the Groovy script
response = requests.post(api_url, auth=(username, api_token),verify=False, data={'script': groovy_script})

if response.status_code == 200:
    data = response.text.strip()
    print('Global Variables:')
    print(data)
else:
    print(f'Failed to retrieve global variables. Error: {response.text}')
