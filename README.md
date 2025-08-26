# Canvas Assignment Manager

A **Flask-based web application** for managing and organizing Canvas assignments using the Canvas API. Includes a notification system and the ability to save assignment-specific URLs.

---

## Features

### Assignment Website

* **View all Canvas assignments** in a clean, searchable table.
* **Click on an assignment** to view its details.
* **Add and save URLs** related to each assignment.
* **Open all URLs** associated with an assignment in your browser.
* **Persistent storage** of assignment URLs in a local JSON file.

### Notification System

* **Background notifications** for assignments due soon.
* Configurable to run automatically on system startup.
* Customizable notification messages for each assignment setup.
* Customizable notification settings to filter assignments.

---

## Installation

1. **Clone the repository:**

```bash
git clone https://github.com/GitDanielR/canvas-assignment-manager.git
cd canvas-assignment-manager
```

2. **Create your environment file:**

Create .env file in the following format.
```
CANVAS_ACCESS_TOKEN=YOUR_TOKEN
```

4. **Install dependencies:**

```bash
pip install -r requirements.txt
```

> Required packages include `Flask` and desktop notification library.

---

## Running the Application

### Website Mode

```bash
python website_main.py
```

* Opens a browser window at `http://127.0.0.1:5000/`.
* Displays all assignments in a table.
* Click an assignment to view details and manage URLs.

### Notification Mode

```bash
python notifications_main.py
```

* Sends desktop notifications for upcoming assignment deadlines. Clicking notifications opens assignment's related URLs.

---

## Recommend Setup

To make running the application easier without requiring Python, you can bundle the main files into standalone executables using **PyInstaller**.

```bash
pip install pyinstaller
```

### Website Executable

Build the website executable:

```bash
python -m PyInstaller --icon="canvas.ico" --add-data=".env;.env" --add-data="templates;templates" --add-data="static;static" --add-data="canvas.ico;canvas.ico" --onefile --clean --noconsole --name="CanvasAssignmentsWebsite" .\website.py
```

### Notification Executable

Build the notifications executable:

```bash
python -m PyInstaller --icon="canvas.ico" --add-data=".env;.env" --add-data "canvas.ico;canvas.ico" --onefile --clean --noconsole --name="CanvasNotifications" .\notifications.py
```

### Launching

Locate the executables in the /dist folder. Run those executables to start your programs. For automatic notifications on system startup, add a shortcut for `CanvasNotifications.exe` to your startup programs or Task Scheduler.

## Usage

### Assignment Website

1. **View assignments:** The homepage shows all current assignments from Canvas.
2. **Open assignment details:** Click a row to see assignment description and manage URLs.
3. **Add URLs/files:** Use the input box to add files/links related to the assignment.
4. **Save URLs/files:** Click “Save” to persist the files/URLs to the local JSON file.
5. **Open all related:** Use the “Open All” feature to open every saved URL/file in your browser.

### Notification System

* Can be configured to launch automatically on system start for reminders and easy access to assignments.

---

## Notes

* **Local JSON storage:** All assignment-specific URLs are stored locally. This allows persistence across sessions but is machine-specific.
* **Browser behavior:** Opening URLs uses Python’s `webbrowser` module. Default browser may depend on system configuration.

---

## License

MIT License © Daniel Reyes
