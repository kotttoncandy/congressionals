import subprocess
import json

query = '''[out:json];
area["ISO3166-2"="US-HI"]->.searchArea;
(
    nwr["natural"="beach"]["name"](area.searchArea);
    nwr["leisure"="park"]["name"~"beach", i](area.searchArea);
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


data = json.loads(result.stdout)

with open("beaches.json", "w") as f:
    json.dump(data, f, indent=2)
    pass