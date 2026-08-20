import json

def get_island(lat, lon):

    # Oʻahu
    if 21.20 <= lat <= 21.75 and -158.30 <= lon <= -157.60:
        return "Oahu"

    # Kauaʻi
    if 21.80 <= lat <= 22.30 and -159.85 <= lon <= -159.20:
        return "Kauaʻi"

    # Maui
    if 20.55 <= lat <= 21.05 and -156.75 <= lon <= -155.90:
        return "Maui"

    # Hawaiʻi Island
    if 18.80 <= lat <= 20.30 and -156.10 <= lon <= -154.70:
        return "Hawaii"

    # Molokaʻi
    if 21.00 <= lat <= 21.25 and -157.30 <= lon <= -156.60:
        return "Molokai"

    # Lānaʻi
    if 20.70 <= lat <= 20.95 and -156.95 <= lon <= -156.70:
        return "Lanai"

    return None

def get_coordinates(beach):
    if "center" in beach:
        return beach["center"]["lat"], beach["center"]["lon"]
    else:
        return beach["lat"], beach["lon"]

with open("static/beaches.json", "r", encoding="utf-8") as f:
    data = json.load(f)

for beach in data["elements"]:

    lat, lon = get_coordinates(beach)

    if lat is None:
        beach["island"] = None
        continue

    name = beach.get("tags", {}).get("name", "Unnamed beach")

    print(f"Finding island for {name}...")

    beach["island"] = get_island(lat, lon).upper()


# Save the updated database
with open("beaches.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Done!")