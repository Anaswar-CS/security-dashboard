import psutil
import socket
import platform
import time
import subprocess
import re
from datetime import datetime

def get_system_info():
    """Get comprehensive system information"""
    try:
        disk = psutil.disk_usage('C:\\')
        disk_total = round(disk.total / (1024**3), 2)
        disk_usage_percent = disk.percent
    except:
        disk = psutil.disk_usage('/')
        disk_total = round(disk.total / (1024**3), 2)
        disk_usage_percent = disk.percent
    
    # Get boot time
    boot_time = datetime.fromtimestamp(psutil.boot_time())
    uptime = datetime.now() - boot_time
    uptime_str = f"{uptime.days}d {uptime.seconds//3600}h {(uptime.seconds//60)%60}m"
    
    info = {
        'os': platform.system(),
        'os_version': platform.version(),
        'os_release': platform.release(),
        'hostname': socket.gethostname(),
        'machine': platform.machine(),
        'processor': platform.processor(),
        'cpu_count': psutil.cpu_count(logical=True),
        'cpu_physical': psutil.cpu_count(logical=False),
        'memory_total': round(psutil.virtual_memory().total / (1024**3), 2),
        'cpu_usage': psutil.cpu_percent(interval=1),
        'memory_usage': psutil.virtual_memory().percent,
        'disk_total': disk_total,
        'disk_usage': disk_usage_percent,
        'uptime': uptime_str,
        'boot_time': boot_time.strftime('%Y-%m-%d %H:%M:%S')
    }
    return info

def get_running_processes():
    """Get detailed list of running processes"""
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_percent']):
        try:
            processes.append({
                'pid': proc.info['pid'],
                'name': proc.info['name'],
                'user': proc.info['username'],
                'cpu': round(proc.info['cpu_percent'] or 0, 1),
                'memory': round(proc.info['memory_percent'] or 0, 1)
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    
    # Sort by CPU usage
    processes.sort(key=lambda x: x['cpu'], reverse=True)
    return processes[:50]

def scan_open_ports():
    """Scan for commonly open ports on localhost"""
    common_ports = [20, 21, 22, 23, 25, 53, 80, 110, 135, 139, 143, 443, 445, 993, 995, 1433, 3306, 3389, 5432, 5900, 8080, 8443, 8888, 27017]
    open_ports = []
    
    for port in common_ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.3)
        result = sock.connect_ex(('127.0.0.1', port))
        if result == 0:
            open_ports.append({
                'port': port,
                'service': get_service_name(port),
                'risk': get_port_risk(port)
            })
        sock.close()
    
    return open_ports

def get_service_name(port):
    """Get common service names for ports"""
    services = {
        20: 'FTP-Data', 21: 'FTP', 22: 'SSH', 23: 'Telnet', 25: 'SMTP',
        53: 'DNS', 80: 'HTTP', 110: 'POP3', 135: 'RPC', 139: 'NetBIOS',
        143: 'IMAP', 443: 'HTTPS', 445: 'SMB', 993: 'IMAPS', 995: 'POP3S',
        1433: 'MSSQL', 3306: 'MySQL', 3389: 'RDP', 5432: 'PostgreSQL',
        5900: 'VNC', 8080: 'HTTP-Alt', 8443: 'HTTPS-Alt', 8888: 'HTTP-Proxy',
        27017: 'MongoDB'
    }
    return services.get(port, 'Unknown')

def get_port_risk(port):
    """Assess security risk of open port"""
    high_risk = [21, 23, 3389, 5900, 1433]  # FTP, Telnet, RDP, VNC, MSSQL
    medium_risk = [22, 80, 3306, 8080, 27017]  # SSH, HTTP, MySQL, etc
    
    if port in high_risk:
        return 'high'
    elif port in medium_risk:
        return 'medium'
    else:
        return 'low'

def get_network_connections():
    """Get active network connections"""
    connections = []
    for conn in psutil.net_connections(kind='inet'):
        if conn.status == 'ESTABLISHED':
            try:
                connections.append({
                    'local': f"{conn.laddr.ip}:{conn.laddr.port}",
                    'remote': f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "N/A",
                    'status': conn.status
                })
            except:
                pass
    return connections[:20]

def get_startup_programs():
    """Get Windows startup programs"""
    startup_programs = []
    try:
        if platform.system() == 'Windows':
            # Check startup registry keys
            import winreg
            keys = [
                r"Software\Microsoft\Windows\CurrentVersion\Run",
                r"Software\Microsoft\Windows\CurrentVersion\RunOnce"
            ]
            
            for key_path in keys:
                try:
                    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_READ)
                    for i in range(winreg.QueryInfoKey(key)[1]):
                        name, value, _ = winreg.EnumValue(key, i)
                        startup_programs.append({
                            'name': name,
                            'path': value[:100] + '...' if len(value) > 100 else value,
                            'location': 'HKCU\\' + key_path
                        })
                    winreg.CloseKey(key)
                except:
                    pass
    except Exception as e:
        startup_programs.append({'name': 'Unable to read', 'path': str(e), 'location': 'N/A'})
    
    return startup_programs[:15]

def check_password_strength(password):
    """Check password strength"""
    score = 0
    feedback = []
    
    # Length check
    if len(password) >= 12:
        score += 25
        feedback.append("✓ Good length")
    elif len(password) >= 8:
        score += 15
        feedback.append("⚠ Acceptable length, 12+ recommended")
    else:
        feedback.append("✗ Too short (minimum 8 characters)")
    
    # Complexity checks
    if re.search(r'[a-z]', password):
        score += 15
        feedback.append("✓ Contains lowercase")
    else:
        feedback.append("✗ Missing lowercase letters")
    
    if re.search(r'[A-Z]', password):
        score += 15
        feedback.append("✓ Contains uppercase")
    else:
        feedback.append("✗ Missing uppercase letters")
    
    if re.search(r'\d', password):
        score += 15
        feedback.append("✓ Contains numbers")
    else:
        feedback.append("✗ Missing numbers")
    
    if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        score += 20
        feedback.append("✓ Contains special characters")
    else:
        feedback.append("✗ Missing special characters")
    
    # Common patterns
    common_patterns = ['123', 'abc', 'password', 'qwerty']
    if any(pattern in password.lower() for pattern in common_patterns):
        score -= 20
        feedback.append("✗ Contains common pattern")
    
    # Determine strength
    if score >= 80:
        strength = "Strong"
        color = "green"
    elif score >= 60:
        strength = "Medium"
        color = "orange"
    else:
        strength = "Weak"
        color = "red"
    
    return {
        'score': max(0, min(100, score)),
        'strength': strength,
        'color': color,
        'feedback': feedback
    }

def perform_security_checks():
    """Comprehensive security checks"""
    checks = []
    
    # Get system info
    processes = get_running_processes()
    open_ports = scan_open_ports()
    cpu = psutil.cpu_percent(interval=1)
    mem = psutil.virtual_memory()
    disk = psutil.disk_usage('C:\\' if platform.system() == 'Windows' else '/')
    
    # Initial scan message
    checks.append({
        'check': 'System Scan Complete',
        'status': 'Comprehensive security analysis performed',
        'severity': 'info'
    })
    
    # Check for suspicious processes
    suspicious_names = ['mimikatz', 'netcat', 'nc.exe', 'psexec', 'metasploit', 'keylogger']
    for proc in processes:
        if any(sus in proc['name'].lower() for sus in suspicious_names):
            checks.append({
                'check': f"⚠️ Suspicious Process Detected",
                'status': f"{proc['name']} (PID: {proc['pid']}) - Review immediately",
                'severity': 'high'
            })
    
    # Check high-risk open ports
    high_risk_ports = [port for port in open_ports if port['risk'] == 'high']
    if high_risk_ports:
        port_list = ', '.join([str(p['port']) for p in high_risk_ports])
        checks.append({
            'check': '🔓 High-Risk Ports Open',
            'status': f"Ports {port_list} are exposed - Consider firewall rules",
            'severity': 'high'
        })
    
    # Check medium-risk ports
    medium_risk_ports = [port for port in open_ports if port['risk'] == 'medium']
    if len(medium_risk_ports) > 3:
        checks.append({
            'check': '⚠️ Multiple Services Exposed',
            'status': f"{len(medium_risk_ports)} medium-risk ports detected",
            'severity': 'medium'
        })
    
    # Check for RDP or VNC (remote access)
    remote_access = [p for p in open_ports if p['port'] in [3389, 5900]]
    if remote_access:
        checks.append({
            'check': '🌐 Remote Access Enabled',
            'status': 'RDP/VNC detected - Ensure strong authentication',
            'severity': 'medium'
        })
    
    # Check total processes
    total_procs = len(list(psutil.process_iter()))
    if total_procs > 300:
        checks.append({
            'check': '📊 High Process Count',
            'status': f'{total_procs} processes - May impact performance',
            'severity': 'medium'
        })
    else:
        checks.append({
            'check': '✓ Process Count Normal',
            'status': f'{total_procs} active processes',
            'severity': 'info'
        })
    
    # CPU usage check
    if cpu > 85:
        checks.append({
            'check': '🔥 Critical CPU Usage',
            'status': f'CPU at {cpu}% - System under heavy load',
            'severity': 'high'
        })
    elif cpu > 70:
        checks.append({
            'check': '⚠️ High CPU Usage',
            'status': f'CPU at {cpu}% - Monitor system performance',
            'severity': 'medium'
        })
    
    # Memory check
    if mem.percent > 90:
        checks.append({
            'check': '💾 Critical Memory Usage',
            'status': f'RAM at {mem.percent}% - Close applications immediately',
            'severity': 'high'
        })
    elif mem.percent > 80:
        checks.append({
            'check': '⚠️ High Memory Usage',
            'status': f'RAM at {mem.percent}% - Consider closing programs',
            'severity': 'medium'
        })
    else:
        checks.append({
            'check': '✓ Memory Usage Normal',
            'status': f'RAM at {mem.percent}%',
            'severity': 'info'
        })
    
    # Disk space check
    if disk.percent > 95:
        checks.append({
            'check': '💿 Critical Disk Space',
            'status': f'Disk at {disk.percent}% - Free space immediately',
            'severity': 'high'
        })
    elif disk.percent > 85:
        checks.append({
            'check': '⚠️ Low Disk Space',
            'status': f'Disk at {disk.percent}% - Clean up recommended',
            'severity': 'medium'
        })
    
    # Network connections check
    connections = get_network_connections()
    if len(connections) > 50:
        checks.append({
            'check': '🌐 Many Network Connections',
            'status': f'{len(connections)} active connections detected',
            'severity': 'medium'
        })
    
    return checks

def get_network_info():
    """Get network interface information"""
    network_info = []
    for interface, addrs in psutil.net_if_addrs().items():
        for addr in addrs:
            if addr.family == socket.AF_INET:  # IPv4
                network_info.append({
                    'interface': interface,
                    'ip': addr.address,
                    'netmask': addr.netmask
                })
                break
    return network_info

def get_system_metrics_history():
    """Get current system metrics for charting"""
    return {
        'cpu': psutil.cpu_percent(interval=0.5),
        'memory': psutil.virtual_memory().percent,
        'disk': psutil.disk_usage('C:\\' if platform.system() == 'Windows' else '/').percent,
        'timestamp': datetime.now().strftime('%H:%M:%S')
    }