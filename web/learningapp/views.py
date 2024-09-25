from django.shortcuts import render
from django.http import HttpResponseNotFound, HttpResponse, HttpResponseForbidden, HttpResponseNotAllowed
from django.conf import settings

import hashlib
import hmac
import requests

WEBHOOK_SECRET = settings.WEBHOOK_SECRET
JENKINS_USER = settings.JENKINS_USER
JENKINS_API_TOKEN = settings.JENKINS_API_TOKEN

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def custom_404_view(request, exception):
    return render(request, '404.html', status=404)

def github_webhook(request):
    if request.method == "POST":
        signature_header = request.headers.get("X-Hub-Signature-256")
        payload_body = request.body

        if not verify_signature(payload_body, WEBHOOK_SECRET, signature_header):
            return HttpResponseForbidden("Request signatures didn't match!")

        trigger_jenkins()
        return HttpResponse("Webhook received and Jenkins triggered successfully.")
    
    return HttpResponseNotAllowed("Invalid request method")

def trigger_jenkins():
    JENKINS_URL = 'http://jenkins:8080/job/testjob/build'
    JENKINS_USERNAME = JENKINS_USER
    JENKINS_TOKEN = JENKINS_API_TOKEN

    response = requests.post(
        JENKINS_URL,
        auth=HTTPBasicAuth(JENKINS_USERNAME, JENKINS_TOKEN)
    )

    if response.status_code == 201:
        print("Jenkins job triggered successfully.")
    else:
        print(f"Failed to trigger job: {response.status_code}, {response.text}")

def verify_signature(payload_body, secret_token, signature_header):
    """Verify that the payload was sent from GitHub by validating SHA256.

    Args:
        payload_body: original request body to verify (request.body)
        secret_token: GitHub app webhook token (WEBHOOK_SECRET)
        signature_header: header received from GitHub (x-hub-signature-256)
    """
    if not signature_header:
        return False
    hash_object = hmac.new(secret_token.encode('utf-8'), msg=payload_body, digestmod=hashlib.sha256)
    expected_signature = "sha256=" + hash_object.hexdigest()
    return hmac.compare_digest(expected_signature, signature_header)
