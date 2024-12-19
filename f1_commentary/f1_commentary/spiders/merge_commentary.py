import json

# Load the commentary snippets
with open("commentary4.json", "r", encoding="utf-8") as file:  # Ensure proper encoding
    commentary_data = json.load(file)

# Load the race ID to link mapping
with open("race_id_to_link.json", "r", encoding="utf-8") as file:  # Ensure proper encoding
    race_id_to_link = json.load(file)

# Merge commentary snippets with their corresponding links
merged_data = []
for snippet in commentary_data:
    race_id = snippet["race_id"]  # Ensure commentary.json has the key 'race_id'
    link = race_id_to_link.get(race_id, None)  # Match race ID with its link
    if link:
        snippet["link"] = link  # Add the corresponding link to the snippet
    merged_data.append(snippet)

# Save the merged data to a new JSON file
with open("merged_commentary.json", "w", encoding="utf-8") as file:  # Save with proper encoding
    json.dump(merged_data, file, indent=4, ensure_ascii=False)  # Ensure Unicode is preserved

print("Merged data saved to merged_commentary.json!")

