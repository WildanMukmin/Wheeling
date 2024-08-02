import csv
import os
from pathlib import Path



# <---------------------- Akses File ---------------------->

def readFileCsv(fileName):
    items = []
    try:
        with open(fileName, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                if len(row) == 8:
                    items.append({
                        "id": row[0],
                        "date": row[1],
                        "balance": row[2],
                        "strength": row[3],
                        "flexibility": row[4],
                        "endurance": row[5],
                        "core": row[6],
                        "semangat": row[7]
                    })
    except FileNotFoundError:
        print(f"File {fileName} tidak ditemukan.")
    return items

# <---------------------- Class Student dan Students ---------------------->

class Student:
    def __init__(self, name, month):
        self.name = name
        self.month = month
        self.file_name = "data.txt"

        # Mendapatkan direktori kerja saat ini
        cwd = Path.cwd()

        # Membuat path lengkap untuk direktori baru
        lokasi = cwd / 'data' / name

        # Membuat direktori baru
        try:
            lokasi.mkdir(parents=True, exist_ok=True)
            print(f"Folder '{lokasi}' berhasil dibuat.")
        except OSError as e:
            print(f"Gagal membuat folder '{lokasi}'. Error: {e}")

        data = [["id", "date", "balance", "strength", "flexibility", "endurance", "core", "semangat"]]
        csv_file_path = lokasi / f"{month}.csv"

        try:
            with open(csv_file_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(data)
            print(f"File CSV '{csv_file_path}' berhasil dibuat.")
        except Exception as e:
            print(f"Gagal membuat file CSV '{csv_file_path}'. Error: {e}")

        self.check_data(name)

    def create_data(self, data):
        with open(self.file_name, "a") as file:
            file.write(data + "\n")

    def check_data(self, name):
        if not os.path.exists(self.file_name):
            print("No data found.")
            with open(self.file_name, "w") as file:
                file.write(name + "\n")
            return

        with open(self.file_name, "r") as file:
            lines = file.readlines()

        name_exists = False
        with open(self.file_name, "w") as file:
            for line in lines:
                if line.strip() == name:
                    name_exists = True
                file.write(line)
            if not name_exists:
                file.write(name + "\n")

            
class Students:
    def __init__(self):
        self.data = []
        self.file_name = "data.txt"

    # <------------------- METHOD CRUD ------------------->
    
    def create_data(self, data):
        with open(self.file_name, "a") as file:
            file.write(data + "\n")

    def read_data(self):
        if not os.path.exists(self.file_name):
            print("No data found.")
            return

        with open(self.file_name, "r") as file:
            for line in file:
                print(line.strip())

    def update_data(self, old_data, new_data):
        if not os.path.exists(self.file_name):
            print("No data found.")
            return

        with open(self.file_name, "r") as file:
            lines = file.readlines()

        with open(self.file_name, "w") as file:
            for line in lines:
                if line.strip() == old_data:
                    file.write(new_data + "\n")
                else:
                    file.write(line)

    def delete_data(self, data):
        if not os.path.exists(self.file_name):
            print("No data found.")
            return

        with open(self.file_name, "r") as file:
            lines = file.readlines()

        with open(self.file_name, "w") as file:
            for line in lines:
                if line.strip() != data:
                    file.write(line)

    # <------------------- METHOD SETTER DAN GETTER ------------------->

    def setDate(self, date):
        pass

    def setBalance(self, balance):
        pass

    def setStrength(self, strength):
        pass
    
    def setFlexibility(self, flexibility):
        pass
    
    def setEndurance(self, endurance):
        pass
    
    def setCore(self, core):
        pass
    
    def setSemangat(self, semangat):
        pass

    def getDate(self):
        pass

    def getBalance(self):
        pass

    def getStrength(self):
        pass
    
    def getFlexibility(self):
        pass
    
    def getEndurance(self):
        pass
    
    def getCore(self):
        pass
    
    def getSemangat(self):
        pass


    # <------------------- METHOD SETTER ------------------->
