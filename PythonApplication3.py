import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import sqlite3
import os

# Function to connect to the database
def connect_db():
    conn = sqlite3.connect('attendance.db')
    return conn

# Function to create the attendance table
def create_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS attendance (
            student_name TEXT,
            date TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Function to mark attendance in the database
def mark_attendance():
    student_name = entry_name.get()
    if not student_name:
        messagebox.showwarning("Input Error", "Please enter a student's name.")
        return
    
    conn = connect_db()
    cursor = conn.cursor()
    date = datetime.now().strftime('%Y-%m-%d')

    cursor.execute("INSERT INTO attendance (student_name, date) VALUES (?, ?)", (student_name, date))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", f"Attendance marked for {student_name} on {date}.")

# Function to view attendance
def view_attendance():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT student_name, date FROM attendance")
    records = cursor.fetchall()
    conn.close()

    if not records:
        messagebox.showinfo("Attendance Records", "No attendance records found.")
        return
    
    attendance_records = "\n".join([f"{student}: {date}" for student, date in records])
    messagebox.showinfo("Attendance Records", attendance_records)

# Function to view attendance by date range
def view_attendance_by_date():
    start_date = entry_start_date.get()
    end_date = entry_end_date.get()

    try:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
    except ValueError:
        messagebox.showerror("Invalid Date", "Please enter valid dates in YYYY-MM-DD format.")
        return

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT student_name, date FROM attendance")
    records = cursor.fetchall()
    conn.close()

    filtered_records = [
        f"{student}: {date}" for student, date in records
        if start_date <= datetime.strptime(date, '%Y-%m-%d') <= end_date
    ]

    if filtered_records:
        messagebox.showinfo("Attendance Records", "\n".join(filtered_records))
    else:
        messagebox.showinfo("Attendance Records", "No records found for the given date range.")

# Create main application window
app = tk.Tk()
app.title("Student Attendance System")

# Create input fields and buttons
tk.Label(app, text="Student Name:").pack(pady=5)
entry_name = tk.Entry(app)
entry_name.pack(pady=5)

tk.Button(app, text="Mark Attendance", command=mark_attendance).pack(pady=10)

tk.Button(app, text="View Attendance", command=view_attendance).pack(pady=10)

tk.Label(app, text="Start Date (YYYY-MM-DD):").pack(pady=5)
entry_start_date = tk.Entry(app)
entry_start_date.pack(pady=5)

tk.Label(app, text="End Date (YYYY-MM-DD):").pack(pady=5)
entry_end_date = tk.Entry(app)
entry_end_date.pack(pady=5)

tk.Button(app, text="View Attendance by Date Range", command=view_attendance_by_date).pack(pady=10)

# Call create_table() when starting the app
create_table()

# Run the application
app.mainloop()
