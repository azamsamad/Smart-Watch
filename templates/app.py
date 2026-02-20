# app.py
from flask import Flask, render_template, jsonify
import random
import time
from threading import Thread
from datetime import datetime

app = Flask(__name__)

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
    return render_template('index.html')

@app.route('/get_heart_rate')
def get_heart_rate():
    return jsonify({'heart_rate': monitor.heart_rate})

def run_monitor():
    monitor.start_monitoring()

if __name__ == '__main__':
    monitor.thread = Thread(target=run_monitor)
    monitor.thread.start()
    app.run(debug=True)