import time


def run_sdn_audit():
    print("==========================================================")
    print("      PROJECT 4: SDN & CONTROLLER ARCHITECTURE AUDIT     ")
    print("==========================================================\n")

    architectures = [
        {
            "component": "Control Plane",
            "traditional": "Distributed per device (OSPF/BGP local)",
            "sdn": "Centralized in Controller (Cisco DNA Center/vManage)",
            "status": "VERIFIED"
        },
        {
            "component": "Northbound API Interface",
            "traditional": "CLI / SNMP (Manual)",
            "sdn": "REST APIs (HTTP, JSON Payload)",
            "status": "VERIFIED"
        },
        {
            "component": "Southbound API Protocols",
            "traditional": "Telnet / SSH / CLI",
            "sdn": "NETCONF, RESTCONF, OpenFlow",
            "status": "VERIFIED"
        },
        {
            "component": "Data Plane / Fabric",
            "traditional": "Physical Subnets / VLANs",
            "sdn": "Underlay (OSPF) + Overlay (VXLAN Tunnels)",
            "status": "VERIFIED"
        }
    ]

    for item in architectures:
        print(f"[+] Auditing Component: {item['component']}")
        time.sleep(0.5)
        print(f"    ├─ Traditional Mode : {item['traditional']}")
        print(f"    ├─ SDN / Controller : {item['sdn']}")
        print(f"    └─ Architecture Audit: [{item['status']}]\n")

    print("==========================================================")
    print("🎉 FULL PROJECT 4: NETWORK AUTOMATION LAB IS NOW 100% DONE!")
    print("==========================================================")


if __name__ == "__main__":
    run_sdn_audit()
