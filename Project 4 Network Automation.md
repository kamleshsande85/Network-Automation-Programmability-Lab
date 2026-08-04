# 📁 Project 4: Network Automation & Programmability Lab

---

## 📌 Project Overview
This project demonstrates **network automation** using Python scripts to automate device configuration, backup, and monitoring. It bridges traditional networking with modern **DevOps** practices.

---

## 🎯 Objectives

| Module | Technology | Purpose |
|--------|------------|---------|
| **SSH Automation** | Python + Paramiko/Netmiko | Automated device backup |
| **Data Serialization** | JSON, YAML | Inventory & config management |
| **REST API** | Python + Requests | Programmatic device management |
| **Ansible (Simulated)** | Ansible Playbooks | Bulk configuration push |

---

## 🏗️ Lab Topology (GNS3)

```
┌────────────────────────────────────────────────────────────────────────────┐
│                         AUTOMATION LAB                                   │
│                                                                            │
│    ┌──────────────────────────────────────────────────────────────┐       │
│    │            Ubuntu VM (Control Node)                          │       │
│    │            Python + Netmiko + Ansible                       │       │
│    │            IP: 172.16.10.100/24                             │       │
│    └──────────────────────────┬───────────────────────────────────┘       │
│                               │ SSH (Port 22)                            │
│                               ▼                                          │
│    ┌──────────────────────────────────────────────────────────────┐       │
│    │              Cloud Node (GNS3 VM Bridge)                     │       │
│    │              IP: 172.16.10.1/24                             │       │
│    └──────────────────────────┬───────────────────────────────────┘       │
│                               │                                          │
│       ┌───────────────────────┼───────────────────────┐                  │
│       │                       │                       │                  │
│       ▼                       ▼                       ▼                  │
│  ┌─────────┐            ┌─────────┐            ┌─────────┐              │
│  │ Router1 │            │ Router2 │            │ Switch1 │              │
│  │172.16.  │            │172.16.  │            │172.16.  │              │
│  │10.1/24  │            │10.2/24  │            │10.10/24 │              │
│  └─────────┘            └─────────┘            └─────────┘              │
│                                                                            │
│   🔵 = Automation Components                                              │
└────────────────────────────────────────────────────────────────────────────┘
```

---

## ⚙️ Part 1: SSH Configuration on Network Devices (GNS3)

### Router1 (SSH Server)

```
! ========================================
! Router1 — SSH Configuration
! ========================================

hostname R1

! Domain & RSA Key
ip domain-name automation.local
crypto key generate rsa modulus 2048

! SSH Version 2
ip ssh version 2
ip ssh authentication-retries 3
ip ssh time-out 60

! Local User
username admin privilege 15 secret Cisco123!

! VTY (SSH Only)
line vty 0 4
 transport input ssh
 login local
 exec-timeout 10 0
 logging synchronous

! Interface for Management
interface gigabitethernet 0/0
 ip address 172.16.10.1 255.255.255.0
 no shutdown

! Save
end
write memory
```

**Verification:**
```
R1# show ip ssh
SSH Enabled - version 2.0
Authentication timeout: 60 secs; Authentication retries: 3
```

---

## 🐍 Part 2: Python Scripts

### 1. Device Backup Script (device_backup.py)

```python
#!/usr/bin/env python3
# ========================================
# device_backup.py
# ========================================

from netmiko import ConnectHandler
import time
import os

def backup_device(device_info):
    """
    Backup running-config from a network device
    """
    try:
        # Connect to device
        connection = ConnectHandler(**device_info)
        connection.enable()
        
        # Get hostname
        hostname = connection.send_command('show hostname')
        hostname = hostname.strip() or device_info['host']
        
        # Get running-config
        output = connection.send_command('show running-config')
        
        # Save to file
        timestamp = time.strftime('%Y%m%d_%H%M%S')
        filename = f"backup_{hostname}_{timestamp}.txt"
        
        with open(filename, 'w') as f:
            f.write(output)
        
        connection.disconnect()
        return f"✅ Backup saved: {filename}"
    
    except Exception as e:
        return f"❌ Failed: {e}"

if __name__ == "__main__":
    # Device details
    devices = [
        {
            'device_type': 'cisco_ios',
            'host': '172.16.10.1',
            'username': 'admin',
            'password': 'Cisco123!',
            'secret': 'Cisco123!',
            'port': 22,
        },
        {
            'device_type': 'cisco_ios',
            'host': '172.16.10.2',
            'username': 'admin',
            'password': 'Cisco123!',
            'secret': 'Cisco123!',
            'port': 22,
        },
        {
            'device_type': 'cisco_ios',
            'host': '172.16.10.10',
            'username': 'admin',
            'password': 'Cisco123!',
            'secret': 'Cisco123!',
            'port': 22,
        }
    ]
    
    # Backup each device
    for device in devices:
        print(backup_device(device))
```

**How to Run:**
```bash
cd ~/Project4-Automation/
python3 device_backup.py
```

**Expected Output:**
```
✅ Backup saved: backup_R1_20260804_120000.txt
✅ Backup saved: backup_R2_20260804_120001.txt
✅ Backup saved: backup_SW1_20260804_120002.txt
```

---

### 2. Bulk Config Push Script (config_push.py)

```python
#!/usr/bin/env python3
# ========================================
# config_push.py
# ========================================

from netmiko import ConnectHandler

def push_config(device_info, commands):
    """
    Push configuration commands to a device
    """
    try:
        connection = ConnectHandler(**device_info)
        connection.enable()
        
        output = connection.send_config_set(commands)
        
        # Save config
        connection.save_config()
        
        connection.disconnect()
        return f"✅ Configured {device_info['host']}"
    
    except Exception as e:
        return f"❌ Failed: {e}"

if __name__ == "__main__":
    # Commands to push
    config_commands = [
        'vlan 10',
        'name MANAGEMENT',
        'exit',
        'vlan 20',
        'name HR',
        'exit',
        'vlan 30',
        'name GUEST',
        'exit',
        'interface loopback 0',
        'ip address 10.10.10.1 255.255.255.255',
        'no shutdown',
        'exit',
        'ip route 0.0.0.0 0.0.0.0 172.16.10.1',
        'end',
        'write memory'
    ]
    
    # Device details
    devices = [
        {
            'device_type': 'cisco_ios',
            'host': '172.16.10.1',
            'username': 'admin',
            'password': 'Cisco123!',
            'secret': 'Cisco123!',
        },
        {
            'device_type': 'cisco_ios',
            'host': '172.16.10.2',
            'username': 'admin',
            'password': 'Cisco123!',
            'secret': 'Cisco123!',
        },
    ]
    
    for device in devices:
        print(push_config(device, config_commands))
```

**How to Run:**
```bash
python3 config_push.py
```

**Expected Output:**
```
✅ Configured 172.16.10.1
✅ Configured 172.16.10.2
```

---

### 3. JSON Inventory Management (inventory.json)

```json
{
  "devices": [
    {
      "hostname": "Router1",
      "ip": "172.16.10.1",
      "type": "router",
      "username": "admin",
      "password": "Cisco123!",
      "secret": "Cisco123!"
    },
    {
      "hostname": "Router2",
      "ip": "172.16.10.2",
      "type": "router",
      "username": "admin",
      "password": "Cisco123!",
      "secret": "Cisco123!"
    },
    {
      "hostname": "Switch1",
      "ip": "172.16.10.10",
      "type": "switch",
      "username": "admin",
      "password": "Cisco123!",
      "secret": "Cisco123!"
    }
  ]
}
```

**How to Use:**
```bash
cat inventory.json
python3 -m json.tool inventory.json
```

---

### 4. REST API Call Script (api_request.py)

```python
#!/usr/bin/env python3
# ========================================
# api_request.py
# ========================================

import requests
import json

# Disable SSL warnings (for lab only)
requests.packages.urllib3.disable_warnings()

def get_device_info(ip, username, password):
    """
    Fetch device information via REST API
    """
    url = f"https://{ip}/api/v1/devices"
    
    try:
        response = requests.get(
            url, 
            auth=(username, password), 
            verify=False,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            return json.dumps(data, indent=2)
        else:
            return f"Error: {response.status_code}"
    
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    result = get_device_info('172.16.10.1', 'admin', 'Cisco123!')
    print(result)
```

**How to Run:**
```bash
python3 api_request.py
```

---

## 🐍 Part 3: Ansible Setup (Ubuntu VM)

### 1. Inventory File (hosts.ini)

```ini
[network]
Router1 ansible_host=172.16.10.1 ansible_user=admin ansible_password=Cisco123!
Router2 ansible_host=172.16.10.2 ansible_user=admin ansible_password=Cisco123!
Switch1 ansible_host=172.16.10.10 ansible_user=admin ansible_password=Cisco123!
```

### 2. Ansible Playbook (config.yml)

```yaml
---
- name: Configure VLANs
  hosts: network
  gather_facts: no
  
  tasks:
    - name: Create VLAN 10
      ios_vlan:
        vlan_id: 10
        name: MANAGEMENT
        state: present
    
    - name: Create VLAN 20
      ios_vlan:
        vlan_id: 20
        name: HR
        state: present
    
    - name: Create VLAN 30
      ios_vlan:
        vlan_id: 30
        name: GUEST
        state: present
    
    - name: Create Loopback on all routers
      ios_interface:
        name: Loopback 0
        description: AUTOMATION
        state: present
    
    - name: Save configuration
      ios_command:
        commands:
          - write memory
```

### 3. Run Playbook

```bash
# Install ansible
sudo apt install ansible -y

# Run playbook
ansible-playbook -i hosts.ini config.yml
```

---

## 📸 Screenshot List (GitHub Ke Liye)

| # | Screenshot | Command |
|---|------------|---------|
| 1 | **GNS3 Topology** | GNS3 window |
| 2 | **Ubuntu VM Setup** | `ifconfig` output |
| 3 | **SSH to Router** | `ssh admin@172.16.10.1` |
| 4 | **Device Backup** | `python3 device_backup.py` |
| 5 | **Backup Files** | `ls -la backup_*.txt` |
| 6 | **JSON Inventory** | `cat inventory.json` |
| 7 | **REST API** | `python3 api_request.py` |
| 8 | **Ansible Playbook** | `ansible-playbook -i hosts.ini config.yml` |

---

## 🧪 Verification Commands

### On Ubuntu VM
```bash
# Test SSH connectivity
ssh admin@172.16.10.1
ssh admin@172.16.10.2

# Python script runs
python3 device_backup.py

# Ansible playbook
ansible-playbook -i hosts.ini config.yml
```

### On Network Devices
```
! Check configurations
show running-config | include vlan
show ip interface brief
show ip route
```

---

## 🎯 LinkedIn Post Template

> **"🚀 Project 4: Network Automation & Programmability Lab Completed!**
>
> **✅ Python + Netmiko:** Automated device backup
> **✅ JSON/YAML:** Structured data for automation
> **✅ REST API:** Programmatic device management
> **✅ Ansible:** Bulk configuration push
>
> **#NetworkAutomation #Python #NetDevOps #SDN #CCNA #GNS3"**

---

## 📂 GitHub Repository Structure

```
Project4-Automation/
├── README.md
├── scripts/
│   ├── device_backup.py
│   ├── config_push.py
│   └── api_request.py
├── data/
│   ├── inventory.json
│   └── config.yaml
├── ansible/
│   ├── hosts.ini
│   └── config.yml
├── screenshots/
│   ├── topology.png
│   ├── ssh-connect.png
│   ├── backup-run.png
│   ├── backup-files.png
│   └── ansible-run.png
└── backups/
    └── (generated .txt files)
```

---

**Bhai, yeh documentation complete hai!** 🎯

**GitHub push karo aur job applications start karo!** 🚀

**All the best! 💪**
