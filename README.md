# HT10 BENCHSAFE: AI Monitor for an Electronics Workspace

A professional, fault-tolerant workspace safety monitoring dashboard and backend built for my Capstone Project. BENCHSAFE integrates multi-sensor telemetry (thermal, current, motion), object detection vision models, automated local LLM incident summaries, and an industrial-grade web interface to safeguard electronics workstations.

---

## 🚀 Key Features

* **Real-Time Workspace Telemetry:** Live monitoring gauges for soldering iron temperature (°C) and circuit load current (A).
* **AI Vision & Safety Overlays:** Dynamic pop-up warning banners inside the live camera feed for hazards like missing safety glasses or tools placed near table edges.
* **Persistent SQLite Logging (`benchsafe.db`):** All sensor events and vision triggers are permanently recorded with precise timestamps, ensuring historical audit logs survive server restarts.
* **Constrained Local LLM Integration:** Powered by Ollama (`Llama 3.2`) to generate concise, single-sentence safety incident summaries without redundant data repetition.
* **Automated Fault-Tolerance Heartbeat:** Background polling routine (`checkServerConnection`) monitors backend health every 4 seconds, automatically shifting the status indicator to a red `CONNECTION LOST` state if communication drops and recovering seamlessly.
* **Audit Log Search & CSV Export:** Built-in keyword search filter and one-click CSV export tool (`Export CSV`) for compliance reporting.
* **Web Audio Alarm System:** In-browser Web Audio API synthesizer that sounds a repeating pulse during critical alarms until acknowledged and reset by the operator.

---

## 🛠️ Tech Stack

* **Frontend:** HTML5, CSS3, JavaScript (Vanilla ES6), Web Audio API
* **Backend:** Python, FastAPI, SQLite
* **AI / LLM:** Ollama (`Llama 3.2`), Roboflow / YOLO (Object Detection)
* **Hardware Interfacing (Target):** ESP32-S3 Microcontroller, MLX90640 Thermal Camera, WCS1800 Current Sensor, Ultrasonic Motion Sensors (`HC-SR04`)

---

## 📂 Project Structure

```text
benchsafe-dashboard/
│
├── main.py             # FastAPI backend server & SQLite database setup
├── llm_engine.py       # Ollama LLM prompt constraints & incident summary logic
├── index.html          # Full-screen responsive operator dashboard UI
├── benchsafe.db        # Persistent SQLite incident log database (auto-generated)
└── README.md           # Project documentation
