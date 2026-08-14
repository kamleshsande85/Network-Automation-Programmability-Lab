import json
import yaml
from netmiko import ConnectHandler

# 1. Read JSON Inventory File
print("[+] Reading Device Inventory from inventory.json...")
with open("inventory.json", "r") as f:
    inventory_data = json.load(f)

# 2. Read YAML Configuration File
print("[+] Reading Config Template from config.yaml...")
with open("config.yaml", "r") as f:
    yaml_data = yaml.safe_load(f)

motd_banner = yaml_data["banners"]["motd"]
domain_name = yaml_data["domain_name"]

# 3. Loop through devices and push configuration
for router in inventory_data["routers"]:
    host = router["ip"]
    name = router["hostname"]

    device_dict = {
        'device_type': 'cisco_ios',
        'host': host,
        'username': router["username"],
        'password': router["password"],
    }

    print(f"\n[+] Connecting to {name} ({host})...")

    config_commands = [
        f"ip domain-name {domain_name}",
        f"banner motd #{motd_banner}#"
    ]

    try:
        net_connect = ConnectHandler(**device_dict)
        output = net_connect.send_config_set(config_commands)
        print(f"[✓] Successfully updated Domain & Banner on {name}!")
        net_connect.disconnect()

    except Exception as e:
        print(f"[X] Error configuring {name}: {e}")

print("\n🎉 Module 2 (JSON & YAML Automation) Successfully Executed!")
