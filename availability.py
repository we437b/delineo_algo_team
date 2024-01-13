import json
import yaml
import csv
import numpy as np

# Load the JSON data from the file
with open('result_poi.json', 'r') as file:
    data = json.load(file)

with open('simul_settings.yaml', mode="r") as settingstream:
    settings = yaml.full_load(settingstream)

time_range = settings['time']
import csv
import numpy as np

# Assuming you already have 'data'

# Initialize sets to store unique person IDs and timestamps
person_ids = set()
timestamps = set()

# Extract unique person IDs and timestamps
for timestamp_key, poi_data in data.items():
    timestamp_idx = int(timestamp_key.split('_')[1])  # Extract the timestamp index from the key
    timestamps.add(timestamp_idx)

    for location_key, timestamp_list in poi_data.items():
        print(location_key)
        print(timestamp_list)
        for person_list in timestamp_list:
            for person in person_list:
                print(person)
                person_ids.add(person['id'])

# Convert sets to sorted lists
sorted_person_ids = sorted(list(person_ids))
sorted_timestamps = sorted(list(timestamps))

# Create a 2D array
result_array = np.zeros((len(sorted_person_ids), len(sorted_timestamps)), dtype=int)

# Fill the array with data
for i, person_id in enumerate(sorted_person_ids):
    for j, timestamp_idx in enumerate(sorted_timestamps):
        poi_key = f"id_{timestamp_idx}_Barnsdall Hs"
        timestamps_list = data.get(poi_key, [])
        for timestamp in timestamps_list:
            for person_list in timestamp:
                for person in person_list:
                    if person.get('id') == person_id:
                        result_array[i, j] = 1  # Person is at the location
                        break

# Create a CSV file
csv_file_path = 'result_matrix.csv'
with open(csv_file_path, 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)

    # Write header
    header = ['Person ID'] + [f'Timestamp {ts}' for ts in sorted_timestamps]
    writer.writerow(header)

    # Write data
    for i, person_id in enumerate(sorted_person_ids):
        row = [person_id] + list(result_array[i, :])
        writer.writerow(row)

print(f"CSV file created: {csv_file_path}")
