import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3


conn = sqlite3.connect("cricket_club.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS players (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    contact TEXT,
    email TEXT,
    age INTEGER,
    role TEXT,
    doj TEXT,
    team TEXT
)
""")
conn.commit()


def add_player():
    name = entry_name.get()
    contact = entry_contact.get()
    email = entry_email.get()
    age = entry_age.get()
    role = entry_role.get()
    doj = entry_doj.get()
    team = entry_team.get()
    
    if name == "" or contact == "" or email == "":
        messagebox.showerror("Error", "Please fill all required fields")
        return
    
    cursor.execute("INSERT INTO players (name, contact, email, age, role, doj, team) VALUES (?, ?, ?, ?, ?, ?, ?)",
                   (name, contact, email, age, role, doj, team))
    conn.commit()
    messagebox.showinfo("Success", "Player added successfully")
    view_players()
    reset_fields()

def delete_player():
    selected = tree.selection()
    if not selected:
        messagebox.showerror("Error", "Please select a player to delete")
        return
    player_id = tree.item(selected[0])['values'][0]
    cursor.execute("DELETE FROM players WHERE id=?", (player_id,))
    conn.commit()
    view_players()

def view_players():
    for row in tree.get_children():
        tree.delete(row)
    cursor.execute("SELECT * FROM players")
    rows = cursor.fetchall()
    for row in rows:
        tree.insert("", tk.END, values=row)

def reset_fields():
    entry_name.delete(0, tk.END)
    entry_contact.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    entry_age.delete(0, tk.END)
    entry_role.delete(0, tk.END)
    entry_doj.delete(0, tk.END)
    entry_team.delete(0, tk.END)

def delete_database():
    cursor.execute("DELETE FROM players")
    conn.commit()
    view_players()
    messagebox.showinfo("Deleted", "All records deleted")


root = tk.Tk()
root.title("Cricket Club Management System")


root.state('zoomed')   

root.config(bg="lightgreen")


title_label = tk.Label(root, text="🏏 Cricket Club Management System 🏏",
                       font=("Arial", 22, "bold"), bg="darkgreen", fg="white", pady=15)
title_label.pack(fill=tk.X)


frame_left = tk.Frame(root, bg="lightgreen")
frame_left.pack(side=tk.LEFT, padx=40, pady=20, fill=tk.Y)

tk.Label(frame_left, text="Player Name", bg="lightgreen", font=("Arial", 12, "bold")).pack(anchor="w")
entry_name = tk.Entry(frame_left, font=("Arial", 12))
entry_name.pack(fill=tk.X)

tk.Label(frame_left, text="Contact Number", bg="lightgreen", font=("Arial", 12, "bold")).pack(anchor="w")
entry_contact = tk.Entry(frame_left, font=("Arial", 12))
entry_contact.pack(fill=tk.X)

tk.Label(frame_left, text="Email Address", bg="lightgreen", font=("Arial", 12, "bold")).pack(anchor="w")
entry_email = tk.Entry(frame_left, font=("Arial", 12))
entry_email.pack(fill=tk.X)

tk.Label(frame_left, text="Age", bg="lightgreen", font=("Arial", 12, "bold")).pack(anchor="w")
entry_age = tk.Entry(frame_left, font=("Arial", 12))
entry_age.pack(fill=tk.X)

tk.Label(frame_left, text="Role (Batsman/Bowler/All-rounder/WK)", bg="lightgreen", font=("Arial", 12, "bold")).pack(anchor="w")
entry_role = tk.Entry(frame_left, font=("Arial", 12))
entry_role.pack(fill=tk.X)

tk.Label(frame_left, text="Date of Joining", bg="lightgreen", font=("Arial", 12, "bold")).pack(anchor="w")
entry_doj = tk.Entry(frame_left, font=("Arial", 12))
entry_doj.pack(fill=tk.X)

tk.Label(frame_left, text="Team", bg="lightgreen", font=("Arial", 12, "bold")).pack(anchor="w")
entry_team = tk.Entry(frame_left, font=("Arial", 12))
entry_team.pack(fill=tk.X)


tk.Button(frame_left, text="Add Player", command=add_player, bg="darkgreen", fg="white", font=("Arial", 12, "bold")).pack(pady=5, fill=tk.X)
tk.Button(frame_left, text="Delete Player", command=delete_player, bg="red", fg="white", font=("Arial", 12, "bold")).pack(pady=5, fill=tk.X)
tk.Button(frame_left, text="View Players", command=view_players, bg="blue", fg="white", font=("Arial", 12, "bold")).pack(pady=5, fill=tk.X)
tk.Button(frame_left, text="Reset Fields", command=reset_fields, bg="orange", fg="black", font=("Arial", 12, "bold")).pack(pady=5, fill=tk.X)
tk.Button(frame_left, text="Delete Database", command=delete_database, bg="black", fg="white", font=("Arial", 12, "bold")).pack(pady=5, fill=tk.X)


frame_right = tk.Frame(root, bg="white")
frame_right.pack(side=tk.RIGHT, padx=20, pady=20, expand=True, fill=tk.BOTH)

columns = ("ID", "Name", "Contact", "Email", "Age", "Role", "DOJ", "Team")
tree = ttk.Treeview(frame_right, columns=columns, show="headings")

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=150, anchor="center")

tree.pack(expand=True, fill=tk.BOTH)


view_players()

root.mainloop()
