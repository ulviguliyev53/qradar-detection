import os
import json
import requests
import urllib3

# SSL xətalarının qarşısını almaq üçün xəbərdarlıqları söndürürük
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

QRADAR_HOST = os.environ.get("QRADAR_HOST")
QRADAR_TOKEN = os.environ.get("QRADAR_TOKEN")

headers = {
    "SEC": QRADAR_TOKEN,
    "Content-Type": "application/json",
    "Accept": "application/json"
}

rules_dir = "rules/"

print(f"[*] QRadar-a qoşululur: {QRADAR_HOST}")

if not os.path.exists(rules_dir):
    print(f"[!] '{rules_dir}' qovluğu tapılmadı!")
    exit(1)

for filename in os.listdir(rules_dir):
    if filename.endswith(".json"):
        filepath = os.path.join(rules_dir, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            try:
                rule_data = json.load(f)
            except Exception as e:
                print(f"[ERROR] {filename} JSON oxunmadı: {e}")
                continue
            
            # QRadar Custom Rules API endpoint
            url = f"https://{QRADAR_HOST}/api/siem/custom_rules"
            
            response = requests.post(url, headers=headers, json=rule_data, verify=False)
            
            if response.status_code in [200, 201]:
                print(f"[SUCCESS] Rule uğurla yükləndi: {filename}")
            else:
                print(f"[ERROR] Rule yüklənmədi {filename}: {response.status_code} - {response.text}")
