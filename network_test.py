import socket
import subprocess
import platform
import os

def check_port_in_use(port):
    """Check if a port is in use"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def get_ip_addresses():
    """Get all IP addresses on the machine"""
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    
    print(f"Hostname: {hostname}")
    print(f"Local IP: {local_ip}")
    
    try:
        # Get all network interfaces
        if platform.system() == "Windows":
            # Windows command to get IP addresses
            result = subprocess.run(['ipconfig'], capture_output=True, text=True)
            print("\nNetwork Interfaces (ipconfig):")
            print(result.stdout)
        else:
            # Unix/Linux/Mac command to get IP addresses
            result = subprocess.run(['ifconfig'], capture_output=True, text=True)
            print("\nNetwork Interfaces (ifconfig):")
            print(result.stdout)
    except Exception as e:
        print(f"Error getting network interfaces: {e}")

def test_flask_binding():
    """Test if Flask can bind to different addresses"""
    from flask import Flask
    app = Flask(__name__)
    
    try:
        # Try binding to all interfaces
        print("\nTesting Flask binding to 0.0.0.0:5000...")
        app.run(host='0.0.0.0', port=5000, debug=False)
    except Exception as e:
        print(f"Error binding to 0.0.0.0:5000: {e}")

if __name__ == "__main__":
    print("===== Network Connectivity Test =====")
    
    # Check if port 5000 is already in use
    port_in_use = check_port_in_use(5000)
    print(f"\nIs port 5000 in use? {port_in_use}")
    
    # Get IP addresses
    get_ip_addresses()
    
    # Test Flask binding
    if not port_in_use:
        test_flask_binding()
    else:
        print("\nPort 5000 is already in use. Cannot test Flask binding.")
        
    print("\n===== Network Test Complete =====") 