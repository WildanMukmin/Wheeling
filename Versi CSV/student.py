import csv
import os
from pathlib import Path

# <---------------------- Akses File ---------------------->

def readData(fileName):
    assessments = []
    try:
        with open(fileName, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                if len(row) == 8:
                    assessments.append(row)
    except FileNotFoundError:
        print(f"File {fileName} tidak ditemukan.")
    return assessments

def readStudents(fileName):
    students = []
    try:
        with open(fileName, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                if len(row) == 2:
                    students.append(row)
    except FileNotFoundError:
        print(f"File {fileName} tidak ditemukan.")
    return students

# <---------------------- Class Student dan Students ---------------------->

class Student:
    def __init__(self, name, month):
        self.name = name
        self.month = month

        # Mendapatkan direktori kerja saat ini
        cwd = Path.cwd()

        # Membuat path lengkap untuk direktori baru
        lokasi = cwd / 'data' / name #untuk parent file
        bulan = cwd / 'data' / name / month #untuk parent file

        # Membuat direktori baru
        try:
            lokasi.mkdir(parents=True, exist_ok=True)
            print(f"Folder '{lokasi}' berhasil dibuat.")
        except OSError as e:
            print(f"Gagal membuat folder '{lokasi}'. Error: {e}")

        try:
            bulan.mkdir(parents=True, exist_ok=True)
            print(f"Folder '{bulan}' berhasil dibuat.")
        except OSError as e:
            print(f"Gagal membuat folder '{bulan}'. Error: {e}")

        data = [["date", "balance", "strength", "flexibility", "endurance", "core", "semangat", "total"]]
        csv_file_path = bulan / f"data.csv"

        try:
            with open(csv_file_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(data)
            print(f"File CSV '{csv_file_path}' berhasil dibuat.")
        except Exception as e:
            print(f"Gagal membuat file CSV '{csv_file_path}'. Error: {e}")

        self.check_data(name)

    def check_data(self, name):
        if not os.path.exists('students.csv'):
            print("No data found.")
            with open('students.csv', "w", newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["id", "name"])
                writer.writerow([1, name])
            return

        with open('students.csv', "r") as file:
            reader = csv.reader(file)
            lines = list(reader)
        
        name_exists = False
        for line in lines:
            if line[1] == name:
                name_exists = True
                break

        if not name_exists:
            new_id = int(lines[-1][0]) + 1 if len(lines) > 1 else 1
            with open('students.csv', "a", newline='') as file:
                writer = csv.writer(file)
                writer.writerow([new_id, name])

class Students:
    def __init__(self):
        self.file_name = "students.csv"
        self.ensure_csv_file_exists()

    def ensure_csv_file_exists(self):
        if not os.path.exists(self.file_name):
            with open(self.file_name, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["id", "name"])

    def get_next_id(self):
        if not os.path.exists(self.file_name):
            return 1

        with open(self.file_name, 'r') as file:
            reader = csv.reader(file)
            rows = list(reader)
            if len(rows) <= 1:
                return 1
            last_row = rows[-1]
            return int(last_row[0]) + 1

    # <------------------- METHOD CRUD ------------------->
    
    def create_data(self, name):
        new_id = self.get_next_id()
        with open(self.file_name, "a", newline='') as file:
            writer = csv.writer(file)
            writer.writerow([new_id, name])

    def read_data(self):
        data = []
        if not os.path.exists(self.file_name):
            print("No data found.")
            return

        with open(self.file_name, "r") as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                data.append([row[0], row[1]])
                print(f"ID: {row[0]}, Name: {row[1]}")

    def update_data(self, student_id, new_name):
        if not os.path.exists(self.file_name):
            print("No data found.")
            return

        rows = []
        updated = False
        with open(self.file_name, "r") as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == str(student_id):
                    row[1] = new_name
                    updated = True
                rows.append(row)

        if updated:
            with open(self.file_name, "w", newline='') as file:
                writer = csv.writer(file)
                writer.writerows(rows)
            print(f"Data with ID {student_id} has been updated.")
        else:
            print(f"No data found with ID {student_id}.")

    def delete_data(self, student_id):
        if not os.path.exists(self.file_name):
            print("No data found.")
            return

        rows = []
        deleted = False
        with open(self.file_name, "r") as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] != str(student_id):
                    rows.append(row)
                else:
                    deleted = True

        if deleted:
            with open(self.file_name, "w", newline='') as file:
                writer = csv.writer(file)
                writer.writerows(rows)
            print(f"Data with ID {student_id} has been deleted.")
        else:
            print(f"No data found with ID {student_id}.")

    # <------------------- METHOD GETTER ------------------->
    def getAllstudents(self):
        pass

    def getDate(self, name, month):
        pass

    def getBalance(self, name, month):
        pass

    def getStrength(self, name, month):
        pass
    
    def getFlexibility(self, name, month):
        pass
    
    def getEndurance(self, name, month):
        pass
    
    def getCore(self, name, month):
        pass
    
    def getSemangat(self, name, month):
        pass
                    
    # <------------------- METHOD SETTER ------------------->

    def setDate(self, name, month, date):
        pass

    def setBalance(self, name, month, balance):
        pass

    def setStrength(self, name, month, strength):
        pass
    
    def setFlexibility(self, name, month, flexibility):
        pass
    
    def setEndurance(self, name, month, endurance):
        pass
    
    def setCore(self, name, month, core):
        pass
    
    def setSemangat(self, name, month, semangat):
        pass


anu = Student("mub", "agustus")