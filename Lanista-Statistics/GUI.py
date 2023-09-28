import tkinter as tk
from tkinter import ttk
from lanista_fetch import LanistaScraper  # Import the LanistaScraper class
from convert_to_csv import json_to_csv  # Import the json_to_csv function
import json


def fetch_data():
    # Get email and password from the input fields
    email = email_entry.get()
    password = password_entry.get()

    # Initialize the scraper and login
    scraper = LanistaScraper()
    api_url = "https://beta.lanista.se/api/avatars/3255/levelhistory"  # Hardcoded API URL
    status_code = scraper.login(email, password)

    if status_code == 200:
        # Fetch data and save it as a JSON file
        data = scraper.fetch_data(api_url)
        with open("Lanista_leveling_data.json", "w") as f:
            json.dump(data, f)
        print("Data fetched and saved as JSON.")
        export_csv_button['state'] = tk.NORMAL  # Enable the export button
    else:
        print("Login failed.")


def export_to_csv():
    # Read the JSON file
    with open("Lanista_leveling_data.json", "r") as f:
        json_data = json.load(f)

    # Convert to CSV
    json_to_csv(json_data, "Lanista_leveling_data.csv")
    print("Data exported to CSV.")


# Create the Tkinter window
root = tk.Tk()
root.title("Lanista Data Fetcher")

# Create and place labels, entry boxes, and buttons
email_label = ttk.Label(root, text="Email:")
email_label.grid(row=0, column=0, padx=10, pady=10)
email_entry = ttk.Entry(root)
email_entry.grid(row=0, column=1, padx=10, pady=10)

password_label = ttk.Label(root, text="Password:")
password_label.grid(row=1, column=0, padx=10, pady=10)
password_entry = ttk.Entry(root, show="*")
password_entry.grid(row=1, column=1, padx=10, pady=10)

fetch_data_button = ttk.Button(root, text="Fetch Data", command=fetch_data)
fetch_data_button.grid(row=2, columnspan=2, padx=10, pady=10)

export_csv_button = ttk.Button(root, text="Export to CSV", command=export_to_csv, state=tk.DISABLED)
export_csv_button.grid(row=3, columnspan=2, padx=10, pady=10)


root.mainloop()
