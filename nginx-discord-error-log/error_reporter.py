import requests
import time


webhook_url = "https://discord.com/api/webhooks/xxxxxxxxxxxxxxxxxxx/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
nginx_error_log = "/var/log/nginx/error.log"

def send_to_discord(message):
    payload = {"content": message}
    response = requests.post(webhook_url, json=payload)
    if response.status_code == 204:
        print(f"Message successfully sent to Discord: ```{message}´´´")
    else:
        print(f"Failed to send message to Discord. Status code: {response.status_code}")

# Tail Nginx error log file
def tail_nginx_error_log():
    try:
        with open(nginx_error_log, "r") as file:
            file.seek(0, 2)
            while True:
                line = file.readline()
                if not line:
                    time.sleep(0.1)
                    continue
                yield line
    except FileNotFoundError:
        print(f"Nginx error log file {nginx_error_log} not found.")

if __name__ == "__main__":
    for line in tail_nginx_error_log():
        send_to_discord(line)
