import re
import json
import requests
import urllib3
from datetime import datetime

urllib3.disable_warnings()

ES_URL = "https://search-openclassrooms-p5-edo-dz6knmpwrwvuhsfg7o7a5pfviu.us-east-1.es.amazonaws.com"
INDEX = "nginx-access"
USER = "admin"
PASS = "Admin123!"

pattern = re.compile(
    r'(?P<ip>\S+) - - \[(?P<time>[^\]]+)\] "(?P<method>\S+) (?P<path>\S+) (?P<protocol>[^"]+)" (?P<status>\d+) (?P<size>\d+) "(?P<referer>[^"]*)" "(?P<agent>[^"]*)"'
)

# Supprimer l'index existant
requests.delete(f"{ES_URL}/{INDEX}", auth=(USER, PASS), verify=False)

# Créer l'index avec le bon mapping
mapping = {
    "mappings": {
        "properties": {
            "time": {"type": "date", "format": "dd/MMM/yyyy:HH:mm:ss Z"},
            "status": {"type": "integer"},
            "size": {"type": "integer"}
        }
    }
}
requests.put(f"{ES_URL}/{INDEX}", auth=(USER, PASS), json=mapping, verify=False)

bulk_data = ""
count = 0

with open("nginx-access.log") as f:
    for line in f:
        m = pattern.match(line.strip())
        if m:
            doc = m.groupdict()
            doc["status"] = int(doc["status"])
            doc["size"] = int(doc["size"])
            bulk_data += json.dumps({"index": {"_index": INDEX}}) + "\n"
            bulk_data += json.dumps(doc) + "\n"
            count += 1

print(f"Envoi de {count} documents...")

r = requests.post(
    f"{ES_URL}/_bulk",
    auth=(USER, PASS),
    headers={"Content-Type": "application/x-ndjson"},
    data=bulk_data,
    verify=False,
    timeout=120
)

print(f"Status: {r.status_code}")
if r.status_code == 200:
    print("Import réussi !")
else:
    print(r.text[:500])