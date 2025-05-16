# 🔐 Ergin's Password Manager

A user-friendly password manager built with Python and Tkinter. It securely stores credentials in JSON format and allows you to manage them easily via a clean graphical interface.

---

## 🚀 Features

- ✅ Generate strong random passwords
- ✅ Automatically copy passwords to clipboard
- ✅ Save credentials in structured JSON format
- ✅ Search and retrieve saved credentials
- ✅ User-selected storage directory via GUI (configurable)
- ✅ Show/Hide password toggle for better UX
- ✅ Asks user confirmation before overwriting or creating files
- ✅ Clean and intuitive Tkinter GUI

---

## 🛠️ Built With

- Python 3.x
- Tkinter
- JSON
- pyperclip
- os / filedialog modules

---

## 💾 How to Use

1. Clone this repository:
```bash
git clone https://github.com/erginsa/password-manager.git
```

2. Install the required library:
```bash
pip install pyperclip
```

3. Run the application:
```bash
python main.py
```

---

## 📦 Packaging as .EXE
To build an executable version:

```bash
pyinstaller --noconfirm --onefile --windowed --icon=logo.ico main.py
```
Make sure to include logo.png and .spec file configurations if needed.


---

## 📁 File Structure

```text
project/
├── main.py
├── config.json        # Stores selected directory path
├── passwords.json     # Saved in the user-selected directory
├── logo.png
├── README.md
└── requirements.txt   # Optional

```

---

## 🧠 Notes
- Passwords are stored in plain text in JSON format.

- This project is a demonstration and should not be used for real-world secure password storage without encryption.

- You can add AES encryption or hashing for enhanced security in future versions.

---

## 📌 Additional Notes Before Packaging

### Should I clear config.json before building .exe?
 Yes — it is recommended to clear or delete config.json before creating the .exe version.

#### Why?

config.json contains your personal file path

Other users won’t have this path, so the app may not function properly if it’s not reset

The app automatically prompts for a new folder if config.json is missing or empty


#### What to do?

Either delete config.json completely
or

Replace its contents with:
```json
{}
```






---

## 👨‍💻 Author
Ergin SABANCI

Istanbul, Turkey

GitHub: @erginsa
