import csv
import os
from pathlib import Path
import shutil

# <---------------------- Akses File ---------------------->

def readFile(fileName):
    data = []
    try:
        with open(fileName, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                data.append(row)
    except FileNotFoundError:
        print(f"File {fileName} tidak ditemukan.")
    return data

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
    
    def addData(self, name, month):
        fileName = f"students.csv"
        params = False
        if not os.path.exists(fileName):
            print(f"File {fileName} tidak ditemukan.")
            return

        row = readFile(fileName)
        
        for i in row:
            if i[1] == name:
                params = True
                break
        
        if not params:
            new_row = [self.get_next_id(), name]
            row.append(new_row)

        with open(fileName, "w", newline='', encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["id", "name"])  # Add header row
            for i in row:
                writer.writerow(i)
        Student(name,month)

    def updateData(self, id, name):
        cwd = Path.cwd()
        folder_lama = cwd / 'data' / self.getName(id)
        folder_baru = cwd / 'data' / name
        
        if not os.path.exists(self.file_name):
            print("No data found.")
            return
        data = readFile(self.file_name)
        params = False
        
        for i in data:
            if i[0] == str(id):
                i[1] = name
                params = True
                break
        if params:
            with open(self.file_name, "w", newline='', encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(["id", "name"])  # Add header row
                for i in data:
                    writer.writerow(i)
            print(f"Data with ID {id} has been update.")
            os.rename(folder_lama, folder_baru)
        else:
            print(f"No data found with ID {id}.")

    def deleteData(self, id):
        cwd = Path.cwd()
        folder = cwd / 'data' / self.getName(id)
        
        if not os.path.exists(self.file_name):
            print("No data found.")
            return
        
        data_lama = readFile(self.file_name)
        data_baru = []
        params = False
        
        for i in data_lama:
            if i[0] == str(id):
                params = True
                continue
            data_baru.append(i)
            
        if params:
            with open(self.file_name, "w", newline='', encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(["id", "name"])  # Add header row
                for i in data_baru:
                    writer.writerow(i)
            print(f"Data with ID {id} has been deleted.")
            try:
                shutil.rmtree(folder)
                print(f"Folder '{folder}' beserta semua isinya berhasil dihapus.")
            except FileNotFoundError:
                print(f"Folder '{folder}' tidak ditemukan.")
            except PermissionError:
                print(f"Izin ditolak untuk menghapus folder '{folder}'.")
            except Exception as e:
                print(f"Terjadi kesalahan: {e}")
        else:
            print(f"No data found with ID {id}.")

    def addProgress(self, id, month, date, balance, strength, flexibility, endurance, core, semangat):
        fileName = f"data/{self.getName(id)}/{month}/data.csv"
        total = sum([balance, strength, flexibility, endurance, core, semangat])

        if not os.path.exists(fileName):
            print(f"File {fileName} tidak ditemukan.")
            Student(self.getName(id), month)
            self.addProgress(id, month, date, balance, strength, flexibility, endurance, core, semangat)
            return

        row = readFile(fileName)
        new_row = [date, balance, strength, flexibility, endurance, core, semangat, total]
        row.append(new_row)
        
        with open(fileName, "w", newline='', encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["date", "balance", "strength", "flexibility", "endurance", "core", "semangat", "total"])  # Add header row
            for i in row:
                writer.writerow(i)

        print(f"Progress for {self.getName(id)} on {date} in {month} has been added.")

    # <------------------- METHOD GETTER ------------------->
    
    def getAllstudents(self):
        data = readFile("students.csv")
        return data

    def getName (self, id):
        id = str(id)
        data = readFile("students.csv")
        for i in data:
            if i[0] == id:
                return i[1]
    
    def getDetailStudent(self, id, month):
        fileName = f"data/{self.getName(id)}/{month}/data.csv"
        data = readFile(fileName)
        return data
    
    def getDate(self, id, month):
        date = []
        fileName = f"data/{self.getName(id)}/{month}/data.csv"
        data = readFile(fileName)
        for i in data:
            # print(i[0])
            date.append(i[0])
        return date

    def getBalance(self, id, month):
        balance = []
        fileName = f"data/{self.getName(id)}/{month}/data.csv"
        data = readFile(fileName)
        for i in data:
            # print(i[0])
            balance.append(i[1])
        return balance

    def getStrength(self, id, month):
        strength = []
        fileName = f"data/{self.getName(id)}/{month}/data.csv"
        data = readFile(fileName)
        for i in data:
            # print(i[0])
            strength.append(i[2])
        return strength
    
    def getFlexibility(self, id, month):
        flexibility = []
        fileName = f"data/{self.getName(id)}/{month}/data.csv"
        data = readFile(fileName)
        for i in data:
            # print(i[0])
            flexibility.append(i[3])
        return flexibility
    
    def getEndurance(self, id, month):
        endurance = []
        fileName = f"data/{self.getName(id)}/{month}/data.csv"
        data = readFile(fileName)
        for i in data:
            # print(i[0])
            endurance.append(i[4])
        return endurance
    
    def getCore(self, id, month):
        core = []
        fileName = f"data/{self.getName(id)}/{month}/data.csv"
        data = readFile(fileName)
        for i in data:
            # print(i[0])
            core.append(i[5])
        return core
    
    def getSemangat(self, id, month):
        semangat = []
        fileName = f"data/{self.getName(id)}/{month}/data.csv"
        data = readFile(fileName)
        for i in data:
            # print(i[0])
            semangat.append(i[6])
        return semangat
    
    def getTotal(self, id, month):
        total = []
        fileName = f"data/{self.getName(id)}/{month}/data.csv"
        data = readFile(fileName)
        for i in data:
            # print(i[0])
            total.append(i[7])
        return total
        
    # <------------------- METHOD SETTER ------------------->

    def updateStudentData(self, id, month, date, balance=None, strength=None, flexibility=None, endurance=None, core=None, semangat=None):
        fileName = f"data/{self.getName(id)}/{month}/data.csv"
        data = readFile(fileName)
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
                    
                row[7] = int(row[1]) + int(row[2]) + int(row[3]) + int(row[4]) + int(row[5]) + int(row[6])

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
                    
    def setDate(self, id, month, old_date, new_date):
        fileName = f"data/{self.getName(id)}/{month}/data.csv"
        data = readFile(fileName)
        
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

