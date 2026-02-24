import platform
import subprocess
import time

def check_ping(target, payload_size):
    """Test ping with a specific payload size and DF-bit set"""
    os_name = platform.system().lower()
    
    # Windows command
    if os_name == "windows":
        cmd = ['ping', '-n', '1', '-f', '-l', str(payload_size), '-w', '1000', target]
    # Linux and macOS command
    else:
        cmd = ['ping', '-c', '1', '-M', 'do', '-s', str(payload_size), '-W', '1', target]
        
    try:
        # Execute the command and capture output
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, errors='ignore')
        output = result.stdout.lower()
        
        # Check for fragmentation/drop errors
        if "fragmented" in output or "100% loss" in output or "timed out" in output or "unreachable" in output:
            return False
            
        # Check for successful reply
        if "reply from" in output or "bytes from" in output:
            return True
            
        return False
    except Exception as e:
        print(f"Error executing ping: {e}")
        return False

def find_optimal_mtu(target="8.8.8.8"):
    print(f"[*] Checking the path to server {target} ...")
    print("[*] Please wait a few seconds...\n")
    
    # Start searching from max payload size (1472 bytes payload = 1500 bytes MTU) downwards
    for size in range(1472, 1300, -2):
        print(f"[-] Testing payload size {size} bytes...")
        
        if check_ping(target, size):
            # Network Magic Math
            mtu = size + 28  # Add 28 bytes for IP and ICMP headers
            mss = mtu - 40   # Subtract 40 bytes to get the pure TCP MSS
            
            print("\n" + "="*55)
            print("✅ Scan completed successfully!")
            print("="*55)
            print(f"🎯 Maximum Payload size : {size} bytes")
            print(f"🌐 Actual Network MTU   : {mtu} bytes")
            print(f"🛡️ Optimal TCP-MSS      : {mss} bytes (Set this in FortiGate!)")
            print("="*55)
            return
        
        # Short delay to prevent flooding the router
        time.sleep(0.1)
            
    print("\n❌ No optimal size found! Ensure ICMP/Ping is allowed to the target.")

if __name__ == "__main__":
    # You can change the target IP here

    find_optimal_mtu("8.8.8.8")
