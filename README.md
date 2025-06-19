# FaceRecon 0.1

Built this back when I was in school, messing around with face recognition, Python GUIs, and databases.
It’s a local desktop app that recognizes faces from images, pulls info from a MySQL database, and also fetches information on the recognized person from Wikipedia.  
Not polished, not maintained, but yeah — it works.

## 🚀 Features

- GUI interface for inserting new faces into the database
- Face recognition via file upload
- Database search for stored descriptions
- Wikipedia integration for face-related context
- Simple local database setup with MySQL

## 🛠️ Tech Stack

- Python
- Tkinter
- face_recognition
- MySQL (local)
- Pillow
- wikipedia-api

## 🧩 Database Setup (Required)

This project requires a local MySQL database to store and fetch face records.

### 📂 Database Name:
`facerecognition`

### 🗂️ Table Name:
`faces`

### 🧱 Table Structure:

| Column Name | Type        | Description                         |
|-------------|-------------|-------------------------------------|
| name        | VARCHAR(255)| Name of the person                  |
| path        | VARCHAR(500)| File path to the person's image     |
| info        | TEXT        | (Optional) Description or context   |

### 📜 SQL to Create the Table:

```sql
CREATE DATABASE facerecognition;

USE facerecognition;

CREATE TABLE faces (
    name VARCHAR(255),
    path VARCHAR(500),
    info TEXT
);

```
## 📦 Requirements
```
pip install -r requirements.txt
