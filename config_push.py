from netmiko import ConnectHandler

# Target Devices List
devices = [
    {
        'device_type': 'cisco_ios',
        'host': '172.16.10.1',
        'username': 'admin',
        'password': 'Cisco123!',
        'loopback_ip': '1.1.1.1'
    },
    {
        'device_type': 'cisco_ios',
        'host': '172.16.10.2',
        'username': 'admin',
        'password': 'Cisco123!',
        'loopback_ip': '2.2.2.2'
    }
]

for device in devices:
    loop_ip = device.pop('loopback_ip')
    host_ip = device['host']
    print(f"\n[+] Pushing Configuration to {host_ip}...")

    # Configuration Commands List
    commands_to_send = [
        'interface Loopback0',
        f'ip address {loop_ip} 255.255.255.255',
        'no shutdown',
        'router ospf 1',
        'network 172.16.10.0 0.0.0.255 area 0',
        f'network {loop_ip} 0.0.0.0 area 0'
    ]

    try:
        net_connect = ConnectHandler(**device)
        # Bulk Config Push Command
        output = net_connect.send_config_set(commands_to_send)
        print(output)

        # Save Memory Command
        net_connect.save_config()
        print(f"[✓] Configuration applied & saved on {host_ip}!")
        net_connect.disconnect()

    except Exception as e:
        print(f"[X] Error on {host_ip}: {e}")

print("\n🎉 Bulk Automation Config Push Complete!")
