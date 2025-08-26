# Canvas Assignment Manager

A **Flask-based web application** for managing and organizing Canvas assignments using the Canvas API. Includes a notification system and the ability to save assignment-specific files/URLs. Saved files/URLs can be opened all-at-once using the website or by clicking the notification.

---

## Features

### Assignment Website

* **View all Canvas assignments** in a clean table.
* **Filter assignments** by upcoming, overdue, class-specific and more.
* **Click on an assignment** to view its details.
* **Add and save files/URLs** related to each assignment.
* **Open all files/URLs** associated with an assignment in your browser.
* **Persistent storage** of assignment files/URLs in a local JSON file.
* **Shutdown** website after use with the shutdown button shown below so the python process behind the webpage stops.

#### 📸 Screenshots

<p align="center">
  <img src="https://github.com/user-attachments/assets/17e62f19-30cf-4d74-b7a4-9d8cdbcae7d4" alt="Home Page" width="80%"><br>
  <em>Assignment list.</em>
</p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/c49d51e3-7d2e-4697-8bbc-8f920cb9512e" alt="Assignment Page" width="80%"><br>
  <em>Assignment view. Includes saved links/files and inputs to add new links/files.</em>
</p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/30c8da9d-db81-4b0b-939c-65d88a7de5d6" alt="Course/assignment settings" width="80%"><br>
  <em>Settings that filter courses/assignments displayed and shown in notifications.</em>
</p>

<p align="center">
  <img alt="Notification/general settings" src="https://github.com/user-attachments/assets/56e220ab-16d0-4dd4-ad7f-b5a684b1df93" width="80%"><br>
  <em>Notification settings that impact the visual display of notifications. Also shows canvas domain configuration and date format setting.</em>
</p>

### Notification System

* **Background notifications** for assignments due soon.
* Configurable to run automatically on system startup.
* Customizable notification messages for each assignment setup.
* User-configured assignment filtering (from web settings).
* User-configured notification settings (from web settings).

#### 📸 Screenshots

<p align="center">
  <img alt="Notification" src="https://github.com/user-attachments/assets/0d75419d-d99c-4871-9520-bbf3adc4273b" width="80%"><br>
  <em>Notification for upcoming assignment.</em>
</p>

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

> Required packages include `Flask` and operating system specific notification systems.

---

## Running the Application

### Website Mode

```bash
python website_main.py
```

* Opens a browser window at `http://127.0.0.1:5000/`.
* Displays all assignments in a table.
* Click an assignment to view details and manage files/URLs.

### Notification Mode

```bash
python notifications_main.py
```

* Sends desktop notifications for upcoming assignment deadlines. Clicking notifications opens assignment's related files/URLs.

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
