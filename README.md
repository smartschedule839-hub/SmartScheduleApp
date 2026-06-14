# SmartScheduleApp
SmartScheduleApp

# Smart Schedule Application

## Overview

Smart Schedule is a mobile-style scheduling and productivity application developed using Python and the Kivy framework. The application is designed to help students organise academic activities, monitor deadlines, manage study schedules, and track productivity through an intuitive and responsive user interface.

The application provides secure user authentication, schedule management, progress tracking, profile customisation, and local data persistence using JSON storage.

---

## Features

The application includes the following features:

* User registration and login authentication
* Password encryption using SHA-256 hashing
* Multi-screen navigation
* Create, edit, delete, and search schedule items
* Mark schedule items as complete or incomplete
* Priority selection using radio buttons (High, Medium, Low)
* Progress tracking with dashboard progress bar
* Profile picture upload
* Dark mode support
* Input validation and error handling
* Local data persistence using JSON files

---

## Framework and Tools Used

The project was developed using:

* Python 3.11
* Kivy Framework
* JSON File Storage
* Git and GitHub for Version Control
* Visual Studio Code

---

## Installation Instructions

### Step 1: Install Python

Download and install Python 3.11 from:

https://www.python.org

### Step 2: Install Kivy

Open Command Prompt and run:

```bash
pip install kivy
```

### Step 3: Download Project Files

Download or clone the repository:

```bash
git clone <repository-url>
```

Alternatively, download the ZIP file and extract it.

### Step 4: Run the Application

Navigate to the project folder and run:

```bash
python smartschedule7.py
```

The application window should launch automatically.

---

## Project Structure

```text
SmartSchedule/
│
├── smartschedule.py
├── smart_schedule_users.json
├── smart_schedule_items.json
├── README.md

```

---

## Data Storage

The application stores data locally using JSON files:

* smart_schedule_users.json – stores user account information.
* smart_schedule_items.json – stores schedule records and completion status.

No external database is required.

---

## Known Limitations

The current version has several limitations:

* Data is stored locally and is not synchronised across devices.
* Profile pictures are stored using local file paths.
* Notifications are limited to on-screen messages.
* No cloud backup functionality is currently available.

---

## Future Enhancements

Potential future improvements include:

* Firebase or cloud database integration
* Push notification reminders
* Calendar integration
* APK deployment for Android devices
* Multi-device synchronisation
* Enhanced analytics and reporting features

