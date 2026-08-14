import requests
import json

print("=== Module 3: REST API Interaction & Automation ===\n")

# 1. Simulating HTTP GET Request (Fetch Network Data from REST API Endpoint)
print("[+] Testing HTTP GET Request (Fetching Mock Device Inventory API)...")
get_url = "https://jsonplaceholder.typicode.com/todos/1"

try:
    response = requests.get(get_url, timeout=5)
    print(f"[✓] HTTP Response Status Code: {response.status_code} (OK)")

    # JSON Payload Parse Karo
    api_data = response.json()
    print("[★] Received API Data Payload:")
    print(json.dumps(api_data, indent=4))

except Exception as e:
    print(f"[X] GET Request Failed: {e}")

print("\n" + "="*50 + "\n")

# 2. Simulating HTTP POST Request (Pushing Config Payload via REST API)
print("[+] Testing HTTP POST Request (Pushing Configuration via REST API)...")
post_url = "https://jsonplaceholder.typicode.com/posts"

headers = {
    'Content-Type': 'application/json; charset=UTF-8'
}

payload = {
    "hostname": "R1-Core-Router",
    "interface": "GigabitEthernet0/0",
    "ip_address": "172.16.10.1",
    "status": "active"
}

try:
    post_response = requests.post(
        post_url, headers=headers, json=payload, timeout=5)
    print(
        f"[✓] HTTP Response Status Code: {post_response.status_code} (Created)")

    print("[★] Server Response Payload:")
    print(json.dumps(post_response.json(), indent=4))

except Exception as e:
    print(f"[X] POST Request Failed: {e}")

print("\n🎉 Module 3 (REST API Interaction) Successfully Executed!")
