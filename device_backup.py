from netmiko import ConnectHandler
import datetime

# Target Devices List
devices = [
    {
        'device_type': 'cisco_ios',
        'host': '172.16.10.1',
        'username': 'admin',
        'password': 'Cisco123!',
        'name': 'R1'
    },
    {
        'device_type': 'cisco_ios',
        'host': '172.16.10.2',
        'username': 'admin',
        'password': 'Cisco123!',
        'name': 'R2'
    }
]

# Get Current Date for File Naming
today = datetime.date.today()

for device in devices:
    dev_name = device.pop('name')  # Name nikal kar log ke liye rakh rahe hain
    print(f"\n[+] Connecting to {dev_name} ({device['host']})...")

    try:
        net_connect = ConnectHandler(**device)
        print(f"[✓] Connected successfully to {dev_name}!")

        # Running Config Command Send Karo
        output = net_connect.send_command('show running-config')

        # File Mein Save Karo
        file_name = f"{dev_name}_backup_{today}.txt"
        with open(file_name, 'w') as f:
            f.write(output)

        print(f"[★] Backup saved: {file_name}")
        net_connect.disconnect()

    except Exception as e:
        print(f"[X] Failed to connect to {dev_name}: {e}")

print("\n🚀 All Device Backups Completed!")
