#!/usr/bin/env python3
from flask import Flask, render_template_string
import random
import time
from threading import Thread
from datetime import datetime

app = Flask(__name__)

# HTML Template (embedded in the Python file)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Heart Rate Monitor</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
            margin-top: 50px;
            background-color: #f5f5f5;
        }
        .container {
            background: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
            max-width: 500px;
            margin: 0 auto;
        }
        .heart-rate {
            font-size: 48px;
            color: #e74c3c;
            margin: 20px;
            font-weight: bold;
        }
        .heart {
            font-size: 100px;
            animation: beat 1s infinite alternate;
            margin: 20px;
        }
        @keyframes beat {
            to { transform: scale(1.2); }
        }
        .status {
            color: #2ecc71;
            font-weight: bold;
        }
        .last-update {
            color: #7f8c8d;
            font-size: 14px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>❤️ Heart Rate Monitor ❤️</h1>
        <div class="heart">❤️</div>
        <div class="heart-rate" id="heartRate">-- bpm</div>
        <div class="status" id="status">Monitoring...</div>
        <div class="last-update" id="lastUpdate"></div>
    </div>
    
    <script>
        function updateHeartRate() {
            fetch('/get_heart_rate')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('heartRate').textContent = data.heart_rate + ' bpm';
                    document.getElementById('lastUpdate').textContent = 'Last update: ' + data.timestamp;
                    
                    // Change color based on heart rate
                    if (data.heart_rate > 100) {
                        document.getElementById('heartRate').style.color = '#e74c3c'; // red
                        document.getElementById('status').textContent = 'High Heart Rate!';
                    } else if (data.heart_rate < 60) {
                        document.getElementById('heartRate').style.color = '#3498db'; // blue
                        document.getElementById('status').textContent = 'Low Heart Rate';
                    } else {
                        document.getElementById('heartRate').style.color = '#2ecc71'; // green
                        document.getElementById('status').textContent = 'Normal';
                    }
                })
                .catch(error => {
                    document.getElementById('status').textContent = 'Connection error';
                    console.error('Error:', error);
                });
        }
        
        // Update every second
        setInterval(updateHeartRate, 1000);
        updateHeartRate(); // Initial update
    </script>
</body>
</html>
"""

class HeartRateMonitor:
    def __init__(self):
        self.heart_rate = 72
        self.last_change_time = time.time()
        self.running = False
        self.thread = None

    def start_monitoring(self):
        self.running = True
        print("Heart Rate Monitor Started")
        while self.running:
            current_time = time.time()
            
            if current_time - self.last_change_time >= 30:
                self.randomly_adjust_heart_rate()
                self.last_change_time = current_time
            
            time.sleep(1)

    def randomly_adjust_heart_rate(self):
        change = random.randint(-10, 10)
        self.heart_rate += change
        self.heart_rate = max(60, min(self.heart_rate, 120))
        print(f"Heart rate adjusted to: {self.heart_rate} bpm")

    def stop_monitoring(self):
        self.running = False
        print("Heart Rate Monitor Stopped")

monitor = HeartRateMonitor()

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/get_heart_rate')
def get_heart_rate():
    return {
        'heart_rate': monitor.heart_rate,
        'timestamp': datetime.now().strftime("%H:%M:%S")
    }

def run_monitor():
    monitor.start_monitoring()

if __name__ == '__main__':
    monitor.thread = Thread(target=run_monitor)
    monitor.thread.daemon = True  # This ensures the thread stops when the main program exits
    monitor.thread.start()
    
    try:
        app.run(debug=True, use_reloader=False)
    except KeyboardInterrupt:
        monitor.stop_monitoring()
        monitor.thread.join()