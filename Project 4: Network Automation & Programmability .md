**Bhai, bahut badhiya!** 🔥 

**Project 3** ka documentation complete hai, ab **Project 4: Network Automation & Programmability Lab** start karte hain. 

**Is project ka unique selling point (USP):** Ye project tumhe **doosre candidates se alag** karega, kyunki **90% network engineers automation nahi jaante** . Ye tumhare resume ko **"Future-Ready"** banayega.

---

## 📡 Project 4: Network Automation & Programmability Lab — Overview

### 🎯 Objectives

| Module | Technology | Purpose |
| :--- | :--- | :--- |
| **1. Device Configuration** | Python + SSH | Automate device configs |
| **2. Data Serialization** | JSON, YAML | Structured data handling |
| **3. REST APIs** | HTTP Methods | API testing with Postman |
| **4. Automation Tools** | Ansible (Simulated) | Configuration management |
| **5. SDN Concepts** | SDN Architecture | Future networking |

---

## 🏗️ Network Topology (Project 4)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    AUTOMATION LAB                                      │
│                                                                         │
│   ┌─────────────────────────────────────────────────────────────────┐   │
│   │              Python Automation Script                           │   │
│   │   (paramiko, netmiko, requests)                                │   │
│   └──────────────┬──────────────────────────────────────────────────┘   │
│                  │                                                     │
│                  │ SSH / REST API                                      │
│                  ▼                                                     │
│   ┌─────────────────────────────────────────────────────────────────┐   │
│   │                    Network Devices                              │   │
│   │                                                                 │   │
│   │  ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐        │   │
│   │  │ Router1 │   │ Router2 │   │ Switch1 │   │ Switch2 │        │   │
│   │  └─────────┘   └─────────┘   └─────────┘   └─────────┘        │   │
│   └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│   🔵 = Automation Components                                           │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## ⚙️ Part 1: Python Environment Setup (Kali Linux)

### Step 1: Install Python Libraries

```bash
pip install paramiko netmiko requests
```

### Step 2: Create Project Directory

```bash
mkdir ~/Project4-Automation
cd ~/Project4-Automation
```

---

## 🤖 Part 2: SSH-Based Device Automation

### 1. SSH Configuration Check (Cisco Device)

```
! ========================================
! Router1 — SSH Configuration
! ========================================

hostname Router1
ip domain-name automation.local
crypto key generate rsa modulus 2048
ip ssh version 2
username admin secret Cisco123!
line vty 0 4
 transport input ssh
 login local
```

### 2. Python Script — SSH Backup

```python
# ========================================
# device_backup.py
# ========================================

import paramiko
import time

def backup_running_config(host, username, password):
    try:
        # Create SSH client
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        # Connect to device
        client.connect(host, username=username, password=password, look_for_keys=False)
        
        # Send command
        channel = client.invoke_shell()
        time.sleep(1)
        channel.send('enable\n')
        time.sleep(1)
        channel.send('cisco123\n')
        time.sleep(1)
        channel.send('show running-config\n')
        time.sleep(2)
        
        # Read output
        output = channel.recv(65535).decode('utf-8')
        
        # Save to file
        filename = f"backup_{host}_{time.strftime('%Y%m%d_%H%M%S')}.txt"
        with open(filename, 'w') as f:
            f.write(output)
        
        client.close()
        return f"Backup saved: {filename}"
    
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    result = backup_running_config('172.16.10.1', 'admin', 'Cisco123!')
    print(result)
```

### 3. Python Script — Bulk Config Push

```python
# ========================================
# config_push.py
# ========================================

import paramiko
import time

def push_config(host, username, password):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, username=username, password=password, look_for_keys=False)
        
        channel = client.invoke_shell()
        time.sleep(1)
        
        # Enable
        channel.send('enable\n')
        time.sleep(1)
        channel.send('cisco123\n')
        time.sleep(1)
        
        # Commands to push
        commands = [
            'configure terminal',
            'interface loopback 0',
            'ip address 10.10.10.1 255.255.255.255',
            'no shutdown',
            'end',
            'write memory'
        ]
        
        for cmd in commands:
            channel.send(cmd + '\n')
            time.sleep(1)
        
        output = channel.recv(65535).decode('utf-8')
        client.close()
        return output
    
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    result = push_config('172.16.10.1', 'admin', 'Cisco123!')
    print(result)
```

---

## 📊 Part 3: JSON/YAML Data Serialization

### 1. Device Inventory (JSON)

```json
{
  "devices": [
    {
      "hostname": "Router1",
      "ip": "172.16.10.1",
      "type": "router",
      "username": "admin",
      "password": "Cisco123!"
    },
    {
      "hostname": "Router2",
      "ip": "172.16.10.2",
      "type": "router",
      "username": "admin",
      "password": "Cisco123!"
    },
    {
      "hostname": "Switch1",
      "ip": "172.16.10.10",
      "type": "switch",
      "username": "admin",
      "password": "Cisco123!"
    }
  ]
}
```

### 2. Python Script — JSON to Configuration

```python
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
```

### 3. Network Configuration (YAML)

```yaml
# ========================================
# config.yaml
# ========================================
vlans:
  - id: 10
    name: MANAGEMENT
  - id: 20
    name: HR
  - id: 30
    name: GUEST

interfaces:
  Gig0/0:
    description: UPLINK_TO_CORE
    ip: 172.16.7.17
    mask: 255.255.255.252
  Gig0/1:
    description: UPLINK_TO_ACCESS
    ip: 172.16.10.1
    mask: 255.255.255.0

ospf:
  process: 1
  router_id: 1.1.1.1
  networks:
    - network: 172.16.0.0
      wildcard: 0.0.255.255
      area: 0
```

---

## 🌐 Part 4: REST API Testing (Postman)

### 1. Enable REST API on Device (IOS-XE)

```
ip http server
ip http authentication local
rest api
```

### 2. API Endpoints

| Method | URL | Purpose |
|--------|-----|---------|
| `GET` | `/api/v1/devices` | List devices |
| `GET` | `/api/v1/devices/Router1/interfaces` | Get interface info |
| `POST` | `/api/v1/devices/Router1/config` | Push config |

### 3. Python Script — REST API Call

```python
# ========================================
# api_request.py
# ========================================

import requests
import json

def get_device_info(url, username, password):
    try:
        response = requests.get(url, auth=(username, password), verify=False)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            return f"Error: {response.status_code}"
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    url = "https://172.16.10.1/api/v1/devices"
    result = get_device_info(url, 'admin', 'Cisco123!')
    print(json.dumps(result, indent=2))
```

---

## ⚙️ Part 5: Ansible (Simulated)

### 1. Ansible Inventory (hosts.ini)

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
```

### 3. Python Script — Ansible Simulation

```python
# ========================================
= ansible_sim.py
# ========================================

import paramiko
import time

def ansible_sim(host, username, password, configs):
    print(f"Configuring {host}...")
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, username=username, password=password, look_for_keys=False)
        
        channel = client.invoke_shell()
        time.sleep(1)
        channel.send('enable\n')
        time.sleep(1)
        channel.send('cisco123\n')
        time.sleep(1)
        
        for cmd in configs:
            channel.send(cmd + '\n')
            time.sleep(1)
        
        output = channel.recv(65535).decode('utf-8')
        client.close()
        return f"{host}: Configured successfully"
    
    except Exception as e:
        return f"{host}: Error - {e}"

if __name__ == "__main__":
    configs = [
        'configure terminal',
        'vlan 10',
        'name MANAGEMENT',
        'exit',
        'vlan 20',
        'name HR',
        'exit',
        'end'
    ]
    
    devices = [
        ('172.16.10.1', 'admin', 'Cisco123!'),
        ('172.16.10.2', 'admin', 'Cisco123!'),
        ('172.16.10.10', 'admin', 'Cisco123!')
    ]
    
    for ip, user, pwd in devices:
        result = ansible_sim(ip, user, pwd, configs)
        print(result)
```

---

## 📸 Screenshot List (GitHub Ke Liye)

| # | Screenshot | Command |
|---|------------|---------|
| 1 | Python SSH Script | `python device_backup.py` |
| 2 | JSON Inventory | `cat inventory.json` |
| 3 | YAML Config | `cat config.yaml` |
| 4 | REST API Request | Postman output |
| 5 | Ansible Playbook | `ansible-playbook config.yml` |
| 6 | Automation Result | Device config output |

---

## 🎯 LinkedIn Post Template

> **"🚀 Project 4: Network Automation & Programmability Lab Completed!**
>
> **✅ Python + SSH automation (Paramiko)**
> **✅ JSON/YAML data serialization**
> **✅ REST API integration**
> **✅ Ansible configuration management**
> **✅ Modern network engineering skills!**
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
│   ├── json_to_config.py
│   ├── api_request.py
│   └── ansible_sim.py
├── data/
│   ├── inventory.json
│   └── config.yaml
├── screenshots/
│   ├── ssh-backup.png
│   ├── json-inventory.png
│   ├── yaml-config.png
│   └── api-request.png
└── configs/
    └── ansible-playbook.yml
```

---

**Bhai, Project 4 ka documentation ready hai!** 🎯

**Ab Project 5 (NOC Simulation) start karte hain?** 🚀
