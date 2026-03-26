import time
import random
import json
from datetime import datetime
import requests

# -------------------------------
# CONFIGURATION
# -------------------------------
CLOUD_URL = "https://your-project.firebaseio.com/data.json"  # Replace with your URL
SAVE_LOCAL_FILE = "health_data.json"
UPLOAD_TO_CLOUD = False  # Change to True when you have a real endpoint


# -------------------------------
# SENSOR SIMULATION FUNCTIONS
# -------------------------------
def get_heart_rate():
    return random.randint(60, 100)  # BPM


def get_spo2():
    return random.randint(94, 100)  # %


def get_temperature():
    return round(random.uniform(36.0, 37.5), 1)  # °C


def get_steps():
    return random.randint(0, 20)  # steps per interval


# -------------------------------
# DATA STORAGE
# -------------------------------
def save_locally(data):
    try:
        with open(SAVE_LOCAL_FILE, "r") as file:
            existing_data = json.load(file)
    except:
        existing_data = []

    existing_data.append(data)

    with open(SAVE_LOCAL_FILE, "w") as file:
        json.dump(existing_data, file, indent=4)


# -------------------------------
# CLOUD UPLOAD
# -------------------------------
def upload_to_cloud(data):
    if not UPLOAD_TO_CLOUD:
        return

    try:
        response = requests.post(CLOUD_URL, json=data)
        print("Cloud Response:", response.status_code)
    except Exception as e:
        print("Cloud Upload Failed:", e)


# -------------------------------
# MAIN LOOP
# -------------------------------
def run_watch():
    print("🚀 Smart Watch Monitoring Started...\n")

    total_steps = 0

    while True:
        heart_rate = get_heart_rate()
        spo2 = get_spo2()
        temperature = get_temperature()
        steps = get_steps()

        total_steps += steps

        data = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "heart_rate": heart_rate,
            "spo2": spo2,
            "temperature": temperature,
            "steps": total_steps
        }

        print("📊 Data:", data)

        # Save locally
        save_locally(data)

        # Upload to cloud
        upload_to_cloud(data)

        print("✅ Data saved\n")

        time.sleep(5)  # delay (5 seconds)


# -------------------------------
# ENTRY POINT
# -------------------------------
if __name__ == "__main__":
    run_watch()
    
    
import smtplib

def send_email_alert(message):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login("your_email@gmail.com", "your_password")

    server.sendmail(
        "your_email@gmail.com",
        "receiver@gmail.com",
        message
    )