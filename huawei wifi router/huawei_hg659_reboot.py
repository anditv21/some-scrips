import sys
import json
import hashlib
import base64
from requests import session
from bs4 import BeautifulSoup
import re
from datetime import datetime
from colorama import Fore

ROUTER_IP = '192.168.1.1'

request_session = session()

def log_success(msg):
    time = datetime.now().strftime('%d.%m.%Y %H:%M:%S')
    print(f"[{time}] [{Fore.LIGHTCYAN_EX}LOG{Fore.RESET}] [✅] {msg}")

def log_failure(msg):
    time = datetime.now().strftime('%d.%m.%Y %H:%M:%S')
    print(f"[{time}] [{Fore.RED}LOG{Fore.RESET}] [❌] {msg}")

# Fetch CSRF tokens using the session
def fetch_csrf():
    try:
        # Sending GET request to fetch the initial page content
        request = request_session.get(f'http://{ROUTER_IP}')
        html = BeautifulSoup(request.text, 'html.parser')

        # Use regex to extract csrf_param and csrf_token from HTML
        match_param = re.search(r'<meta name="csrf_param" content="(.*?)"/>', request.text)
        match_token = re.search(r'<meta name="csrf_token" content="(.*?)"/>', request.text)

        if match_param and match_token:
            csrf_param = match_param.group(1)
            csrf_token = match_token.group(1)
            log_success("CSRF tokens acquired.")
            return csrf_param, csrf_token
        else:
            log_failure("Failed to extract CSRF tokens from HTML.")
            sys.exit(1)

    except Exception as e:
        log_failure(f"Failed to fetch CSRF tokens: {e}")
        sys.exit(1)

def login(username, password):
    try:
        csrf_param, csrf_token = fetch_csrf()

        # Step 1: SHA256 hash of password
        password_hash = hashlib.sha256(password.encode()).hexdigest()

        # Step 2: Base64 encode the SHA256 hash
        password_hash_b64 = base64.b64encode(password_hash.encode()).decode()

        # Step 3: Concatenate (USERNAME + base64_hash + csrf_param + csrf_token)
        final_hash_input = username + password_hash_b64 + csrf_param + csrf_token

        # Step 4: Final SHA256 hash
        password_hash_final = hashlib.sha256(final_hash_input.encode()).hexdigest()

        # log_success(f"Final password hash: {password_hash_final}")

        # Step 5: Prepare payload
        payload = {
            'csrf': {
                'csrf_param': csrf_param,
                'csrf_token': csrf_token
            },
            'data': {
                'UserName': username,
                'Password': password_hash_final
            }
        }

        headers = {
            'Content-Type': 'application/json',
            'Referer': f'http://{ROUTER_IP}/',
            'X-Requested-With': 'XMLHttpRequest'
        }

        # Login request
        request = request_session.post(f'http://{ROUTER_IP}/api/system/user_login', headers=headers, data=json.dumps(payload))
        response_content = request.text
        log_success(f"Response: {response_content}")

        data = json.loads(re.search(r'\{.*?\}', response_content).group(0))


        if data.get('errorCategory') == 'user_pass_err':
            log_failure("Incorrect username or password.")
            sys.exit(1)

        if data.get('csrf') == 'Menu.csrf_err':
            log_failure("Expired CSRF token. Fetching new tokens and retrying login.")
            return login(username, password)

        if data.get('errorCategory') == 'ok':
            log_success("Successfully logged in.")
            return data['csrf_param'], data['csrf_token']

        log_failure(f"Unexpected login response: {response_content}")
        sys.exit(1)

    except Exception as e:
        log_failure(f"Failed to login: {e}")
        sys.exit(1)

def reboot(csrf_param, csrf_token):
    try:
        data = {
            'csrf': {
                'csrf_param': csrf_param,
                'csrf_token': csrf_token
            }
        }


        request = request_session.post(f'http://{ROUTER_IP}/api/service/reboot.cgi', data=json.dumps(data, separators=(',', ':')))
        response_content = request.text
        data = json.loads(re.search(r'\{.*?\}', response_content).group(0))

        assert data['errcode'] == 0, data
        log_success("Rebooting")

    except Exception as e:
        log_failure(f"Failed to reboot: {e}")
        sys.exit(1)


if __name__ == '__main__':
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    csrf_param, csrf_token = login(username, password)
    reboot(csrf_param, csrf_token)
