import tkinter as tk
from tkinter import ttk
from lanista_fetch import LanistaScraper
from convert_to_csv import json_to_csv
import json

class LanistaDataFetcher:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Lanista Data Fetcher")
        self.create_widgets()

    def create_widgets(self):
        self.email_label = ttk.Label(self.root, text="Email:")
        self.email_label.grid(row=0, column=0, padx=10, pady=10)
        self.email_entry = ttk.Entry(self.root)
        self.email_entry.grid(row=0, column=1, padx=10, pady=10)

        self.password_label = ttk.Label(self.root, text="Password:")
        self.password_label.grid(row=1, column=0, padx=10, pady=10)
        self.password_entry = ttk.Entry(self.root, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=10)

        self.fetch_data_button = ttk.Button(self.root, text="Fetch Data", command=self.fetch_data)
        self.fetch_data_button.grid(row=2, columnspan=2, padx=10, pady=10)

        self.export_csv_button = ttk.Button(self.root, text="Export to CSV", command=self.export_to_csv, state=tk.DISABLED)
        self.export_csv_button.grid(row=3, columnspan=2, padx=10, pady=10)

        self.status_text = tk.Text(self.root, height=5, width=40)
        self.status_text.grid(row=4, columnspan=2, padx=10, pady=10)


    def append_status(self, msg):
        self.status_text.config(state=tk.NORMAL)
        self.status_text.insert(tk.END, f"{msg}\n")
        self.status_text.config(state=tk.DISABLED)
        self.status_text.see(tk.END)

    def fetch_data(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        scraper = LanistaScraper()
        api_url = "https://beta.lanista.se/api/avatars/3255/levelhistory"
        scraper.login(email, password)

        data = scraper.fetch_data(api_url)
        if data != None:
            with open("Lanista_leveling_data.json", "w") as f:
                json.dump(data, f)
            self.append_status("Data fetched and saved as JSON.")
            self.export_csv_button['state'] = tk.NORMAL
        else:
            self.append_status("Login failed.")


    def export_to_csv(self):
        try:
            with open("Lanista_leveling_data.json", "r") as f:
                json_data = json.load(f)
            json_to_csv(json_data, "Lanista_leveling_data.csv")
            self.append_status("Data exported to CSV.")
        except FileNotFoundError:
            self.append_status("No data found. Fetch data first.")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = LanistaDataFetcher()
    app.run()
