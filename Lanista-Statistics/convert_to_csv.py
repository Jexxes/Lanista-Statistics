import csv
import json

# Column mapping dictionary for renaming
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

    def generate_header(self):
        header = ['level', 'stats_changed']  # Removed unnecessary columns
        first_entry = self.json_data[0]
        stats_names = [stat['name'] for stat in first_entry['stats']['stats']]
        weapon_skills_names = [skill['name'] for skill in first_entry['stats']['weapon_skills']]
        header.extend(stats_names)
        header.extend(weapon_skills_names)

        # Translate header to Swedish
        header = [COLUMN_MAPPING.get(col, col) for col in header]
        self.csv_data.append(header)

    def extract_and_compare_stats(self, entry, stats_names, weapon_skills_names):
        stats_values = {stat['name']: stat['value'] for stat in entry['stats']['stats']}
        weapon_skills_values = {skill['name']: skill['value'] for skill in entry['stats']['weapon_skills']}
        changed_stats = []

        self.stat_changes(changed_stats, stats_names, stats_values)

        self.weapon_skill_changes(changed_stats, weapon_skills_names, weapon_skills_values)

        self.prev_stats_values = stats_values
        self.prev_weapon_skills_values = weapon_skills_values

        return ", ".join(changed_stats) if changed_stats else 'N/A', stats_values, weapon_skills_values

    def weapon_skill_changes(self, changed_stats, weapon_skills_names, weapon_skills_values):
        for name in weapon_skills_names:
            if name in self.prev_weapon_skills_values:
                change = weapon_skills_values.get(name, 0) - self.prev_weapon_skills_values[name]
                if change != 0:
                    # Translate name to Swedish
                    translated_name = COLUMN_MAPPING.get(name, name)
                    changed_stats.append(f"{translated_name} ({change})")

    def stat_changes(self, changed_stats, stats_names, stats_values):
        for name in stats_names:
            if name in self.prev_stats_values:
                change = stats_values.get(name, 0) - self.prev_stats_values[name]
                if change != 0:
                    translated_name = COLUMN_MAPPING.get(name, name)
                    changed_stats.append(f"{translated_name} ({change})")

    def convert(self, csv_file_path):
        for entry in self.json_data:
            row = [entry['level']]
            stats_names = [stat['name'] for stat in entry['stats']['stats']]
            weapon_skills_names = [skill['name'] for skill in entry['stats']['weapon_skills']]
            changed_stats, stats_values, weapon_skills_values = self.extract_and_compare_stats(entry, stats_names,
                                                                                               weapon_skills_names)
            row.append(changed_stats)
            row.extend([stats_values.get(name, 'N/A') for name in stats_names])
            row.extend([weapon_skills_values.get(name, 'N/A') for name in weapon_skills_names])
            self.csv_data.append(row)

        with open(csv_file_path, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerows(self.csv_data)

def json_to_csv(json_data, csv_file_path):
    converter = JsonToCsvConverter(json_data)
    converter.convert(csv_file_path)

