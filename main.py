from tkinter import *
from tkinter import messagebox, filedialog
import random
import pyperclip
import json
import os, sys

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    password_entry.delete(0, END)
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password = random.sample(letters, k=random.randint(6, 10)) + \
               random.sample(numbers, k=random.randint(2, 5)) + \
               random.sample(symbols, k=random.randint(2, 4))

    random.shuffle(password)
    generated_password = "".join(password)
    password_entry.insert(0, generated_password)
    pyperclip.copy(password_entry.get())


# ---------------------------- FUNCTIONS FOR STORAGE PATH AND LOGO ------------------------------- #
def get_storage_path():
    if os.path.exists("config.json"):
        with open("config.json", "r", encoding="utf-8") as file:
            config = json.load(file)
        return config["storage_path"]
    else:
        selected_folder = filedialog.askdirectory(title="Select folder to store passwords.json")
        if selected_folder:
            config_data = {"storage_path": selected_folder}
            with open("config.json", "w", encoding="utf-8") as file:
                json.dump(config_data, file, indent=4)
            return selected_folder
        else:
            messagebox.showwarning(title="No Folder Selected", message="You must select a folder to continue")
            exit()


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_password():
    website = website_entry.get()
    email = email_username_entry.get()
    password = password_entry.get()
    new_password = {
        website: {
            "email": email,
            "password": password
        }
    }

    if website == "":
        messagebox.showwarning(title="Invalid Input", message="Website field cannot be empty!")
        return
    if password == "":
        messagebox.showwarning(title="Invalid Input", message="Password field cannot be empty!")
        return
    if len(password) < 4:
        messagebox.showwarning(title="Invalid Input", message="Password cannot be less than 4 character!")
        return

    is_ok = messagebox.askokcancel(title=website, message=f"These are the details entered:"
                                                  f" \n\nEmail: {email}\nPassword: {password} \n\nIs it ok to save?")
    if is_ok:
        file_path = os.path.join(storage_path, "passwords.json")
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
        except FileNotFoundError:
            response = messagebox.askyesno(
                    title="File not found",
                    message="Password file not found. Do you want to create a new one?"
                )
            if response:
                with open(file_path, "w", encoding="utf-8") as file:
                    json.dump(new_password, file, indent=4)
            else:
                return

        else:
            data.update(new_password)
            with open(file_path, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)
            website_entry.focus()
        messagebox.showinfo(title="Success", message="Password saved successfully!")


# --------------------------- SEARCH PASSWORD ------------------------------ #
def search_password():
    website = website_entry.get()
    file_path = os.path.join(storage_path, "passwords.json")

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        response = messagebox.askyesno(
            title="File not found",
            message="Password file not found. Do you want to create a new one?"
        )
        if response:
            with open(file_path, "w", encoding="utf-8") as file:
                json.dump({}, file, indent=4)
            messagebox.showinfo(title="Created", message="New password file created. Currently no data.")
        else:
            return
    else:
        if website in data:
            current_email = data[website]["email"]
            current_password = data[website]["password"]

            # Mini popup aç
            popup = Toplevel()
            popup.title(f"{website} - Update")
            popup.config(padx=20, pady=20, bg="#F0F7FA")
            popup.resizable(False, False)

            Label(popup, text="Email:", bg="#F0F7FA").grid(row=0, column=0, sticky="w")
            email_entry = Entry(popup, width=40)
            email_entry.insert(0, current_email)
            email_entry.grid(row=0, column=1, pady=5)

            Label(popup, text="Password:", bg="#F0F7FA").grid(row=1, column=0, sticky="w")
            password_entry_popup = Entry(popup, width=30)
            password_entry_popup.insert(0, current_password)
            password_entry_popup.grid(row=1, column=1, pady=5)

            def save_update():
                new_email = email_entry.get()
                new_password = password_entry_popup.get()

                if not new_email or not new_password:
                    messagebox.showwarning("Invalid Input", "Fields cannot be empty.")
                    return

                data[website] = {
                    "email": new_email,
                    "password": new_password
                }

                with open(file_path, "w", encoding="utf-8") as file:
                    json.dump(data, file, indent=4)

                messagebox.showinfo("Success", "Password updated successfully.")
                popup.destroy()

            Button(popup, text="Update", bg="#129990", fg="white", command=save_update).grid(row=2, column=1, pady=10)

        else:
            messagebox.showwarning(title="Not Found", message=f"No details found for {website}.")


# ---------------------------- SHOW/HIDE PASSWORD ------------------------------- #
def show_hide_password():
    if show_password_var.get():
        password_entry.config(show="*")
    else:
        password_entry.config(show="")


# Calling Storage Path function before TK class
storage_path = get_storage_path()


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Ergin's Password Manager")
window.resizable(False, False)
window.config(padx=50, pady=50, bg="#9AD1D4")

image = PhotoImage(file=resource_path("logo.png"))
canvas = Canvas(width=200, height=200, bg="#9AD1D4", highlightthickness=0)
canvas.create_image(100, 100, image=image)
canvas.grid(row=0, column=1)


# Labels
website_label = Label(text="Website:", bg="#5C9EAD", font=("Arial", 10), width=13)
website_label.grid(row=1, column=0)

email_username_label = Label(text="Email/Username:", bg="#5C9EAD", font=("Arial", 10), width=13)
email_username_label.grid(row=2, column=0)

password_label = Label(text="Password:", bg="#5C9EAD", font=("Arial", 10), width=13)
password_label.grid(row=3, column=0)


# Entries
website_entry = Entry(width=39, bg="#FFFBDE")
website_entry.focus()
website_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

email_username_entry = Entry(width=58, bg="#FFFBDE")
email_username_entry.grid(row=2, column=1, columnspan=2)

password_entry = Entry(width=35, bg="#FFFBDE")
password_entry.grid(row=3, column=1, padx=5, pady=5, sticky="w")

# Checkbox to show/hide password
show_password_var = BooleanVar()
show_password_check = Checkbutton(text="Show", variable=show_password_var, command=show_hide_password, bg="#129990")
show_password_check.grid(row=3, column=1, sticky="e")


# Buttons
search_button = Button(text="Search", width=14 ,command=search_password, bg="#129990")
search_button.grid(row=1, column=2, columnspan=2)

generate_password_button = Button(text="Generate Password", command=generate_password, bg="#129990")
generate_password_button.grid(row=3, column=2, sticky="w", padx=2)

add_button = Button(text="Add", width=50, command=save_password, bg="#096B68", relief="raised")
add_button.grid(row=4, column=1, columnspan=2)


window.mainloop()
