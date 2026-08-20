import subprocess
import json

query = '''[out:json];
area["name"="Oʻahu"]->.searchArea;
(
    way["natural"="beach"](area.searchArea);
    node["natural"="beach"](area.searchArea);
);
out center;'''

result = subprocess.run(
    [
        "curl",
        "-X", "POST",
        "https://overpass-api.de/api/interpreter",
        "--data", query
    ],
    capture_output=True,
    text=True
)

print(result.returncode)
print(result.stdout)

data = json.loads(result.stdout)

with open("beaches.json", "w") as f:
    json.dump(data, f, indent=2)
    pass