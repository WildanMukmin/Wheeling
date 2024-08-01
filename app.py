import customtkinter as ctk
from tkinter import messagebox
from database import Database
from datetime import datetime

class SkatingApp:
    def __init__(self, root):
        self.db = Database()
        self.db.create_tables()

        self.root = root
        self.root.title("Skating Coach App")

        # Frames
        self.frame_students = ctk.CTkFrame(self.root, width=300, height=150)
        self.frame_students.place(x=10, y=10)

        self.frame_assessments = ctk.CTkFrame(self.root, width=300, height=300)
        self.frame_assessments.place(x=10, y=170)

        self.frame_display_students = ctk.CTkFrame(self.root, width=400, height=200)
        self.frame_display_students.place(x=320, y=10)

        self.frame_display_assessments = ctk.CTkFrame(self.root, width=400, height=250)
        self.frame_display_assessments.place(x=320, y=220)

        # Add Student
        ctk.CTkLabel(self.frame_students, text="Add Student").place(x=10, y=10)
        ctk.CTkLabel(self.frame_students, text="Name:").place(x=10, y=40)
        self.entry_name = ctk.CTkEntry(self.frame_students)
        self.entry_name.place(x=60, y=40)

        ctk.CTkLabel(self.frame_students, text="Age:").place(x=10, y=70)
        self.entry_age = ctk.CTkEntry(self.frame_students)
        self.entry_age.place(x=60, y=70)

        self.btn_add_student = ctk.CTkButton(self.frame_students, text="Add", command=self.add_student)
        self.btn_add_student.place(x=60, y=100)

        # Delete Student
        ctk.CTkLabel(self.frame_students, text="Delete Student ID:").place(x=10, y=130)
        self.entry_delete_student_id = ctk.CTkEntry(self.frame_students)
        self.entry_delete_student_id.place(x=150, y=130)

        self.btn_delete_student = ctk.CTkButton(self.frame_students, text="Delete", command=self.delete_student)
        self.btn_delete_student.place(x=220, y=130)

        # Add Assessment
        ctk.CTkLabel(self.frame_assessments, text="Add Assessment").place(x=10, y=10)
        ctk.CTkLabel(self.frame_assessments, text="Student ID:").place(x=10, y=40)
        self.entry_student_id = ctk.CTkEntry(self.frame_assessments)
        self.entry_student_id.place(x=150, y=40)

        ctk.CTkLabel(self.frame_assessments, text="Date (YYYY-MM-DD):").place(x=10, y=70)
        self.entry_date = ctk.CTkEntry(self.frame_assessments)
        self.entry_date.place(x=150, y=70)

        self.scores = {}
        aspects = ['keseimbangan', 'kekuatan', 'flexibilitas', 'ketahanan', 'core', 'kemauan']
        for i, aspect in enumerate(aspects):
            ctk.CTkLabel(self.frame_assessments, text=f"{aspect.capitalize()}:").place(x=10, y=100 + i*30)
            self.scores[aspect] = ctk.CTkEntry(self.frame_assessments)
            self.scores[aspect].place(x=150, y=100 + i*30)

        self.btn_add_assessment = ctk.CTkButton(self.frame_assessments, text="Add", command=self.add_assessment)
        self.btn_add_assessment.place(x=10, y=280)

        # Display Students
        self.btn_display_students = ctk.CTkButton(self.frame_display_students, text="Display Students", command=self.display_students)
        self.btn_display_students.place(x=10, y=10)

        self.text_display_students = ctk.CTkTextbox(self.frame_display_students, height=150, width=380)
        self.text_display_students.place(x=10, y=50)

        # Display Assessments
        ctk.CTkLabel(self.frame_display_assessments, text="Student ID:").place(x=10, y=10)
        self.entry_assessment_student_id = ctk.CTkEntry(self.frame_display_assessments)
        self.entry_assessment_student_id.place(x=150, y=10)

        self.btn_display_assessments = ctk.CTkButton(self.frame_display_assessments, text="Display Assessments", command=self.display_assessments)
        self.btn_display_assessments.place(x=10, y=40)

        self.text_display_assessments = ctk.CTkTextbox(self.frame_display_assessments, height=180, width=380)
        self.text_display_assessments.place(x=10, y=80)

    def add_student(self):
        name = self.entry_name.get()
        age = self.entry_age.get()
        if name and age.isdigit():
            self.db.add_student(name, int(age))
            messagebox.showinfo("Success", "Student added successfully.")
            self.entry_name.delete(0, ctk.END)
            self.entry_age.delete(0, ctk.END)
        else:
            messagebox.showerror("Error", "Please enter valid name and age.")

    def delete_student(self):
        student_id = self.entry_delete_student_id.get()
        if student_id.isdigit():
            self.db.delete_student(int(student_id))
            messagebox.showinfo("Success", "Student deleted successfully.")
            self.entry_delete_student_id.delete(0, ctk.END)
        else:
            messagebox.showerror("Error", "Please enter a valid student ID.")

    def add_assessment(self):
        student_id = self.entry_student_id.get()
        date = self.entry_date.get()
        if not student_id.isdigit():
            messagebox.showerror("Error", "Please enter a valid student ID.")
            return

        if not self.valid_date(date):
            date = datetime.now().strftime('%Y-%m-%d')
        
        scores = {}
        for aspect, entry in self.scores.items():
            score = entry.get()
            if score.isdigit() and 1 <= int(score) <= 100:
                scores[aspect] = int(score)
            else:
                messagebox.showerror("Error", f"Please enter a valid score for {aspect}.")
                return

        self.db.add_assessment(int(student_id), date, scores)
        messagebox.showinfo("Success", "Assessment added successfully.")
        self.entry_student_id.delete(0, ctk.END)
        self.entry_date.delete(0, ctk.END)
        for entry in self.scores.values():
            entry.delete(0, ctk.END)

    def valid_date(self, date_str):
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
            return True
        except ValueError:
            return False

    def display_students(self):
        students = self.db.get_all_students()
        self.text_display_students.delete(1.0, ctk.END)
        for student in students:
            self.text_display_students.insert(ctk.END, f"ID: {student[0]}, Name: {student[1]}, Age: {student[2]}\n")

    def display_assessments(self):
        student_id = self.entry_assessment_student_id.get()
        if student_id.isdigit():
            assessments = self.db.get_assessments_by_student_id(int(student_id))
            self.text_display_assessments.delete(1.0, ctk.END)
            if assessments:
                for assessment in assessments:
                    self.text_display_assessments.insert(ctk.END, f"Date: {assessment[0]}, Aspect: {assessment[1]}, Score: {assessment[2]}\n")
            else:
                self.text_display_assessments.insert(ctk.END, "No assessments found for this student.\n")
        else:
            messagebox.showerror("Error", "Please enter a valid student ID.")

if __name__ == "__main__":
    root = ctk.CTk()
    app = SkatingApp(root)
    root.geometry("750x500")
    root.mainloop()
