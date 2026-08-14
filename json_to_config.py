# ========================================
# json_to_config.py
# ========================================

import json
import paramiko

def load_inventory(filename):
    with open(filename, 'r') as f:
        return json.load(f)

def configure_device(device):
    print(f"Configuring {device['hostname']}...")
    # Add your config logic here

if __name__ == "__main__":
    inventory = load_inventory('inventory.json')
    for device in inventory['devices']:
        configure_device(device)
