from requests import post, auth
from config import settings

def trigger_jenkins() -> bool:
    jenkins_url = 'http://jenkins:8080/job/simple-pipeline/build'
    
    response = post(
        jenkins_url,
        auth=auth.HTTPBasicAuth(settings.jenkins_user, settings.jenkins_api_token)
    )

    if response.status_code == 201:
        print("Jenkins job triggered successfully.")
        return True
    else:
        print(f"Failed to trigger job: {response.status_code}, {response.text}")
        return False
