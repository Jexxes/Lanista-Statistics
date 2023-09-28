import csv
import json

# Author Maximilian Ygdell (2023-09-29)

# This code is a bit messy at the moment. Late night work.
# I may refactor it at a later point, but it should at least work
# for the basic cases

# Words to translate from English to Swedish
COLUMN_MAPPING = {
    'level': 'Grad',
    'stats_changed': 'Utsatta poäng',
    'STAMINA': 'Bashälsa',
    'STRENGTH': 'Styrka',
    'WISDOM': 'Intellekt',
    'ENDURANCE': 'Uthållighet',
    'INITIATIVE': 'Initiativ',
    'LEARNING_CAPACITY': 'Inlärningsförmåga',
    'DODGE': 'Undvika anfall',
    'LUCK': 'Tur',
    'DISCIPLINE': 'Disciplin',
    'LEADERSHIP': 'Ledarskap',
    'AXE': 'Yxa',
    'SWORD': 'Svärd',
    'MACE': 'Hammare',
    'STAVE': 'Stav',
    'SHIELD': 'Sköld',
    'SPEAR': 'Stickvapen',
    'CHAIN': 'Kättingvapen',
    'FIST_WEAPON': 'Obeväpnat'
}

class JsonToCsvConverter:
    def __init__(self, json_data):
        self.json_data = sorted(json_data, key=lambda x: x['level'])
        self.csv_data = []
        self.prev_stats_values = {}
        self.prev_weapon_skills_values = {}
        self.generate_header()

    # Get headers from json response and translates it to Swedish
    def generate_header(self):
        first_entry = self.json_data[0]
        stats_names = [stat['name'] for stat in first_entry['stats']['stats']]
        weapon_skills_names = [skill['name'] for skill in first_entry['stats']['weapon_skills']]
        header = ['level', 'stats_changed'] + stats_names + weapon_skills_names
        self.csv_data.append([COLUMN_MAPPING.get(col, col) for col in header])

     # Checks what stats are changed from previous levels
    def extract_and_compare(self, entry, names, prev_values, category):
        current_values = {item['name']: item['value'] for item in entry['stats'][category]}
        changed = []
        for name in names:
            if name in prev_values:
                change = current_values.get(name, 0) - prev_values[name]
                if change != 0:
                    translated_name = COLUMN_MAPPING.get(name, name)
                    changed.append(f"{translated_name} ({change})")
        prev_values.update(current_values)
        return ", ".join(changed) if changed else 'N/A', current_values

    
    def write_to_file(self, csv_file_path):
        with open(csv_file_path, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerows(self.csv_data)

    def convert(self, csv_file_path):
        for entry in self.json_data:
            stats_names = [stat['name'] for stat in entry['stats']['stats']]
            weapon_skills_names = [skill['name'] for skill in entry['stats']['weapon_skills']]
            
            row = [entry['level']]
            changed_stats, _ = self.extract_and_compare(entry, stats_names, self.prev_stats_values, 'stats')
            changed_skills, _ = self.extract_and_compare(entry, weapon_skills_names, self.prev_weapon_skills_values, 'weapon_skills')
            
            all_changes = changed_stats + "; " + changed_skills if changed_stats and changed_skills else changed_stats or changed_skills
            row.append(all_changes)

            row.extend([self.prev_stats_values.get(name, 'N/A') for name in stats_names])
            row.extend([self.prev_weapon_skills_values.get(name, 'N/A') for name in weapon_skills_names])
            
            self.csv_data.append(row)
        
        self.write_to_file(csv_file_path)

def json_to_csv(json_data, csv_file_path):
    converter = JsonToCsvConverter(json_data)
    converter.convert(csv_file_path)


