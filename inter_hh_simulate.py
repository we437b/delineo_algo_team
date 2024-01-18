import json
import yaml
import csv
import numpy as np

def generate_intra_household_visits(
        availability_matrix, household_info, 
        individual_movement_frequency, social_event_frequency,
        regular_visitation_frequency, school_children_frequency
    ):
    num_timestamps = availability_matrix.shape[1]
    num_persons = availability_matrix.shape[0]

    result_array = np.zeros((num_persons, num_timestamps), dtype=int)

    for timestamp in range(num_timestamps):
        for person_id in range(num_persons):
            # Check if the person is available at the given timestamp
            if availability_matrix[person_id, timestamp] == 1:
                # Check household relationships
                household_id = household_info[person_id]['household_id']
                household_members = [p['id'] for p in household_info if p['household_id'] == household_id]

                # Generate individual movement
                if np.random.rand() < individual_movement_frequency:
                    result_array[person_id, timestamp] = 1

                # Generate social event visit
                if np.random.rand() < social_event_frequency:
                    other_household_members = [
                        p for p in household_info if p['household_id'] != household_id
                    ]
                    selected_person = np.random.choice(other_household_members)
                    result_array[selected_person['id'], timestamp] = 1

                # Generate regular visitation
                if np.random.rand() < regular_visitation_frequency:
                    selected_person = np.random.choice(household_members)
                    result_array[selected_person, timestamp] = 1

                # Generate school children movement
                if np.random.rand() < school_children_frequency and 'school' in household_info[person_id]['roles']:
                    result_array[person_id, timestamp] = 1

    return result_array

# Load the JSON data from the file
with open('result_poi.json', 'r') as file:
    data = json.load(file)

with open('simul_settings.yaml', mode="r") as settingstream:
    settings = yaml.full_load(settingstream)

# Load the availability matrix
availability_matrix = np.genfromtxt('result_matrix.csv', delimiter=',', skip_header=1)

# Sample household_info format, adjust based on your data structure
household_info = [
    {'id': 0, 'household_id': 0, 'roles': ['school']},
    {'id': 1, 'household_id': 0, 'roles': []},
    {'id': 2, 'household_id': 1, 'roles': []},
    # ... more entries
]

result = generate_intra_household_visits(
    availability_matrix, household_info,
    individual_movement_frequency=0.2,
    social_event_frequency=0.1,
    regular_visitation_frequency=0.15,
    school_children_frequency=0.3
)

with open(csv_file_path_intra_household, 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)

    # Write header
    header = ['Person ID'] + [f'Timestamp {ts}' for ts in range(result.shape[1])]
    writer.writerow(header)

    # Write data
    for i in range(result.shape[0]):
        row = [i] + list(result[i, :])
        writer.writerow(row)

print(f"CSV file created for intra-household visits: {csv_file_path_intra_household}")
