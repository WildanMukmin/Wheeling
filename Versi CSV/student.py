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
        data = readStudents("students.csv")
        return data

    def getName (self, id):
        id = str(id)
        data = readStudents("students.csv")
        for i in data:
            if i[0] == id:
                return i[1]
    
    def getDetailStudent(self, id, month):
        fileName = f"data/{self.getName(id)}/{month}/data.csv"
        data = readData(fileName)
        return data
    
    def getDate(self, id, month):
        date = []
        fileName = f"data/{self.getName(id)}/{month}/data.csv"
        data = readData(fileName)
        for i in data:
            # print(i[0])
            date.append(i[0])
        return date

    def getBalance(self, id, month):
        balance = []
        fileName = f"data/{self.getName(id)}/{month}/data.csv"
        data = readData(fileName)
        for i in data:
            # print(i[0])
            balance.append(i[1])
        return balance

    def getStrength(self, id, month):
        strength = []
        fileName = f"data/{self.getName(id)}/{month}/data.csv"
        data = readData(fileName)
        for i in data:
            # print(i[0])
            strength.append(i[2])
        return strength
    
    def getFlexibility(self, id, month):
        flexibility = []
        fileName = f"data/{self.getName(id)}/{month}/data.csv"
        data = readData(fileName)
        for i in data:
            # print(i[0])
            flexibility.append(i[3])
        return flexibility
    
    def getEndurance(self, id, month):
        endurance = []
        fileName = f"data/{self.getName(id)}/{month}/data.csv"
        data = readData(fileName)
        for i in data:
            # print(i[0])
            endurance.append(i[4])
        return endurance
    
    def getCore(self, id, month):
        core = []
        fileName = f"data/{self.getName(id)}/{month}/data.csv"
        data = readData(fileName)
        for i in data:
            # print(i[0])
            core.append(i[5])
        return core
    
    def getSemangat(self, id, month):
        semangat = []
        fileName = f"data/{self.getName(id)}/{month}/data.csv"
        data = readData(fileName)
        for i in data:
            # print(i[0])
            semangat.append(i[6])
        return semangat
    
    def getTotal(self, id, month):
        total = []
        fileName = f"data/{self.getName(id)}/{month}/data.csv"
        data = readData(fileName)
        for i in data:
            # print(i[0])
            total.append(i[7])
        return total
        
    def updateStudentData(self, id, month, date, balance=None, strength=None, flexibility=None, endurance=None, core=None, semangat=None, total=None):
        fileName = f"data/{self.getName(id)}/{month}/data.csv"
        data = readData(fileName)
        
        # Find the row with the given date and update the corresponding columns
        updated = False
        for row in data:
            if row[0] == date:
                if balance is not None:
                    row[1] = balance
                if strength is not None:
                    row[2] = strength
                if flexibility is not None:
                    row[3] = flexibility
                if endurance is not None:
                    row[4] = endurance
                if core is not None:
                    row[5] = core
                if semangat is not None:
                    row[6] = semangat
                if total is not None:
                    row[7] = total
                updated = True
                break
        
        if updated:
            with open(fileName, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["date", "balance", "strength", "flexibility", "endurance", "core", "semangat", "total"])
                writer.writerows(data)
            print(f"Data for {self.getName(id)} on {date} in {month} has been updated.")
        else:
            print(f"No data found for {self.getName(id)} on {date} in {month}.")
                    
    # <------------------- METHOD SETTER ------------------->

    def setDate(self, id, month, old_date, new_date):
        fileName = f"data/{self.getName(id)}/{month}/data.csv"
        data = readData(fileName)
        
        # Find the row with the given old_date and update the date
        updated = False
        for row in data:
            if row[0] == old_date:
                row[0] = new_date
                updated = True
                break
        
        if updated:
            with open(fileName, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["date", "balance", "strength", "flexibility", "endurance", "core", "semangat", "total"])
                writer.writerows(data)
            print(f"Date for {self.getName(id)} on {old_date} in {month} has been updated to {new_date}.")
        else:
            print(f"No data found for {self.getName(id)} on {old_date} in {month}.")

    def setBalance(self, id, month, date, balance):
        self.updateStudentData(id, month, date, balance=balance)

    def setStrength(self, id, month, date, strength):
        self.updateStudentData(id, month, date, strength=strength)

    def setFlexibility(self, id, month, date, flexibility):
        self.updateStudentData(id, month, date, flexibility=flexibility)
    
    def setEndurance(self, id, month, date, endurance):
        self.updateStudentData(id, month, date, endurance=endurance)
    
    def setCore(self, id, month, date, core):
        self.updateStudentData(id, month, date, core=core)
    
    def setSemangat(self, id, month, date, semangat):
        self.updateStudentData(id, month, date, semangat=semangat)


anu = Students()
 
print(anu.getTotal(2,"agustus"))