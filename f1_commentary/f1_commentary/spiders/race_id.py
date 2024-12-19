import json

# Load the links file
with open("links.json", "r") as file:
    links = json.load(file)

# Create a mapping of race IDs to links
race_id_to_link = {}
for link_data in links:
    url = link_data["link"]
    race_id = url.split("/")[-2]  # Extract race ID
    race_id_to_link[race_id] = url

# Save the mapping to a file for reference
with open("race_id_to_link.json", "w") as file:
    json.dump(race_id_to_link, file, indent=4)

print("Race ID to link mapping created and saved!")
