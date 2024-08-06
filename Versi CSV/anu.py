from customtkinter import CTkFrame, CTkLabel, CTkButton, CTk, CTkScrollableFrame, CTkOptionMenu
from student import Students  # Ensure this module exists and is correctly imported
import tkinter as tk  # Import tkinter for StringVar

class ContectDisplayAllStudents(CTkScrollableFrame):
    def __init__(self, master, command=None, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure(1, weight=2)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.grid_columnconfigure(4, weight=1)
        self.grid_columnconfigure(5, weight=1)
        self.command = command
        self.label = []
        self.button = []
        self.label_list = []
        self.button_list = []

    def manage_button(self, data, image=None):
        label_id = CTkLabel(self, text=f"id : {data[0]}", image=image, compound="left", anchor="w", fg_color="white", corner_radius=10, width=100, height=24)
        label_name = CTkLabel(self, text=f"Name : {data[1]}", image=image, compound="left", anchor="w", fg_color="white", corner_radius=10, width=100, height=24)
        button_detail = CTkButton(self, text="Detail", width=100, height=24)
        button_delete = CTkButton(self, text="Delete", width=100, height=24, fg_color="red")
        button_update = CTkButton(self, text="Update", width=100, height=24, fg_color="orange")
        button_graph = CTkButton(self, text="Graph", width=100, height=24, fg_color="green")
        
        if self.command is not None:
            button_detail.configure(command=lambda: self.command('detail', data[1]))
            button_delete.configure(command=lambda: self.command('delete', data[1]))
            button_update.configure(command=lambda: self.command('update', data[1]))
            button_graph.configure(command=lambda: self.command('graph', data[1]))
        
        label_id.grid(row=len(self.label_list), column=0, pady=(0, 10), sticky="w", padx=28)
        label_name.grid(row=len(self.label_list), column=1, pady=(0, 10), sticky="w", padx=28)
        button_detail.grid(row=len(self.button_list), column=2, pady=(0, 10), padx=28)
        button_delete.grid(row=len(self.button_list), column=3, pady=(0, 10), padx=28)
        button_update.grid(row=len(self.button_list), column=4, pady=(0, 10), padx=28)
        button_graph.grid(row=len(self.button_list), column=5, pady=(0, 10), padx=28)
        
        self.label.append(label_id)
        self.label.append(label_name)
        
        self.button.append(button_detail)
        self.button.append(button_delete)
        self.button.append(button_update)
        self.button.append(button_graph)
        
        self.label_list.append(self.label)
        self.button_list.append(self.button)

class SkatingApp:
    def __init__(self, root):
        self.root = root
        self.db = Students()
        self.root.title("Skating Coach App")
        self.root.geometry("1365x700")

        # Frames
        self.frame_parent = CTkFrame(self.root, fg_color="white")
        self.frame_parent.place(relwidth=1, relheight=1)
        
        self.frame_header = CTkFrame(self.frame_parent)
        self.frame_header.place(relx=0.5, rely=0.08, relwidth=0.9, relheight=0.07, anchor="center")
        
        self.frame_content = CTkFrame(self.frame_parent, fg_color="white")
        self.frame_content.place(relx=0.5, rely=0.55, relwidth=0.9, relheight=0.8, anchor="center")
        
        # <--------------------------- HEADER --------------------------->
        
        # Month selection dropdown
        self.month_var = tk.StringVar()
        self.month_menu = CTkOptionMenu(self.frame_header, variable=self.month_var, values=[
            "januari", "febuari", "maret", "april", "mei", "juni", "juli", "agustus", "september", "oktober", "november", "desember"])
        self.month_menu.place(relx=0.5, rely=0.5, anchor="center")

        # Buttons
        self.btn_display_all = CTkButton(self.frame_header, text="Display All", command=self.display_all)
        self.btn_display_all.place(relx=0.25, rely=0.5, anchor="center")

        # <--------------------------- CONTENT --------------------------->
        
        # Initial display of students
        self.display_all()

    def clear_frame(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

    # Methods
    def display_all(self):
        self.clear_frame(self.frame_content)
        self.list_students = ContectDisplayAllStudents(self.frame_content, width=300, command=self.label_button_frame_event, corner_radius=20)
        self.list_students.place(relx=0.5, rely=0.5, relwidth=1, relheight=1, anchor="center")
        
        data = self.db.getAllstudents()
        
        for student in data:
            self.list_students.manage_button(student)

    def label_button_frame_event(self, action, item):
        student_id = next((student[0] for student in self.db.getAllstudents() if student[1] == item), None)
        selected_month = self.month_var.get()
        
        if action == 'detail' and student_id:
            self.display_student_details(student_id, selected_month)
        elif action == 'delete' and student_id:
            self.db.deleteData(student_id)
            self.display_all()  # Refresh the list
        elif action == 'update' and student_id:
            self.update_student(student_id)
        elif action == 'graph' and student_id:
            self.display_graph(student_id)

    def display_student_details(self, student_id, month):
        self.clear_frame(self.frame_content)
        student_details = self.db.getDetailStudent(student_id, month)
        student_name = self.db.getName(student_id)
        
        # Create header labels
        headers = ["ID", "Name", "Date", "Balance", "Strength", "Flexibility", "Endurance", "Core", "Semangat", "Total"]
        for i, header in enumerate(headers):
            CTkLabel(self.frame_content, text=header, width=100, height=24, fg_color="lightgrey").grid(row=0, column=i, padx=5, pady=5)

        # Display student details
        for row_index, detail in enumerate(student_details, start=1):
            detail_row = [student_id, student_name] + detail
            for col_index, item in enumerate(detail_row):
                CTkLabel(self.frame_content, text=item, width=100, height=24).grid(row=row_index, column=col_index, padx=5, pady=5)

    def update_student(self, student_id):
        # Implement update functionality
        pass

    def display_graph(self, student_id):
        # Implement graph functionality
        pass

if __name__ == "__main__":
    root = CTk()
    app = SkatingApp(root)
    root.mainloop()
