import json

def get_island(lat, lon):

    if 21.22 <= lat <= 21.75 and -158.33 <= lon <= -157.62:
        return "Oahu"

    # Kauaʻi
    if 21.85 <= lat <= 22.30 and -159.85 <= lon <= -159.25:
        return "Kauai"

    # Maui
    if 20.55 <= lat <= 21.05 and -156.75 <= lon <= -155.90:
        return "Maui"

    # Hawaiʻi Island
    if 18.90 <= lat <= 20.30 and -156.10 <= lon <= -154.70:
        return "Hawaii"

    # Molokaʻi
    if 21.05 <= lat <= 21.25 and -157.35 <= lon <= -156.60:
        return "Molokai"

    # Lānaʻi
    if 20.70 <= lat <= 20.95 and -157.00 <= lon <= -156.70:
        return "Lanai"

    return "NOT ON MAIN ISLANDS"

def get_coordinates(beach):
    if beach["type"] == "node":
        lat = beach["lat"]
        lon = beach["lon"]
        return lat, lon
    else:
        lat = beach["center"]["lat"]
        lon = beach["center"]["lon"]
        return lat, lon

with open("beaches.json", "r", encoding="utf-8") as f:
    data = json.load(f)



for beach in data["elements"]:
    lat, lon = get_coordinates(beach)

    if lat is None or lon is None:
        beach["island"] = None
        continue
        
    name = beach.get("tags", {}).get("name", "Unnamed beach")

    print(f"Finding island for {name}...")

    beach["island"] = get_island(lat, lon).upper()


# Save the updated database
with open("beaches.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Done!")