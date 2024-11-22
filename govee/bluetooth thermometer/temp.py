import requests
import json

url = "https://app2.govee.com/device/rest/devices/v1/list"
headers = {
    "Authorization": "", # Insert your Bearer Authorization token here
    "clientId": "", # Insert your clientId key here
    "appVersion": "6.2.30",
    "Content-Type": "application/json"
}
payload = {
    "key": "",
    "view": 0,
    "transaction": "" # Insert your transaction key here
}

response = requests.post(url, headers=headers, json=payload)

if response.status_code == 200:
    data = response.json()

    devices = data.get("devices", [])
    for device in devices:
        if device.get("sku") == "H5075": # Change this to the SKU of your device
            device_name = device.get("deviceName", "Unknown Device")
            device_ext = device.get("deviceExt", {})
            last_device_data = device_ext.get("lastDeviceData", "{}")
            device_settings = device_ext.get("deviceSettings", "{}")

            try:
                last_data = json.loads(last_device_data)
                temperature = last_data.get("tem")
                humidity = last_data.get("hum")

                settings_data = json.loads(device_settings)
                battery = settings_data.get("battery")

                formatted_temp = f"{temperature / 100:.1f}" if temperature is not None else "N/A"
                formatted_hum = f"{humidity / 100:.1f}" if humidity is not None else "N/A"
                battery_status = f"{battery}%" if battery is not None else "N/A"

                print(f"Device: {device_name}")
                print(f"  Temperature: {formatted_temp}°C")
                print(f"  Humidity: {formatted_hum}%")
                print(f"  Battery: {battery_status}")

            except json.JSONDecodeError:
                print(f"Failed to parse data for device: {device_name}")
else:
    print(f"Request failed with status code {response.status_code}: {response.text}")
