import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import os

# Load student data
file_path = os.path.join(os.path.dirname(__file__), "studentMarks.txt")
students = []

def load_students():
    students.clear()
    try:
        with open(file_path, "r", encoding="utf-8-sig") as file:
            lines = file.readlines()[1:]
            for line in lines:
                data = line.strip().split(",")
                if len(data) == 6:
                    try:
                        students.append({
                            "code": data[0], "name": data[1],
                            "c1": int(data[2]), "c2": int(data[3]),
                            "c3": int(data[4]), "exam": int(data[5])
                        })
                    except ValueError:
                        continue
    except FileNotFoundError:
        messagebox.showerror("Error", "studentMarks.txt not found!")

# Calculate marks and grades
def calculate(s):
    coursework = s["c1"] + s["c2"] + s["c3"]
    total = coursework + s["exam"]
    percentage = total / 160 * 100
    grade = ("A" if percentage >= 70 else
             "B" if percentage >= 60 else
             "C" if percentage >= 50 else
             "D" if percentage >= 40 else "F")
    return coursework, total, percentage, grade

# Display student records
def display(records, title):
    table.delete(*table.get_children())
    heading.config(text=title)

    if not records:
        summary.config(text="No student records found.")
        return

    for s in records:
        cw, total, percent, grade = calculate(s)
        table.insert("", "end", values=(
            s["name"], s["code"], cw, s["exam"],
            total, f"{percent:.1f}%", grade
        ))

    average = sum(calculate(s)[2] for s in students) / len(students)
    summary.config(
        text=f"Students: {len(students)}    |    Class Average: {average:.1f}%"
    )

# Menu options
def view_all():
    display(students, "All Student Records")

def find_student():
    search = simpledialog.askstring(
        "Find Student", "Enter student name or number:", parent=root
    )
    if search:
        results = [s for s in students if
                   search.lower() in s["name"].lower()
                   or search.strip() == s["code"]]
        if results:
            display(results, "Individual Student Record")
        else:
            messagebox.showinfo("Not Found", "Student not found.")

def highest_student():
    if students:
        best = max(students, key=lambda s: calculate(s)[1])
        display([best], "Highest Overall Mark")

def lowest_student():
    if students:
        lowest = min(students, key=lambda s: calculate(s)[1])
        display([lowest], "Lowest Overall Mark")

# Main window
root = tk.Tk()
root.title("Student Manager")
root.geometry("1100x680")
root.configure(bg="#f1f4f9")
root.resizable(False, False)

dark, blue, light = "#17243a", "#3478f6", "#f1f4f9"

# Sidebar
sidebar = tk.Frame(root, bg=dark, width=240)
sidebar.pack(side="left", fill="y")
sidebar.pack_propagate(False)

tk.Label(sidebar, text="STUDENT\nMANAGER", font=("Arial", 21, "bold"),
         bg=dark, fg="white", justify="left").pack(anchor="w", padx=25, pady=(35, 10))

tk.Label(sidebar, text="RECORD MANAGEMENT", font=("Arial", 9, "bold"),
         bg=dark, fg="#91a3bd").pack(anchor="w", padx=25, pady=(5, 25))

# Create sidebar buttons
def menu_button(text, command, colour=dark):
    tk.Button(sidebar, text=text, command=command,
              font=("Arial", 10, "bold"), bg=colour, fg="white",
              activebackground="#40516d", activeforeground="white",
              relief="flat", anchor="w", padx=18, height=2,
              cursor="hand2").pack(fill="x", padx=12, pady=5)

menu_button("  1. View All Students", view_all)
menu_button("  2. Find a Student", find_student)
menu_button("  3. Highest Mark", highest_student)
menu_button("  4. Lowest Mark", lowest_student)
menu_button("  X  Quit", root.destroy, "#a93642")

# Main dashboard
main = tk.Frame(root, bg=light)
main.pack(side="right", fill="both", expand=True, padx=30, pady=25)

tk.Label(main, text="Dashboard", font=("Arial", 25, "bold"),
         bg=light, fg=dark).pack(anchor="w")

tk.Label(main, text="Manage and analyse student performance",
         font=("Arial", 11), bg=light, fg="#77849a").pack(anchor="w", pady=(4, 20))

# Summary section
card = tk.Frame(main, bg="white", padx=20, pady=15)
card.pack(fill="x", pady=(0, 20))

heading = tk.Label(card, text="Welcome to Student Manager",
                   font=("Arial", 15, "bold"), bg="white", fg=dark)
heading.pack(anchor="w")

summary = tk.Label(card, text="Loading records...",
                   font=("Arial", 10), bg="white", fg="#64748b")
summary.pack(anchor="w", pady=(8, 0))

# Student table
frame = tk.Frame(main, bg="white")
frame.pack(fill="both", expand=True)

columns = ("name", "code", "coursework", "exam", "total", "percentage", "grade")
table = ttk.Treeview(frame, columns=columns, show="headings")

titles = ("Student Name", "Student No.", "Coursework",
          "Exam", "Total /160", "Percentage", "Grade")
widths = (165, 85, 90, 65, 85, 95, 55)

for col, title, width in zip(columns, titles, widths):
    table.heading(col, text=title)
    table.column(col, width=width, anchor="center")

style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview", rowheight=38, font=("Arial", 10),
                background="white", foreground=dark, fieldbackground="white")
style.configure("Treeview.Heading", background="#e8edf5",
                foreground=dark, font=("Arial", 10, "bold"), padding=10)

scrollbar = ttk.Scrollbar(frame, orient="vertical", command=table.yview)
table.configure(yscrollcommand=scrollbar.set)
table.pack(side="left", fill="both", expand=True, padx=10, pady=10)
scrollbar.pack(side="right", fill="y", pady=10)

# Start application
load_students()
summary.config(text=f"{len(students)} student records loaded")
root.deiconify()
root.lift()
root.mainloop()
