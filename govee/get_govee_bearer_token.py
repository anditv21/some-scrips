import requests
import json

def login():
    url = "https://app2.govee.com/account/rest/account/v1/login?host=app2.govee.com&appVersion=0311c551fb539335"
    
    email = input("Enter your email: ")
    password = input("Enter your password: ")
    
    body = {
        "client": "", # Insert some random clientId here
        "email": email,
        "password": password,
        "key": "",
        "view": 0,
        "transaction": "" # Insert some random transaction id here
    }
    
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=json.dumps(body), headers=headers)
    
    if response.status_code == 200:
        try:
            response_data = response.json()
            message = response_data.get("message", "").replace("\u00a0", " ")
            if message == "Login successful":
                print("Login successful")
                
                client_data = response_data.get("client", {})
                refresh_token = client_data.get("refreshToken")
                if refresh_token:
                    print(f"Refresh Token: {refresh_token}")
                else:
                    print("Refresh token not set")
                
                token = client_data.get("token")
                print(f"Token: {token}")
            else:
                print(f"Login failed: {message}")
        except json.JSONDecodeError:
            print("Error decoding JSON response. Full response:", response.text)
    else:
        print(f"Error: Unable to login, status code {response.status_code}")

if __name__ == "__main__":
    login()
