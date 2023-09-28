import csv
import json


# Function to convert JSON to CSV with further enhancements
def json_to_csv(json_data, csv_file_path):
    # Sort the JSON data by 'level' in ascending order
    sorted_json_data = sorted(json_data, key=lambda x: x['level'])

    # Create a list to hold the header and data rows
    csv_data = []

    # Extract header
    header = ['id', 'level', 'paragon_level', 'created_at', 'stats_changed']

    # Dynamically find the stats and weapon_skills names for header
    first_entry = sorted_json_data[0]
    stats_names = [stat['name'] for stat in first_entry['stats']['stats']]
    weapon_skills_names = [skill['name'] for skill in first_entry['stats']['weapon_skills']]

    # Combine to create full header
    header.extend(stats_names)
    header.extend(weapon_skills_names)

    # Add header to csv_data
    csv_data.append(header)

    # Variable to hold the previous level's stats and weapon_skills for comparison
    prev_stats_values = {}
    prev_weapon_skills_values = {}

    # Loop through each level's data
    for entry in sorted_json_data:
        row = [entry['id'], entry['level'], entry['paragon_level'], entry['created_at']]

        # Extract stats and weapon_skills
        stats_values = {stat['name']: stat['value'] for stat in entry['stats']['stats']}
        weapon_skills_values = {skill['name']: skill['value'] for skill in entry['stats']['weapon_skills']}

        # Detect stats that have changed compared to the previous level and calculate the change amount
        changed_stats = []
        for name in stats_names:
            if name in prev_stats_values:
                change = stats_values.get(name, 0) - prev_stats_values[name]
                if change != 0:
                    changed_stats.append(f"{name} ({change})")
        for name in weapon_skills_names:
            if name in prev_weapon_skills_values:
                change = weapon_skills_values.get(name, 0) - prev_weapon_skills_values[name]
                if change != 0:
                    changed_stats.append(f"{name} ({change})")

        # Add the changed stats and their change amounts to the row
        row.append(", ".join(changed_stats) if changed_stats else 'N/A')

        # Fill in the stats and weapon_skills values in the same order as in header
        row.extend([stats_values.get(name, 'N/A') for name in stats_names])
        row.extend([weapon_skills_values.get(name, 'N/A') for name in weapon_skills_names])

        # Add the row to csv_data
        csv_data.append(row)

        # Update the previous level's stats and weapon_skills for the next iteration
        prev_stats_values = stats_values
        prev_weapon_skills_values = weapon_skills_values

    # Write the csv_data to a CSV file
    with open(csv_file_path, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerows(csv_data)

# # Load the JSON file into a Python object
# json_file_path = 'Lanista_leveling_data.json'
# with open(json_file_path, 'r') as f:
#     json_data = json.load(f)
#
# # Convert the JSON data to CSV
# csv_file_path = 'Lanista_leveling_data.csv'
# json_to_csv(json_data, csv_file_path)
