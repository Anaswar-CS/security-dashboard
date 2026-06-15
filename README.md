# 🛡️ Real-Time Security Dashboard

> A cybersecurity monitoring web app with live system metrics, port scanning, password strength analysis, and threat detection — built with Python Flask and JavaScript.

[![Backend](https://img.shields.io/badge/Backend-Python%20Flask-000000?logo=flask)](https://flask.palletsprojects.com)
[![Frontend](https://img.shields.io/badge/Frontend-JavaScript-F7DF1E?logo=javascript)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
[![Security](https://img.shields.io/badge/Domain-CyberSecurity-red?logo=shield)](https://owasp.org)
[![License](https://img.shields.io/badge/License-MIT-blue)](LICENSE)

---

## 🔍 Overview

A real-time security dashboard that gives you a live view of your system's security posture — monitoring metrics, scanning ports, analysing password strength, and detecting active threats, all from a single web interface.

---

## ✨ Features

### 📊 Live System Metrics
- Real-time CPU, memory, disk, and network usage
- Auto-refreshing dashboard — no manual reload needed

### 🔌 Port Scanner
- Scans open ports on a target host
- Classifies each port with a **risk level** (Low / Medium / High / Critical)
- Identifies common vulnerable services by port number

### 🔐 Password Strength Tester
- Analyses passwords against length, complexity, and pattern rules
- Scores strength and gives actionable improvement suggestions
- Checks against common weak password patterns

### 🚨 Security Threat Detection
- Detects active security threats and suspicious activity on the system
- Displays categorised alerts with severity levels

### 🌙 Dark Mode
- Toggle between light and dark themes
- Preference persists across sessions

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask |
| System Metrics | `psutil` |
| Port Scanning | `socket` / `python-nmap` |
| Frontend | HTML, CSS, JavaScript |
| Real-Time Updates | Fetch API / WebSocket |
| Styling | Custom CSS + Dark Mode toggle |

---

## 📂 Project Structure

```
security-dashboard/
├── app.py                        # Flask app & API routes
├── modules/
│   ├── system_monitor.py         # CPU, memory, disk, network metrics
│   ├── port_scanner.py           # Port scanning & risk classification
│   ├── password_checker.py       # Password strength analysis
│   └── threat_detector.py        # Security threat detection logic
├── static/
│   ├── js/
│   │   └── dashboard.js          # Real-time updates, dark mode toggle
│   └── css/
│       └── style.css             # Dashboard styles + dark theme
├── templates/
│   └── index.html                # Main dashboard UI
├── requirements.txt
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- pip

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/security-dashboard.git
   cd security-dashboard
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate      # Linux/macOS
   venv\Scripts\activate         # Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the app:
   ```bash
   python app.py
   ```

5. Open your browser at `http://localhost:5000`

---

## ⚠️ Legal & Ethical Notice

> Port scanning and network probing should only be performed on systems you own or have **explicit written permission** to test. Unauthorised scanning may be illegal in your jurisdiction. This tool is intended for **educational and authorised security testing** purposes only.

---

## 🗺️ Roadmap

- [ ] Authentication — login-protected dashboard
- [ ] Alert history log with timestamps
- [ ] Email / webhook notifications for critical threats
- [ ] Network traffic analysis
- [ ] Docker deployment support

---

## 🤝 Contributing

Contributions are welcome! Open an issue first to discuss major changes.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'Add your feature'`)
4. Push and open a Pull Request

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.


> *Because security visibility is the first step to security confidence.*
