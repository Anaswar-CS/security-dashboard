def get_demo_system_info():
    """Fake system info for demo/LinkedIn video"""
    return {
        'os': 'Windows',
        'os_version': '10.0.19045',
        'os_release': '11',
        'hostname': 'SECURITY-LAPTOP',
        'machine': 'AMD64',
        'processor': 'Intel Core i7-12700K',
        'cpu_count': 12,
        'cpu_physical': 6,
        'memory_total': 32.0,
        'cpu_usage': 23.5,
        'memory_usage': 42.8,
        'disk_total': 1000.0,
        'disk_usage': 45.2,
        'uptime': '3d 12h 45m',
        'boot_time': '2025-01-05 08:30:00'
    }

def get_demo_processes():
    """Fake process list"""
    return [
        {'pid': 1234, 'name': 'chrome.exe', 'user': 'User', 'cpu': 12.3, 'memory': 8.5},
        {'pid': 5678, 'name': 'python.exe', 'user': 'User', 'cpu': 8.1, 'memory': 4.2},
        {'pid': 9012, 'name': 'Code.exe', 'user': 'User', 'cpu': 5.7, 'memory': 6.1},
        {'pid': 3456, 'name': 'explorer.exe', 'user': 'SYSTEM', 'cpu': 3.2, 'memory': 2.8},
        {'pid': 7890, 'name': 'svchost.exe', 'user': 'SYSTEM', 'cpu': 2.1, 'memory': 1.5},
    ]

def get_demo_open_ports():
    """Fake open ports"""
    return [
        {'port': 445, 'service': 'SMB', 'risk': 'low'},
        {'port': 3306, 'service': 'MySQL', 'risk': 'medium'}
    ]

def get_demo_security_checks():
    """Fake security checks"""
    return [
        {
            'check': 'System Scan Complete',
            'status': 'Comprehensive security analysis performed',
            'severity': 'info'
        },
        {
            'check': '✓ Process Count Normal',
            'status': '156 active processes',
            'severity': 'info'
        },
        {
            'check': '✓ Memory Usage Normal',
            'status': 'RAM at 42.8%',
            'severity': 'info'
        }
    ]

def get_demo_network_info():
    """Fake network interfaces"""
    return [
        {'interface': 'Wi-Fi', 'ip': '192.168.1.XXX', 'netmask': '255.255.255.0'},
        {'interface': 'Ethernet', 'ip': 'Not Connected', 'netmask': 'N/A'}
    ]

def get_demo_network_connections():
    """Fake network connections"""
    return [
        {'local': '192.168.1.XXX:54321', 'remote': 'XX.XX.XX.XX:443', 'status': 'ESTABLISHED'},
        {'local': '192.168.1.XXX:54322', 'remote': 'XX.XX.XX.XX:443', 'status': 'ESTABLISHED'}
    ]

def get_demo_startup_programs():
    """Fake startup programs"""
    return [
        {'name': 'OneDrive', 'path': 'C:\\Program Files\\Microsoft OneDrive\\OneDrive.exe', 'location': 'HKCU\\Run'},
        {'name': 'SecurityApp', 'path': 'C:\\Program Files\\SecurityApp\\app.exe', 'location': 'HKCU\\Run'}
    ]