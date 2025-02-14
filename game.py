import tkinter as tk
from tkinter import messagebox

class Participant:
    def __init__(self, name, contact):
        self.name = name
        self.contact = contact

    def __str__(self):
        return f"{self.name} - {self.contact}"

class SportsManagementSystem:
    def __init__(self, root):
        self.sports = {
            "Kabaddi": [],
            "Cricket": [],
            "Volleyball": [],
            "Basketball": [],
            "Badminton": [],
        }
        self.root = root
        self.root.title("Sports Management System")

        # Dropdown for sports selection
        self.sport_label = tk.Label(root, text="Select Sport:")
        self.sport_label.grid(row=0, column=0, padx=10, pady=5)
        
        self.sport_var = tk.StringVar()
        self.sport_var.set("Kabaddi")
        self.sport_menu = tk.OptionMenu(root, self.sport_var, *self.sports.keys())
        self.sport_menu.grid(row=0, column=1, padx=10, pady=5)

        # Entry fields for participant name & contact
        self.name_label = tk.Label(root, text="Name:")
        self.name_label.grid(row=1, column=0, padx=10, pady=5)
        self.name_entry = tk.Entry(root)
        self.name_entry.grid(row=1, column=1, padx=10, pady=5)

        self.contact_label = tk.Label(root, text="Contact:")
        self.contact_label.grid(row=2, column=0, padx=10, pady=5)
        self.contact_entry = tk.Entry(root)
        self.contact_entry.grid(row=2, column=1, padx=10, pady=5)

        # Buttons for Add, View, Delete
        self.add_button = tk.Button(root, text="Add Participant", command=self.add_participant)
        self.add_button.grid(row=3, column=0, columnspan=2, pady=5)

        self.view_button = tk.Button(root, text="View Participants", command=self.view_participants)
        self.view_button.grid(row=4, column=0, columnspan=2, pady=5)

        self.delete_button = tk.Button(root, text="Delete Participant", command=self.delete_participant)
        self.delete_button.grid(row=5, column=0, columnspan=2, pady=5)

        # Listbox to display participants
        self.listbox = tk.Listbox(root, width=50)
        self.listbox.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

    def add_participant(self):
        sport = self.sport_var.get()
        name = self.name_entry.get().strip()
        contact = self.contact_entry.get().strip()

        if name and contact:
            participant = Participant(name, contact)
            self.sports[sport].append(participant)
            messagebox.showinfo("Success", f"Added {name} to {sport}")
            self.view_participants()
        else:
            messagebox.showwarning("Input Error", "Please enter name and contact.")

    def view_participants(self):
        sport = self.sport_var.get()
        self.listbox.delete(0, tk.END)  # Clear the listbox
        participants = self.sports[sport]

        if participants:
            for participant in participants:
                self.listbox.insert(tk.END, str(participant))
        else:
            self.listbox.insert(tk.END, "No participants registered.")

    def delete_participant(self):
        sport = self.sport_var.get()
        selected_index = self.listbox.curselection()

        if selected_index:
            participant = self.sports[sport].pop(selected_index[0])
            messagebox.showinfo("Deleted", f"Removed {participant.name} from {sport}")
            self.view_participants()
        else:
            messagebox.showwarning("Selection Error", "Please select a participant to delete.")

if __name__ == "__main__":
    root = tk.Tk()
    app = SportsManagementSystem(root)
    root.mainloop()
