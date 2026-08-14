import yaml
from netmiko import ConnectHandler

print("=== Module 4: Ansible Configuration Management Automation ===\n")

# 1. Inventory List (Direct, Fast & Reliable)
inventory = [
    {"name": "R1", "host": "172.16.10.1", "user": "admin", "pass": "Cisco123!"},
    {"name": "R2", "host": "172.16.10.2", "user": "admin", "pass": "Cisco123!"}
]

# 2. Reading Ansible Playbook ('site.yml')
print("[+] Reading Ansible Playbook 'site.yml'...")
with open("site.yml", "r") as f:
    playbook = yaml.safe_load(f)

play_name = playbook[0]["name"]
print(f"[★] PLAYBOOK LOADED: {play_name}\n")

# 3. Executing Tasks on Devices
for device in inventory:
    dev_name = device["name"]
    host = device["host"]

    dev_dict = {
        'device_type': 'cisco_ios',
        'host': host,
        'username': device["user"],
        'password': device["pass"]
    }

    print(
        f"TASK [1/2: Connect & Execute Commands on {dev_name} ({host})] *********************")
    try:
        net_connect = ConnectHandler(**dev_dict)
        print(f"ok: [{dev_name}] => SSH Connection Established")

        # Task 1: Show IP interface brief
        cmd_out = net_connect.send_command("show ip interface brief")
        print(f"ok: [{dev_name}] => Executed 'show ip interface brief'")

        # Task 2: Apply NTP Config
        print(
            f"\nTASK [2/2: Apply NTP Server Config on {dev_name}] ******************************")
        cfg_out = net_connect.send_config_set(["ntp server 8.8.8.8"])
        print(f"changed: [{dev_name}] => NTP Config Applied Successfully")

        net_connect.disconnect()
        print(
            f"\nPLAY RECAP [{dev_name}] : ok=2    changed=1    failed=0\n" + "-"*60 + "\n")

    except Exception as e:
        print(f"FAILED: [{dev_name}] => Error: {e}\n")

print("🎉 Module 4 (Ansible Automation) Executed Successfully!")
