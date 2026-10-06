import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3


conn = sqlite3.connect("artist.db")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS artists (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER NOT NULL,
        songname TEXT NOT NULL,
        genre TEXT NOT NULL)
""")

conn.commit()


def add_artist():
    name = name_entry.get().strip()
    age = age_entry.get().strip()
    songname = songname_entry.get().strip()
    genre = genre_entry.get().strip()

    # Check if all fields are filled
    if name == "" or age == "" or songname == "" or genre == "":
        messagebox.showwarning(
            "Warning",
            "Please fill in all fields."
        )
        return

    # Check if age is a number
    try:
        age = int(age)
    except ValueError:
        messagebox.showerror(
            "Error",
            "Age must be a number."
        )
        return

    # Add artist to database
    cursor.execute(
        """
        INSERT INTO artists (name, age, songname, genre)
        VALUES (?, ?, ?, ?)
        """,
        (name, age, songname, genre)
    )

    conn.commit()

    messagebox.showinfo(
        "Success",
        "Your favorite artist has been added successfully!"
    )

    # Clear input boxes
    clear_fields()

    # Refresh the Treeview
    display_artists()




def display_artists():
    for item in tree.get_children():
        tree.delete(item)

    cursor.execute("SELECT * FROM artists")

    artists = cursor.fetchall()

    for artist in artists:
        tree.insert("", tk.END, values=artist)



def update_artist():
    selected = tree.selection()

    if not selected:
        messagebox.showwarning(
            "Warning",
            "Please select an artist to update."
        )
        return

    artist_id = tree.item(selected[0])["values"][0]

    name = name_entry.get().strip()
    age = age_entry.get().strip()
    songname = songname_entry.get().strip()
    genre = genre_entry.get().strip()

    if name == "" or age == "" or songname == "" or genre == "":
        messagebox.showwarning(
            "Warning",
            "Please fill in all fields."
        )
        return

    try:
        age = int(age)
    except ValueError:
        messagebox.showerror(
            "Error",
            "Age must be a number."
        )
        return

    cursor.execute(
        """
        UPDATE artists
        SET name = ?, age = ?, songname = ?, genre = ?
        WHERE id = ?
        """,
        (name, age, songname, genre, artist_id)
    )

    conn.commit()

    messagebox.showinfo(
        "Success",
        "Artist updated successfully."
    )

    clear_fields()
    display_artists()



def delete_artist():
    selected = tree.selection()

    if not selected:
        messagebox.showwarning(
            "Warning",
            "Please select a artist you want to delete."
        )
        return

    artist_id = tree.item(selected[0])["values"][0]

    confirm = messagebox.askyesno(
        "Confirm Delete",
        "Are you sure you want to delete this handsome/beautiful artist?"
    )

    if confirm:
        cursor.execute(
            "DELETE FROM artists WHERE id = ?",
            (artist_id,)
        )
        conn.commit()
        messagebox.showinfo(
            "Success",
            "Artist deleted successfully.\n Mabuhay!"
        )

        clear_fields()
        display_artists()


def clear_fields():
    name_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    songname_entry.delete(0, tk.END)
    genre_entry.delete(0, tk.END)




def select_artist(event):
    selected = tree.selection()

    if selected:
        artist = tree.item(selected[0])["values"]

        clear_fields()
        name_entry.insert(0, artist[1])
        age_entry.insert(0, artist[2])
        songname_entry.insert(0, artist[3])
        genre_entry.insert(0, artist[4])
        
root = tk.Tk()
root.title("Song Artist Information")
root.geometry("700x500")


title_label=tk.Label(
    root,
    text="Song Artist Information",
    font=("Times New Roman", 16, "bold", "italic")
    
)

title_label.pack(pady=10)

input_frame=tk.Frame(root)
input_frame.pack(pady=10)


tk.Label(
    input_frame,
    text="Name:"
   ).grid(row=0,column=0,padx=5,pady=5)
name_entry=tk.Entry(input_frame,width=30)
name_entry.grid(row=0,column=1,padx=5,pady=5)


tk.Label(
    input_frame,
    text="Age:"
    ).grid(row=1,column=0,padx=5,pady=5)
age_entry=tk.Entry(input_frame,width=30)
age_entry.grid(row=1,column=1,padx=5,pady=5)

tk.Label(
    input_frame,
    text="Song Name:"
    ).grid(row=2,column=0,padx=5,pady=5)
songname_entry=tk.Entry(input_frame,width=30)
songname_entry.grid(row=2,column=1,padx=5,pady=5)

tk.Label(
    input_frame,
    text="Genre:"
    ).grid(row=3,column=0,padx=5,pady=5)
genre_entry=tk.Entry(input_frame,width=30)
genre_entry.grid(row=3,column=1,padx=5,pady=5)


button_frame=tk.Frame(root)
button_frame.pack(pady=10)

tk.Button(
    button_frame,
    text="Add",
    width=10,
    command=add_artist
    ).grid(row=0,column=0,padx=5)

tk.Button(
    button_frame,
    text="Update",
    width=10,
    command=update_artist
    ).grid(row=0,column=1,padx=5)

tk.Button(
    button_frame,
    text="Delete",
    width=10,
    command=delete_artist
    ).grid(row=0,column=2 ,padx=5)
tk.Button(
    button_frame,
    text="Clear",
    width=10,
    command=clear_fields
    ).grid(row=0,column=3,padx=5)

tk.Button(
    button_frame,
    text="Exit",
    width=10,
    command=root.destroy
    ).grid(row=0,column=4,padx=5)


tree=ttk.Treeview(
    root,
    columns=("ID","Name","Age","Song name", "Genre"),
    show="headings"
    )

    
tree.heading("ID",text="ID")
tree.heading("Name",text="Name")
tree.heading("Age",text="Age")
tree.heading("Song name",text="Song name")
tree.heading("Genre",text="Genre")

    
tree.column("ID",width=50)
tree.column("Name",width=200)
tree.column("Age",width=80)
tree.column("Song name",width=200)
tree.column("Genre",width=50)

tree.pack(
    fill="both",
    expand=True,
    padx=10,
    pady=10
    )


tree.bind(
    "<<TreeviewSelect>>",
    select_artist
    )


display_artists()


root.mainloop()


conn.close()


            
