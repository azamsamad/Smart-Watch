import smtplib
import platform
import os

# -------------------------------
# ALERT THRESHOLDS
# -------------------------------
MAX_HEART_RATE = 100
MIN_SPO2 = 92
MAX_TEMPERATURE = 38.0

# -------------------------------
# SOUND ALERT
# -------------------------------
def play_alert_sound():
    if platform.system() == "Windows":
        import winsound
        winsound.Beep(1000, 1000)  # frequency, duration
    else:
        os.system('echo "\a"')  # mac/linux beep


# -------------------------------
# EMAIL ALERT
# -------------------------------
def send_email_alert(subject, message):
    sender_email = "your_email@gmail.com"
    receiver_email = "receiver@gmail.com"
    password = "your_app_password"  # NOT your real password (use App Password)

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, password)

        full_message = f"Subject: {subject}\n\n{message}"
        server.sendmail(sender_email, receiver_email, full_message)

        server.quit()
        print("📧 Email alert sent!")

    except Exception as e:
        print("❌ Email failed:", e)


# -------------------------------
# ALERT CHECK FUNCTION
# -------------------------------
def check_alerts(data):
    alerts = []

    # Heart Rate Alert
    if data["heart_rate"] > MAX_HEART_RATE:
        alerts.append(f"High Heart Rate: {data['heart_rate']} BPM")

    # SpO2 Alert
    if data["spo2"] < MIN_SPO2:
        alerts.append(f"Low SpO2: {data['spo2']}%")

    # Temperature Alert
    if data["temperature"] > MAX_TEMPERATURE:
        alerts.append(f"High Temperature: {data['temperature']}°C")

    # If any alerts triggered
    if alerts:
        print("\n🚨 ALERT TRIGGERED 🚨")
        
        for alert in alerts:
            print("⚠️", alert)

        # Play sound
        play_alert_sound()

        # Send email
        send_email_alert(
            "🚨 Smart Watch Health Alert",
            "\n".join(alerts)
        )

    else:
        print("✅ All vitals normal")


# -------------------------------
# TEST DATA (Replace with real data)
# -------------------------------
if __name__ == "__main__":
    sample_data = {
        "heart_rate": 110,
        "spo2": 89,
        "temperature": 38.5
    }

    check_alerts(sample_data)
