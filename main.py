import csv
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

# File path for the CSV file
CSV_FILE = 'pokemon_dashboard.csv'

def load_csv(file_path):
    """Load data from the CSV file."""
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return list(reader)

def calculate_statistics(data):
    """Calculate basic and derived statistics."""
    total_entries = len(data)
    unique_games = len(set(row['Game'] for row in data))
    total_playtime = sum(int(row['Playtime'].split(':')[0]) for row in data)
    avg_playtime = total_playtime / total_entries if total_entries > 0 else 0
    avg_pokedex_caught = sum(int(row['Pokedex Caught']) for row in data) / total_entries if total_entries > 0 else 0
    return {
        'total_entries': total_entries,
        'unique_games': unique_games,
        'total_playtime': total_playtime,
        'avg_playtime': avg_playtime,
        'avg_pokedex_caught': avg_pokedex_caught
    }

def add_new_entry(file_path):
    """Add a new entry to the CSV file."""
    new_entry = {
        'Game': simpledialog.askstring("Input", "Game:"),
        'Platform': simpledialog.askstring("Input", "Platform:"),
        'Playtime': simpledialog.askstring("Input", "Playtime (hh:mm):"),
        'Battle Style': simpledialog.askstring("Input", "Battle Style:"),
        'Date': datetime.now().strftime('%m/%d/%Y'),
        'Starter': simpledialog.askstring("Input", "Starter:"),
        'Pokedex Caught': simpledialog.askstring("Input", "Pokedex Caught:"),
        'Pokedex Seen': simpledialog.askstring("Input", "Pokedex Seen:"),
        'Pokemon in Box': simpledialog.askstring("Input", "Pokemon in Box:"),
        'Money': simpledialog.askstring("Input", "Money:"),
        'Player Name': simpledialog.askstring("Input", "Player Name:"),
        'Legendaries Caught': simpledialog.askstring("Input", "Legendaries Caught:"),
        'Shinies Caught': simpledialog.askstring("Input", "Shinies Caught:"),
        'Fun Rating': simpledialog.askstring("Input", "Fun Rating:"),
        'Team Favorability': simpledialog.askstring("Input", "Team Favorability:"),
        'Notes': simpledialog.askstring("Input", "Notes:"),
    }
    with open(file_path, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=new_entry.keys())
        writer.writerow(new_entry)
    messagebox.showinfo("Success", "New entry added successfully!")

def update_statistics(summary_label, detailed_label, data):
    """Update the statistics displayed on the dashboard."""
    stats = calculate_statistics(data)
    summary_label.config(text=(
        f"Total Entries: {stats['total_entries']}\n"
        f"Unique Games: {stats['unique_games']}\n"
        f"Total Playtime: {stats['total_playtime']} hours"
    ))
    detailed_label.config(text=(
        f"Average Playtime: {stats['avg_playtime']:.2f} hours\n"
        f"Average Pokedex Caught: {stats['avg_pokedex_caught']:.2f}"
    ))

def main():
    data = load_csv(CSV_FILE)

    # Create the main window
    root = tk.Tk()
    root.title("Pokemon Dashboard")
    root.geometry("500x400")

    # Create frames for sections
    summary_frame = ttk.LabelFrame(root, text="Summary Statistics", padding=(10, 10))
    summary_frame.pack(fill="x", padx=10, pady=5)

    detailed_frame = ttk.LabelFrame(root, text="Detailed Statistics", padding=(10, 10))
    detailed_frame.pack(fill="x", padx=10, pady=5)

    actions_frame = ttk.Frame(root, padding=(10, 10))
    actions_frame.pack(fill="x", padx=10, pady=5)

    # Summary statistics label
    summary_label = ttk.Label(summary_frame, text="", justify=tk.LEFT)
    summary_label.pack(anchor="w")

    # Detailed statistics label
    detailed_label = ttk.Label(detailed_frame, text="", justify=tk.LEFT)
    detailed_label.pack(anchor="w")

    # Update statistics
    update_statistics(summary_label, detailed_label, data)

    # Add Entry button
    def on_add_entry():
        add_new_entry(CSV_FILE)
        nonlocal data
        data = load_csv(CSV_FILE)
        update_statistics(summary_label, detailed_label, data)

    add_entry_button = ttk.Button(actions_frame, text="Add New Entry", command=on_add_entry)
    add_entry_button.pack(side="left", padx=5)

    # Run the application
    root.mainloop()

if __name__ == "__main__":
    main()