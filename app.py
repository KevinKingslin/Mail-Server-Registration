from flask import Flask, request
from flask import render_template
import requests
import json
import ast

API_BASE_URL = "https://mail.twotwo1bbs.life/api/v1/"

app = Flask(__name__)

def createUser(email, name, password):
    headers = {"accept": "application/json", "Authorization": "E7APWA9UWZC13HFGH5Y53RY0UHF46KRM", "Content-Type": "application/json"}
    payload = {
        "email": email,
        "raw_password": password,
        "comment": "",
        "quota_bytes": 1000000000,
        "global_admin": False,
        "enabled": True,
        "enable_imap": True,
        "enable_pop": True,
        "allow_spoofing": False,
        "displayed_name": name,
    }
    payload = json.dumps(payload)
    r = requests.post('https://mail.twotwo1bbs.life/api/v1/user', data=payload, headers=headers)

def createDomain(domain):
    headers = {"accept": "application/json", "Authorization": "E7APWA9UWZC13HFGH5Y53RY0UHF46KRM", "Content-Type": "application/json"}
    payload = {
        "name": domain,
        "comment": "",
        "max_users": -1,
        "max_aliases": -1,
        "max_quota_bytes": 0,
        "signup_enabled": False,
    }
    payload = json.dumps(payload)
    r = requests.post('https://mail.twotwo1bbs.life/api/v1/domain', data=payload, headers=headers)

def generateKeys(domain):
    headers = {"accept": "application/json", "Authorization": "E7APWA9UWZC13HFGH5Y53RY0UHF46KRM", "Content-Type": "application/json"}
    r = requests.post(f'https://mail.twotwo1bbs.life/api/v1/domain/{domain}/dkim', headers=headers)

@app.route("/", methods = ['GET', 'POST'])
def index():
    if request.method == "GET":
        return render_template("index.html")
    elif request.method == "POST":
        data = request.get_data()
        data = ast.literal_eval(data.decode('utf-8'))

        name = data["displayName"]
        email = data["email"]
        domain = email.split('@')[1]
        password = data["password"]

        createDomain(domain)
        generateKeys(domain)
        createUser(email, name, password)

        return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 