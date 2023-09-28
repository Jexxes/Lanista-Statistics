import tkinter as tk
from tkinter import ttk
from tkinter.font import Font
from lanista_fetch import LanistaScraper
from convert_to_csv import json_to_csv
import json

# Author Maximilian Ygdell (2023-09-29)

# The code found here should probably be refactored and more properly divided into a GUI part
# and a part for data handling. For now, it will have to do. 

class LanistaDataFetcher:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Lanista - Gladiatorinformation")
        self.create_widgets()
        self.fetched_data = None
        self.gladiator_info = None


    # Setup GUI elements
    def create_widgets(self):
        self.email_label = ttk.Label(self.root, text="Email:")
        self.email_label.grid(row=0, column=0, padx=2, pady=10)
        self.email_entry = ttk.Entry(self.root)
        self.email_entry.grid(row=0, column=1, padx=2, pady=10)

        self.password_label = ttk.Label(self.root, text="Lösenord:")
        self.password_label.grid(row=1, column=0, padx=2, pady=10)
        self.password_entry = ttk.Entry(self.root, show="*")
        self.password_entry.grid(row=1, column=1, padx=2, pady=10)

        self.gladiator_frame = ttk.Frame(self.root)
        self.gladiator_frame.grid(row=6, columnspan=3, padx=10, pady=10)

        self.gladiator_stats_label = ttk.Label(self.gladiator_frame, text="Basinfo Gladiator:")
        self.gladiator_stats_label.grid(row=0, column=1, padx=2, pady=2)

        self.gladiator_name_label = ttk.Label(self.gladiator_frame, text="Namn:")
        self.gladiator_name_label.grid(row=1, column=0, padx=2, pady=2)
        self.gladiator_name_value = ttk.Label(self.gladiator_frame, text="")
        self.gladiator_name_value.grid(row=1, column=2, padx=2, pady=2)

        self.gladiator_level_label = ttk.Label(self.gladiator_frame, text="Grad:")
        self.gladiator_level_label.grid(row=2, column=0, padx=2, pady=2)
        self.gladiator_level_value = ttk.Label(self.gladiator_frame, text="")
        self.gladiator_level_value.grid(row=2, column=2, padx=2, pady=2)

        self.gladiator_race_label = ttk.Label(self.gladiator_frame, text="Ras:")
        self.gladiator_race_label.grid(row=3, column=0, padx=2, pady=2)
        self.gladiator_race_value = ttk.Label(self.gladiator_frame, text="")
        self.gladiator_race_value.grid(row=3, column=2, padx=2, pady=2)

        self.fetch_data_button = ttk.Button(self.root, text="Hämta Gradinfo", command=self.fetch_data)
        self.fetch_data_button.grid(row=3, columnspan=2, padx=10, pady=10)

        self.export_csv_button = ttk.Button(self.root, text="Exportera till CSV", command=self.export_to_csv, state=tk.DISABLED)
        self.export_csv_button.grid(row=4, columnspan=2, padx=10, pady=10)

        self.status_text = tk.Text(self.root, height=5, width=40)
        self.status_text.grid(row=5, columnspan=2, padx=10, pady=10)



    def append_status(self, msg):
        self.status_text.config(state=tk.NORMAL)
        self.status_text.insert(tk.END, f"{msg}\n")
        self.status_text.config(state=tk.DISABLED)
        self.status_text.see(tk.END)

    # Gathers basic information of Gladiator
    def extract_gladiator_details(self, gladiator_info):

        avatar = gladiator_info.get('avatar', {})
        name = avatar.get('name', 'N/A')
        current_level = avatar.get('current_level', 'N/A')
        race = avatar.get('race', {}).get('name_display', 'N/A')
        return {'name': name, 'current_level': current_level, 'race': race}
    

    # Logs in and gathers data
    def fetch_data(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        scraper = LanistaScraper()
        api_url = "https://beta.lanista.se/api/avatars/3255/levelhistory"
        scraper.login(email, password)
        self.fetched_data = scraper.fetch_data(api_url)

        if self.fetched_data is not None:
            self.append_status("Data inhämtad")
            self.export_csv_button['state'] = tk.NORMAL
            self.gladiator_info = scraper.get_gladiator_info()
            avatar_details = self.extract_gladiator_details(self.gladiator_info)

            if avatar_details:
                self.gladiator_name_value['text'] = avatar_details['name']
                self.gladiator_level_value['text'] = avatar_details['current_level']
                self.gladiator_race_value['text'] = avatar_details['race'].replace('|', ', ').capitalize()
            else:
                self.append_status("Ingen gladiatorinfo hittad! ")
        else:
            self.append_status("Felaktig e-post eller lösenord!")

    def export_to_csv(self):
        if self.fetched_data:
            json_to_csv(self.fetched_data, "Lanista_leveling_data.csv")
            self.append_status("Exporterat till CSV!")
        else:
            self.append_status("Ingen gradinfo funnen, hämta data igen.")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = LanistaDataFetcher()
    app.run()
