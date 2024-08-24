from customtkinter import CTkFrame, CTkLabel, CTkButton, CTkEntry, CTkOptionMenu, CTk, CTkScrollableFrame
from tkinter import StringVar
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from student import Students

class ContectDisplayAllStudents(CTkScrollableFrame):
    def __init__(self, master, command=None, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure(1, weight=2)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.grid_columnconfigure(4, weight=1)
        self.grid_columnconfigure(5, weight=1)
        self.grid_columnconfigure(6, weight=1)
        self.command = command
        self.label = []
        self.button = []
        self.label_list = []
        self.button_list = []

    def manage_button(self, data, image=None):
        label_id = CTkLabel(self, text=f"id : {data[0]}", image=image, compound="left", anchor="w", fg_color="#1E3A8A", text_color="white", corner_radius=10, width=100, height=24)
        label_name = CTkLabel(self, text=f"Name : {data[1]}", image=image, compound="left", anchor="w", fg_color="#047857", text_color="white", corner_radius=10, width=100, height=24)
        button_newData = CTkButton(self, text="NewData", width=100, height=24, fg_color="#10B981", hover_color="#10B931")
        button_detail = CTkButton(self, text="Detail", width=100, height=24, fg_color="#3B82F6", hover_color="#3B82A6")
        button_delete = CTkButton(self, text="Delete", width=100, height=24, fg_color="#EF4444", hover_color="#EF4F74")
        button_update = CTkButton(self, text="Update", width=100, height=24, fg_color="#F59E0B", hover_color="#F56E02")
        button_graph = CTkButton(self, text="Graph", width=100, height=24, fg_color="#8B5CF6", hover_color="#8B5CA6")
        
        if self.command is not None:
            button_newData.configure(command=lambda: self.command('newData', data[1]))
            button_detail.configure(command=lambda: self.command('detail', data[1]))
            button_delete.configure(command=lambda: self.command('delete', data[1]))
            button_update.configure(command=lambda: self.command('update', data[1]))
            button_graph.configure(command=lambda: self.command('graph', data[1]))
        
        label_id.grid(row=len(self.label_list), column=0, pady=(0, 10), sticky="w", padx=28)
        label_name.grid(row=len(self.label_list), column=1, pady=(0, 10), sticky="w", padx=28)
        button_newData.grid(row=len(self.button_list), column=2, pady=(0, 10), padx=28)
        button_detail.grid(row=len(self.button_list), column=3, pady=(0, 10), padx=28)
        button_delete.grid(row=len(self.button_list), column=4, pady=(0, 10), padx=28)
        button_update.grid(row=len(self.button_list), column=5, pady=(0, 10), padx=28)
        button_graph.grid(row=len(self.button_list), column=6, pady=(0, 10), padx=28)
        
        self.label.append(label_id)
        self.label.append(label_name)
        
        self.button.append(button_newData)
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
        self.current_month = None
        
        # Frames
        self.frame_parent = CTkFrame(self.root, fg_color="white")
        self.frame_parent.place(relwidth=1, relheight=1)
        
        self.frame_header = CTkFrame(self.frame_parent)
        self.frame_header.place(relx=0.5, rely=0.08, relwidth=0.9, relheight=0.07, anchor="center")
        
        self.frame_content = CTkFrame(self.frame_parent, fg_color="white")
        self.frame_content.place(relx=0.5, rely=0.55, relwidth=0.9, relheight=0.8, anchor="center")
        
        # <--------------------------- HEADER --------------------------->
        
        # Month selection dropdown
        self.month_var = StringVar(value="agustus")
        self.month_menu = CTkOptionMenu(self.frame_header, variable=self.month_var, values=[
            "januari", "febuari", "maret", "april", "mei", "juni", "juli", "agustus", "september", "oktober", "november", "desember"])
        self.month_menu.place(relx=0.5, rely=0.5, anchor="center")

        # Buttons
        self.btn_display_all = CTkButton(self.frame_header, text="Display All", command=self.display_all)
        self.btn_display_all.place(relx=0.25, rely=0.5, anchor="center")

        self.btn_add_student = CTkButton(self.frame_header, text="Add New Student", command=self.add_student)
        self.btn_add_student.place(relx=0.75, rely=0.5, anchor="center")

        # <--------------------------- CONTENT --------------------------->
        
        # Initial display of students
        self.display_all()

    def clear_frame(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

    def display_all(self):
        self.clear_frame(self.frame_content)
        self.list_students = ContectDisplayAllStudents(self.frame_content, width=300, command=self.label_button_frame_event, corner_radius=20)
        self.list_students.place(relx=0.5, rely=0.5, relwidth=1, relheight=1, anchor="center")
        
        data = self.db.getAllstudents()
        
        for student in data:
            self.list_students.manage_button(student)

    def add_student(self):
        self.clear_frame(self.frame_content)
        
        CTkLabel(self.frame_content, text="Nama").grid(row=0, column=0, padx=10, pady=10)
        name_entry = CTkEntry(self.frame_content)
        name_entry.grid(row=0, column=1, padx=10, pady=10)
        
        CTkLabel(self.frame_content, text="Bulan").grid(row=1, column=0, padx=10, pady=10)
        month_entry = CTkEntry(self.frame_content)
        month_entry.grid(row=1, column=1, padx=10, pady=10)
        
        def add_new():
            name = name_entry.get()
            month = month_entry.get()

            self.db.addData(name,month)
            self.display_all()
        
        add_button = CTkButton(self.frame_content, text="Add", command=add_new)
        add_button.grid(row=7, column=0, columnspan=2, pady=20)

    def label_button_frame_event(self, action, data):
        id = next((student[0] for student in self.db.getAllstudents() if student[1] == data), None)
        selected_month = self.month_var.get()
        
        if action == 'newData' and id:
            self.add_new_progress(id, selected_month)
        elif action == 'detail' and id:
            self.display_student_details(id, selected_month)
        elif action == 'delete' and id:
            self.delete_student(id)
            self.display_all()  # Refresh the list
        elif action == 'update' and id:
            self.update_student(id, selected_month)
        elif action == 'graph' and id:
            self.display_graph(id, selected_month)
    
    def add_new_progress(self, id, month):
        self.clear_frame(self.frame_content)
        
        CTkLabel(self.frame_content, text="Date").grid(row=0, column=0, padx=10, pady=10)
        date_entry = CTkEntry(self.frame_content, placeholder_text="Masukan Date", width=180)
        date_entry.grid(row=0, column=1, padx=10, pady=10)
        
        CTkLabel(self.frame_content, text="Balance").grid(row=1, column=0, padx=10, pady=10)
        balance_entry = CTkEntry(self.frame_content, placeholder_text="Masukan Balanace Point", width=180)
        balance_entry.grid(row=1, column=1, padx=10, pady=10)
        
        CTkLabel(self.frame_content, text="Strength").grid(row=2, column=0, padx=10, pady=10)
        strength_entry = CTkEntry(self.frame_content, placeholder_text="Masukan Strength Point", width=180)
        strength_entry.grid(row=2, column=1, padx=10, pady=10)
        
        CTkLabel(self.frame_content, text="Flexibility").grid(row=3, column=0, padx=10, pady=10)
        flexibility_entry = CTkEntry(self.frame_content, placeholder_text="Masukan Flexibility Point", width=180)
        flexibility_entry.grid(row=3, column=1, padx=10, pady=10)
        
        CTkLabel(self.frame_content, text="Endurance").grid(row=4, column=0, padx=10, pady=10)
        endurance_entry = CTkEntry(self.frame_content, placeholder_text="Masukan Endurance Point", width=180)
        endurance_entry.grid(row=4, column=1, padx=10, pady=10)
        
        CTkLabel(self.frame_content, text="Core").grid(row=5, column=0, padx=10, pady=10)
        core_entry = CTkEntry(self.frame_content, placeholder_text="Masukan Core Point", width=180)
        core_entry.grid(row=5, column=1, padx=10, pady=10)
        
        CTkLabel(self.frame_content, text="Semangat").grid(row=6, column=0, padx=10, pady=10)
        semangat_entry = CTkEntry(self.frame_content, placeholder_text="Masukan Semangat Point", width=180)
        semangat_entry.grid(row=6, column=1, padx=10, pady=10)
        
        def save_progress():
            date = date_entry.get()
            balance = int(balance_entry.get())
            strength = int(strength_entry.get())
            flexibility = int(flexibility_entry.get())
            endurance = int(endurance_entry.get())
            core = int(core_entry.get())
            semangat = int(semangat_entry.get())
            self.db.addProgress(id, month, date, balance, strength, flexibility, endurance, core, semangat)
            self.display_student_details(id, month)  # Refresh the details display
        
        save_button = CTkButton(self.frame_content, text="Save", command=save_progress)
        save_button.grid(row=7, column=0, columnspan=2, pady=20)

    def display_student_details(self, id, month):
        self.clear_frame(self.frame_content)
        student_details = self.db.getDetailStudent(id, month)
        student_name = self.db.getName(id)
        
        # Create header labels
        headers = ["ID", "Name", "Date", "Balance", "Strength", "Flexibility", "Endurance", "Core", "Semangat", "Total"]
        for i, header in enumerate(headers):
            CTkLabel(self.frame_content, text=header, width=100, height=24, fg_color="lightgrey").grid(row=0, column=i, padx=11, pady=10)

        # Display student details
        for row_index, detail in enumerate(student_details, start=1):
            detail_row = [id, student_name] + detail
            for col_index, data in enumerate(detail_row):
                CTkLabel(self.frame_content, text=data, width=100, height=24, fg_color="skyblue").grid(row=row_index, column=col_index, padx=5, pady=5)

    def delete_student(self, id):
        self.db.deleteData(id)

    def update_student(self, id, month):
        self.clear_frame(self.frame_content)
        self.current_month = month
        old_date = self.db.getDate(id, self.current_month)
        
        self.date_var = StringVar(value=old_date[0])
        self.date_menu = CTkOptionMenu(self.frame_content, variable=self.date_var, values=old_date)
        self.date_menu.grid(row=0, column=1, padx=10, pady=10)

        # Variabel untuk menyimpan data
        balance_var = StringVar()
        strength_var = StringVar()
        flexibility_var = StringVar()
        endurance_var = StringVar()
        core_var = StringVar()
        semangat_var = StringVar()
        
        def refresh():
            self.clear_frame(self.frame_content)
            
            # Mengambil nilai yang diperbarui
            old_date = self.db.getDate(id, self.current_month)
            
            balance_temp = self.db.getBalance(id, self.current_month)
            strength_temp = self.db.getStrength(id, self.current_month)
            flexibility_temp = self.db.getFlexibility(id, self.current_month)
            endurance_temp = self.db.getEndurance(id, self.current_month)
            core_temp = self.db.getCore(id, self.current_month)
            semangat_temp = self.db.getSemangat(id, self.current_month)
            
            for i in range(len(old_date)):
                # print(old_date[i])
                # print(self.date_var.get())
                if old_date[i] == self.date_var.get():
                    balance_var.set(balance_temp[i])
                    strength_var.set(strength_temp[i])
                    flexibility_var.set(flexibility_temp[i])
                    endurance_var.set(endurance_temp[i])
                    core_var.set(core_temp[i])
                    semangat_var.set(semangat_temp[i])
                    break
            
            refresh_button = CTkButton(self.frame_content, text="Refresh", command=refresh)
            refresh_button.grid(row=0, column=3, padx=10, pady=10)
            
            self.date_menu = CTkOptionMenu(self.frame_content, variable=self.date_var, values=old_date)
            self.date_menu.grid(row=0, column=1, padx=10, pady=10)
            
            # Balance
            CTkLabel(self.frame_content, text="Balance").grid(row=1, column=0, padx=10, pady=10)
            balance_entry = CTkEntry(self.frame_content, textvariable=balance_var)
            balance_entry.grid(row=1, column=1, padx=10, pady=10)
            
            # Strength
            CTkLabel(self.frame_content, text="Strength").grid(row=2, column=0, padx=10, pady=10)
            strength_entry = CTkEntry(self.frame_content, textvariable=strength_var)
            strength_entry.grid(row=2, column=1, padx=10, pady=10)
            
            # Flexibility
            CTkLabel(self.frame_content, text="Flexibility").grid(row=3, column=0, padx=10, pady=10)
            flexibility_entry = CTkEntry(self.frame_content, textvariable=flexibility_var)
            flexibility_entry.grid(row=3, column=1, padx=10, pady=10)
            
            # Endurance
            CTkLabel(self.frame_content, text="Endurance").grid(row=4, column=0, padx=10, pady=10)
            endurance_entry = CTkEntry(self.frame_content, textvariable=endurance_var)
            endurance_entry.grid(row=4, column=1, padx=10, pady=10)
            
            # Core
            CTkLabel(self.frame_content, text="Core").grid(row=5, column=0, padx=10, pady=10)
            core_entry = CTkEntry(self.frame_content, textvariable=core_var)
            core_entry.grid(row=5, column=1, padx=10, pady=10)
            
            # Semangat
            CTkLabel(self.frame_content, text="Semangat").grid(row=6, column=0, padx=10, pady=10)
            semangat_entry = CTkEntry(self.frame_content, textvariable=semangat_var)
            semangat_entry.grid(row=6, column=1, padx=10, pady=10)            

            update_button = CTkButton(self.frame_content, text="Update", command=update)
            update_button.grid(row=7, column=0, columnspan=2, pady=20)
        
        refresh_button = CTkButton(self.frame_content, text="Refresh", command=refresh)
        refresh_button.grid(row=0, column=3, padx=10, pady=10)

        CTkLabel(self.frame_content, text="Balance").grid(row=1, column=0, padx=10, pady=10)
        balance_entry = CTkEntry(self.frame_content)
        balance_entry.grid(row=1, column=1, padx=10, pady=10)

        CTkLabel(self.frame_content, text="Strength").grid(row=2, column=0, padx=10, pady=10)
        strength_entry = CTkEntry(self.frame_content)
        strength_entry.grid(row=2, column=1, padx=10, pady=10)

        CTkLabel(self.frame_content, text="Flexibility").grid(row=3, column=0, padx=10, pady=10)
        flexibility_entry = CTkEntry(self.frame_content)
        flexibility_entry.grid(row=3, column=1, padx=10, pady=10)

        CTkLabel(self.frame_content, text="Endurance").grid(row=4, column=0, padx=10, pady=10)
        endurance_entry = CTkEntry(self.frame_content)
        endurance_entry.grid(row=4, column=1, padx=10, pady=10)

        CTkLabel(self.frame_content, text="Core").grid(row=5, column=0, padx=10, pady=10)
        core_entry = CTkEntry(self.frame_content)
        core_entry.grid(row=5, column=1, padx=10, pady=10)

        CTkLabel(self.frame_content, text="Semangat").grid(row=6, column=0, padx=10, pady=10)
        semangat_entry = CTkEntry(self.frame_content)
        semangat_entry.grid(row=6, column=1, padx=10, pady=10)
        
        def update():
            balance = int(balance_var.get())
            strength = int(strength_var.get())
            flexibility = int(flexibility_var.get())
            endurance = int(endurance_var.get())
            core = int(core_var.get())
            semangat = int(semangat_var.get())

            self.db.updateStudentData(id, self.current_month, self.date_var.get(), balance=balance, strength=strength, flexibility=flexibility, endurance=endurance, core=core, semangat=semangat)
            self.display_student_details(id, self.current_month)  # Refresh the details display

        update_button = CTkButton(self.frame_content, text="Update", command=update)
        update_button.grid(row=7, column=0, columnspan=2, pady=20)

    # def display_graph(self, id, month):
    #     self.clear_frame(self.frame_content)

    #     fig, ax = plt.subplots()

    #     def plot_graf():
    #         ax.clear()
    #         ax.set_xlabel('Tanggal', labelpad=30)
    #         ax.set_ylabel('Point', labelpad=30)
    #         ax.set_title(f'Progress {self.db.getName(id)} di bulan {month}', pad=35)
            
    #         ax.plot(self.db.getDate(id, month), self.db.getBalance(id, month), label='Balance')
    #         ax.plot(self.db.getDate(id, month), self.db.getStrength(id, month), label='Strength')
    #         ax.plot(self.db.getDate(id, month), self.db.getFlexibility(id, month), label='Flexibility')
    #         ax.plot(self.db.getDate(id, month), self.db.getEndurance(id, month), label='Endurance')
    #         ax.plot(self.db.getDate(id, month), self.db.getCore(id, month), label='Core')
    #         ax.plot(self.db.getDate(id, month), self.db.getSemangat(id, month), label='Semangat')

    #         ax.legend(loc="upper left", bbox_to_anchor=(1, 1), facecolor='white', edgecolor='black')
    #         plt.yticks(range(2, 20, 2))
    #         plt.subplots_adjust(right=0.8)  # Mengurangi ruang kosong di sebelah kanan
            
    #         plt.savefig(f"./data/{self.db.getName(id)}/{month}/plot_graf.png", bbox_inches='tight')

    #     def plot_total_graf():
    #         ax.clear()
    #         ax.set_xlabel('Tanggal', labelpad=30)
    #         ax.set_ylabel('Point', labelpad=30)
    #         ax.set_title(f'Progress total {self.db.getName(id)} di bulan {month}', pad=35)
    #         ax.grid()
            
    #         ax.plot(self.db.getDate(id, month), self.db.getTotal(id, month), label='Total')

    #         ax.legend(loc="upper left", bbox_to_anchor=(1, 1), facecolor='white', edgecolor='black')
    #         plt.yticks(range(10, 110, 10))
    #         plt.subplots_adjust(right=0.8)  # Mengurangi ruang kosong di sebelah kanan
            
    #         plt.savefig(f"./data/{self.db.getName(id)}/{month}/plot_graf_total.png", bbox_inches='tight')

    #     graph_frame = CTkFrame(self.frame_content, fg_color="white")
    #     graph_frame.pack(fill="both", expand=True)
        
    #     button_frame = CTkFrame(self.frame_content)
    #     button_frame.pack(fill="x", expand=False)
        
    #     CTkButton(button_frame, text="Graph", command=plot_graf).pack(side='left', padx=10, pady=10)
    #     CTkButton(button_frame, text="Total Graph", command=plot_total_graf).pack(side='right', padx=10, pady=10)
        
    #     plot_graf()  # Plot default grafik ketika frame pertama kali ditampilkan




if __name__ == "__main__":
    root = CTk()
    app = SkatingApp(root)
    root.mainloop()
