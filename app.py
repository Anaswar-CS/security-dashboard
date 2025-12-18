from flask import Flask, render_template, jsonify, request
from scanner import *
from demo_data import *
import datetime
import json

# Demo mode toggle - Set to True for LinkedIn video!
DEMO_MODE = False  # Change to False for real data

app = Flask(__name__)

# Store scan history (in production, use a database)
scan_history = []

@app.route('/')
def dashboard():
    """Main dashboard page"""
    return render_template('index.html')

@app.route('/api/scan')
def perform_scan():
    """API endpoint to get security data"""
    
    # Use demo data if DEMO_MODE is True
    if DEMO_MODE:
        data = {
            'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'system_info': get_demo_system_info(),
            'processes': get_demo_processes(),
            'open_ports': get_demo_open_ports(),
            'security_checks': get_demo_security_checks(),
            'network_info': get_demo_network_info(),
            'network_connections': get_demo_network_connections(),
            'startup_programs': get_demo_startup_programs()
        }
    else:
        # Use real data
        data = {
            'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'system_info': get_system_info(),
            'processes': get_running_processes(),
            'open_ports': scan_open_ports(),
            'security_checks': perform_security_checks(),
            'network_info': get_network_info(),
            'network_connections': get_network_connections(),
            'startup_programs': get_startup_programs()
        }
    
    # Store in history (keep last 20 scans)
    scan_history.append({
        'timestamp': data['timestamp'],
        'cpu': data['system_info']['cpu_usage'],
        'memory': data['system_info']['memory_usage'],
        'open_ports': len(data['open_ports']),
        'processes': len(data['processes']),
        'issues': sum(1 for check in data['security_checks'] if check['severity'] in ['high', 'medium'])
    })
    
    if len(scan_history) > 20:
        scan_history.pop(0)
    
    return jsonify(data)

@app.route('/api/metrics')
def get_metrics():
    """Get current system metrics for real-time charts"""
    if DEMO_MODE:
        # Return demo metrics
        metrics = {
            'cpu': get_demo_system_info()['cpu_usage'],
            'memory': get_demo_system_info()['memory_usage'],
            'disk': get_demo_system_info()['disk_usage'],
            'timestamp': datetime.datetime.now().strftime('%H:%M:%S')
        }
    else:
        # Return real metrics
        metrics = get_system_metrics_history()
    return jsonify(metrics)

@app.route('/api/history')
def get_history():
    """Get scan history"""
    return jsonify(scan_history)

@app.route('/api/check-password', methods=['POST'])
def check_password():
    """Check password strength"""
    data = request.get_json()
    password = data.get('password', '')
    
    if not password:
        return jsonify({'error': 'No password provided'}), 400
    
    result = check_password_strength(password)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, port=5000)