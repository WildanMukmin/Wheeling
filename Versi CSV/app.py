from customtkinter import CTkFrame, CTkLabel, CTkEntry, CTkButton, CTkTextbox, CTk
from tkinter import messagebox
from student import Students

class SkatingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Skating Coach App")
        self.root.geometry("1365x700")

        # Frames
        self.frame_header = CTkFrame(self.root)
        self.frame_header.place(relx = 0.5, rely = 0.08, relwidth = 0.9, relheight = 0.07, anchor = "center")
        
        self.frame_content = CTkFrame(self.root)
        self.frame_content.place(relx = 0.5, rely = 0.55, relwidth = 0.9, relheight = 0.8, anchor = "center")

        # Button
        self.btn_display_all = CTkButton(self.frame_header, text="Display All", command=self.display_all)
        self.btn_display_all.place(relx = 0.25, rely = 0.5, anchor = "center")

        self.btn_add_student = CTkButton(self.frame_header, text="Add Student", command=self.add_student)
        self.btn_add_student.place(relx = 0.5, rely = 0.5, anchor = "center")


    # Method
    def display_all(self):
        print("Btn Display All")
        
    def add_student(self):
        print("Btn Add Student")






if __name__ == "__main__":
    root = CTk()
    app = SkatingApp(root)
    root.mainloop()
