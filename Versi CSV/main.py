import csv
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# <---------------------- Akses File ---------------------->

def readFileCsv(fileName):
    items = []
    try:
        with open(fileName, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                if len(row) == 4:
                    items.append(Item(row[0], row[1], int(row[2]), int(row[3])))
    except FileNotFoundError:
        pass
    return items

# <---------------------- Algoritma Sorting ---------------------->

def mergeSort(arr, parameter):
    if len(arr) <= 1:
        return arr
    
    mid = len(arr) // 2
    left = mergeSort(arr[:mid], parameter)
    right = mergeSort(arr[mid:], parameter)
    
    return merge(left, right, parameter)

def merge(left, right, parameter):
    result = []
    i = j = 0
    
    while i < len(left) and j < len(right):
        if getattr(left[i], parameter) < getattr(right[j], parameter):
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    while i < len(left):
        result.append(left[i])
        i += 1
    while j < len(right):
        result.append(right[j])
        j += 1
    
    return result

# <---------------------- Algoritma Search ---------------------->

def binarySearch(arr, target_id):
    left, right = 0, len(arr) - 1

    while left <= right:
        mid = (left + right) // 2
        current_id = arr[mid].id
        
        if current_id == target_id:
            return mid
        elif current_id < target_id:
            left = mid + 1
        else:
            right = mid - 1

    return -1

# <---------------------- Class Item dan Gudang ---------------------->

class Item:
    def __init__(self, id, name, quantity, price):
        self.id = id
        self.name = name
        self.quantity = int(quantity)
        self.price = int(price)
    
    def to_list(self):
        return [self.id, self.name, self.quantity, self.price]

class Gudang:
    def __init__(self):
        self.items = readFileCsv("items.csv")

    def getAllproduct(self):
        return [item.to_list() for item in self.items]
    
    def getNameItem(self, id):
        item = self.SearchItemById(id)
        return item.name if item else None
    
    def getPriceItem(self, id):
        item = self.SearchItemById(id)
        return item.price if item else None

    def getQuantityItem(self, id):
        item = self.SearchItemById(id)
        return item.quantity if item else None

    def setNameItem(self, id, name):
        item = self.SearchItemById(id)
        if item:
            item.name = name
            self.updateFileCsv()

    def setPriceItem(self, id, price):
        item = self.SearchItemById(id)
        if item:
            item.price = price
            self.updateFileCsv()

    def setQuantityItem(self, id, quantity):
        item = self.SearchItemById(id)
        if item:
            item.quantity = quantity
            self.updateFileCsv()

    def addItem(self, name, quantity, price):
        self.sortById()
        self.next_id = int(self.items[-1].to_list()[0]) + 1
        self.items.append(Item(str(self.next_id), name, quantity, price))
        self.updateFileCsv()
        
    def removeItemByName(self, name):
        self.items = [item for item in self.items if item.name != name]
        self.updateFileCsv()
    
    def removeItemById(self, id):
        self.items = [item for item in self.items if item.id != id]
        self.updateFileCsv()
    
    def updateFileCsv(self):
        with open("items.csv", "w", newline='', encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(['id', 'name', 'quantity', 'price'])  # Add header row
            for item in self.items:
                writer.writerow(item.to_list())

    def sortByPrice(self):
        self.items = mergeSort(self.items, 'price')
        self.updateFileCsv()

    def sortByQuantity(self):
        self.items = mergeSort(self.items, 'quantity')
        self.updateFileCsv()

    def sortById(self):
        self.items = mergeSort(self.items, 'id')
        self.updateFileCsv()
    
    def SearchItemById(self, id):
        self.sortById()
        index = binarySearch(self.items, id)
        if index != -1:
            return self.items[index]
        return None
    
    def searchByName(self, name):
        return [item for item in self.items if item.name.lower() == name.lower()]
    
    def displayAllproduct(self):
        for item in self.items:
            print(item.to_list())

class GudangApp(tk.Tk):
    
    def __init__(self, gudang):
        super().__init__()
        
        self.gudang = gudang
        self.title("Gudang Inventory Management")
        self.geometry("1365x700")
        # self.attributes('-fullscreen', True)
        # self.resizable(False, False)
        
        # <---------------------- ALL STYLE CONFIGURE ---------------------->
        self.style = ttk.Style(self)
        
        # <---------------------- STYLE FRAME ---------------------->
        self.style.configure("general_style.TFrame", background="#1064a3")
        self.style.configure("form_style.TFrame", background="#3194eb")
        self.style.configure("nav_style.TFrame", background="#1064a3")
        
        # <---------------------- STYLE LABEL ---------------------->
        self.style.configure("general_style.TLabel", background="lightblue", font=("Arial", 12))
        self.style.configure("form_style.TLabel", background="#3194eb", font=("Arial", 12), foreground='white')
        
        # <---------------------- STYLE ENTRY ---------------------->
        self.style.configure("general_style.TEntry", font=("Arial", 12))
        self.style.configure("form_style.TEntry", font=("Arial", 12))
        
        # <---------------------- STYLE BUTTON ---------------------->
        self.style.configure('general_style.TButton', font=('Helvetica', 6), relief='flat', background='#000000', foreground='black')
        self.style.configure('form_style.TButton', font=('Helvetica', 6), relief='flat', background='#000000', foreground='black')
        
        # <---------------------- STYLE LIST ITEM ---------------------->
        self.style.configure('list_items.TLabel', font=('Helvetica', 10, 'bold'), background='#f0f0f0', foreground='#333333',padding=10)
        
        self.create_widgets()

    def create_widgets(self):
        style_button_nav = ttk.Style()
        style_button_nav.configure('TButton', font=('Helvetica', 8), padding=6, background='#000000', foreground='black')
        
        # <----------------- GENERATE NAV FRAME ----------------->
        self.nav_frame = ttk.Frame(self, height=40, style="nav_style.TFrame")
        self.nav_frame.pack(side=tk.TOP, fill=tk.X)

        # <----------------- GENERATE CONTENT FRAME ----------------->
        self.content_frame = ttk.Frame(self, style="general_style.TFrame")
        self.content_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        # <----------------- GENERATE NAV CONTENT ----------------->

        self.btn_display_all = ttk.Button(self.nav_frame, text="Display All", command=self.display_all, style='TButton')
        self.btn_display_all.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.btn_add_item = ttk.Button(self.nav_frame, text="Add Item", command=self.add_item, style='TButton')
        self.btn_add_item.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.btn_remove_item = ttk.Button(self.nav_frame, text="Remove Item", command=self.remove_item, style='TButton')
        self.btn_remove_item.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.btn_search_item = ttk.Button(self.nav_frame, text="Search Item", command=self.search_item, style='TButton')
        self.btn_search_item.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.btn_update_item = ttk.Button(self.nav_frame, text="Update Item", command=self.update_item, style='TButton')
        self.btn_update_item.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.display_all() # Jika dibutuhkan bisa di generate langsung isi dari gudang
        
    def clear_content_frame(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    # def home(self):

    def display_all(self):
        self.clear_content_frame()
        
        # <----------------- GENERATE NAV SORT ----------------->
        self.nav_frame_sort = ttk.Frame(self.content_frame, height=40, style="general_style.TFrame")
        self.nav_frame_sort.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.btn_sort_price = ttk.Button(self.nav_frame_sort, text="Sort by Price", command=self.sort_by_price, style='TButton')
        self.btn_sort_price.pack(side=tk.RIGHT, padx=5, pady=5)
        
        self.btn_sort_quantity = ttk.Button(self.nav_frame_sort, text="Sort by Quantity", command=self.sort_by_quantity, style='TButton')
        self.btn_sort_quantity.pack(side=tk.RIGHT, padx=5, pady=5)
        
        self.btn_sort_id = ttk.Button(self.nav_frame_sort, text="Sort by ID", command=self.sort_by_id, style='TButton')
        self.btn_sort_id.pack(side=tk.RIGHT, padx=5, pady=5)      
        
        self.canvas_content_frame = tk.Canvas(self.content_frame, bg="#1064a3")
        self.canvas_content_frame.pack(side=tk.LEFT, fill="both", expand=True, padx=10, pady=10)
        
        self.canvas_content_frame_scrolbar = ttk.Scrollbar(self.content_frame, orient=tk.VERTICAL, command=self.canvas_content_frame.yview)
        self.canvas_content_frame_scrolbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.canvas_content_frame.configure(yscrollcommand=self.canvas_content_frame_scrolbar.set)
        self.canvas_content_frame.bind("<Configure>", lambda e : self.canvas_content_frame.configure(scrollregion=self.canvas_content_frame.bbox("all")))
        
        self.box_detail_item = ttk.Frame(self.canvas_content_frame, height=30, style="general_style.TFrame")
        
        self.canvas_content_frame.create_window((100,20), window=self.box_detail_item, anchor=tk.NW)
        
        products = self.gudang.getAllproduct()

        for product in products:
            self.box_info = ttk.Label(self.box_detail_item,style="list_items.TLabel" ,text=f"    Id Barang : {product[0]}\t\t\t\t Nama Barang : {product[1]}\t\t\t\t Jumlah Barang : {product[2]}\t\t\t\t Harga Barang : {product[3]}    ").pack(side=tk.TOP, pady=6, fill=tk.BOTH)     
        
    def add_item(self):
        self.clear_content_frame()
        
        # <---------------- FORM NAME ---------------->
        frame_name = ttk.Frame(self.content_frame, style="form_style.TFrame")
        frame_name.pack(side=tk.TOP, padx=100, pady=25, fill=tk.X)
        
        label_name = ttk.Label(frame_name, text="Name", style="form_style.TLabel")
        label_name.pack(padx=10, pady=10, side=tk.LEFT, expand=True)
        
        name_entry = ttk.Entry(frame_name)
        name_entry.pack(padx=10, pady=10, side=tk.LEFT, expand=True, fill="x")
        
        # <---------------- FORM QUANTITY ---------------->
        frame_quantity = ttk.Frame(self.content_frame, style="form_style.TFrame")
        frame_quantity.pack(side=tk.TOP, padx=100, pady=25, fill=tk.X)
        
        label_quantity = ttk.Label(frame_quantity, text="Quantity", style="form_style.TLabel")
        label_quantity.pack(padx=10, pady=10, side=tk.LEFT, expand=True)
        
        quantity_entry = ttk.Entry(frame_quantity)
        quantity_entry.pack(padx=10, pady=10, side=tk.LEFT, expand=True, fill="x")
        
        # <---------------- FORM PRICE ---------------->
        frame_price = ttk.Frame(self.content_frame, style="form_style.TFrame")
        frame_price.pack(side=tk.TOP, padx=100, pady=25, fill=tk.X)
        
        label_price = ttk.Label(frame_price, text="Price", style="form_style.TLabel")
        label_price.pack(padx=10, pady=10, side=tk.LEFT, expand=True)
        
        price_entry = ttk.Entry(frame_price)
        price_entry.pack(padx=10, pady=10, side=tk.LEFT, expand=True, fill="x")
        
        def add_item_to_gudang():
            name = name_entry.get()
            quantity_str = quantity_entry.get()
            price_str = price_entry.get()
            
            if name and quantity_str.isdigit() and price_str.isdigit():
                quantity = int(quantity_str)
                price = int(price_str)
                self.gudang.addItem(name, quantity, price)
                messagebox.showinfo("Sukses", "Data Berhasil Ditambahkan")
                self.display_all()
            else:
                messagebox.showerror("Input Error", "Please enter valid name, quantity, and price.")
        
        # <---------------- BUTTON ADD ---------------->
        add_button = ttk.Button(self.content_frame, text="ADD", command=add_item_to_gudang, style="form_style.TButton")
        add_button.pack(padx=100, pady=20, fill=tk.X)

    def remove_item(self):
        self.clear_content_frame()
                
        # <---------------- FORM NAME ---------------->
        frame_name = ttk.Frame(self.content_frame, style="form_style.TFrame")
        frame_name.pack(side=tk.TOP, padx=100, pady=25, fill=tk.X)
        
        label_name = ttk.Label(frame_name, text="Masukan Nama Yang Ingin di Hapus!", style="form_style.TLabel")
        label_name.pack(padx=10, pady=10, side=tk.LEFT, expand=True)
        
        name_entry = ttk.Entry(frame_name)
        name_entry.pack(padx=10, pady=10, side=tk.LEFT, expand=True, fill="x")

        
        def remove_item_in_gudang():
            name = name_entry.get()  # Get the name when the button is clicked
            if self.gudang.searchByName(name):
                self.gudang.removeItemByName(name)
                messagebox.showwarning("Sukses", "Data Berhasil Dihapus")
                self.display_all()
            else:
                messagebox.showerror("Error", "Nama tidak ditemukan")
        
        delete_button = ttk.Button(self.content_frame, text="DELETE", command=remove_item_in_gudang, style="form_style.TButton")
        delete_button.pack(padx=100, pady=20, fill=tk.X)

    def search_item(self):
        self.clear_content_frame()

        # <---------------- FORM NAME ---------------->
        frame_name = ttk.Frame(self.content_frame, style="form_style.TFrame")
        frame_name.pack(side=tk.TOP, padx=100, pady=25, fill=tk.X)
        
        label_name = ttk.Label(frame_name, text="Masukan Nama Yang Ingin Anda Cari!", style="form_style.TLabel")
        label_name.pack(padx=10, pady=10, side=tk.LEFT, expand=True)
        
        name_entry = ttk.Entry(frame_name)
        name_entry.pack(padx=10, pady=10, side=tk.LEFT, expand=True, fill="x")

        def display_item_in_gudang():
            name = name_entry.get().strip()
            items = self.gudang.searchByName(name)
            
            if items:
                messagebox.showinfo("Sukses", "Data ditemukan")
                for item in items: # dapet nya objek
                    frame_info = ttk.Frame(self.content_frame, style="list_items.TLabel")
                    frame_info.pack(side=tk.TOP, padx=20, pady=20)
                    
                    id = ttk.Label(frame_info, style="list_items.TLabel", text=f"Id Barang : {item.id}")
                    id.pack(side=tk.LEFT, padx=20, pady=20, fill=tk.X, expand=True)
                    
                    nama = ttk.Label(frame_info, style="list_items.TLabel", text=f"Nama Barang : {item.name}")
                    nama.pack(side=tk.LEFT, padx=20, pady=20, fill=tk.X, expand=True)
                    
                    quantity = ttk.Label(frame_info, style="list_items.TLabel", text=f"Quantity Barang : {item.quantity}")
                    quantity.pack(side=tk.LEFT, padx=20, pady=20, fill=tk.X, expand=True)
                    
                    price = ttk.Label(frame_info, style="list_items.TLabel", text=f"Price Barang : {item.price}")
                    price.pack(side=tk.LEFT, padx=20, pady=20, fill=tk.X, expand=True)
                    
                    
                    
                    # ttk.Label(self.content_frame, style="list_items.TLabel", text=f"           Id Barang : {item.id}\t\t Nama Barang : {item.name}\t              Jumlah Barang : {item.quantity}\t              Harga Barang : {item.price}    ").pack(side=tk.TOP, padx=100, pady=25, fill=tk.X)
            else:
                messagebox.showerror("Error", "Nama tidak ditemukan")
        
        search_button = ttk.Button(self.content_frame, text="FIND", command=display_item_in_gudang, style="general_style.TButton")
        search_button.pack(padx=100, pady=20, fill=tk.X)
        
    def update_item(self):
        self.clear_content_frame()

        # <---------------- FORM ID ---------------->
        frame_id = ttk.Frame(self.content_frame, style="form_style.TFrame")
        frame_id.pack(side=tk.TOP, padx=100, pady=25, fill=tk.X)
        
        label_id = ttk.Label(frame_id, text="Masukkan ID yang ingin diperbarui:", style="form_style.TLabel")
        label_id.pack(padx=10, pady=10, side=tk.LEFT, expand=True)
        
        id_entry = ttk.Entry(frame_id)
        id_entry.pack(padx=10, pady=10, side=tk.LEFT, expand=True, fill="x")
        
        # <---------------- FORM NAME ---------------->
        frame_name = ttk.Frame(self.content_frame, style="form_style.TFrame")
        frame_name.pack(side=tk.TOP, padx=100, pady=25, fill=tk.X)
        
        label_name = ttk.Label(frame_name, text="Nama baru (kosongkan jika tidak ingin mengubah):", style="form_style.TLabel")
        label_name.pack(padx=10, pady=10, side=tk.LEFT, expand=True)
        
        name_entry = ttk.Entry(frame_name)
        name_entry.pack(padx=10, pady=10, side=tk.LEFT, expand=True, fill="x")
        
        # <---------------- FORM QUANTITY ---------------->
        frame_quantity = ttk.Frame(self.content_frame, style="form_style.TFrame")
        frame_quantity.pack(side=tk.TOP, padx=100, pady=25, fill=tk.X)
        
        label_quantity = ttk.Label(frame_quantity, text="Jumlah baru (kosongkan jika tidak ingin mengubah):", style="form_style.TLabel")
        label_quantity.pack(padx=10, pady=10, side=tk.LEFT, expand=True)
        
        quantity_entry = ttk.Entry(frame_quantity)
        quantity_entry.pack(padx=10, pady=10, side=tk.LEFT, expand=True, fill="x")
        
        # <---------------- FORM PRICE ---------------->
        frame_price = ttk.Frame(self.content_frame, style="form_style.TFrame")
        frame_price.pack(side=tk.TOP, padx=100, pady=25, fill=tk.X)
        
        label_price = ttk.Label(frame_price, text="Harga baru (kosongkan jika tidak ingin mengubah):", style="form_style.TLabel")
        label_price.pack(padx=10, pady=10, side=tk.LEFT, expand=True)
        
        price_entry = ttk.Entry(frame_price)
        price_entry.pack(padx=10, pady=10, side=tk.LEFT, expand=True, fill="x")
        

        def update_item_in_gudang():
            item_id = id_entry.get().strip()
            new_name = name_entry.get().strip()
            new_quantity_str = quantity_entry.get().strip()
            new_price_str = price_entry.get().strip()

            item = self.gudang.SearchItemById(item_id)
            if item:
                if new_name:
                    self.gudang.setNameItem(item_id, new_name)
                if new_quantity_str.isdigit():
                    new_quantity = int(new_quantity_str)
                    self.gudang.setQuantityItem(item_id, new_quantity)
                if new_price_str.isdigit():
                    new_price = int(new_price_str)
                    self.gudang.setPriceItem(item_id, new_price)
                messagebox.showinfo("Sukses", "Data berhasil diperbarui")
                self.display_all()
            else:
                messagebox.showerror("Error", "ID tidak ditemukan")

        update_button = ttk.Button(self.content_frame, text="UPDATE", command=update_item_in_gudang, style="general_style.TButton")
        update_button.pack(padx=100, pady=20, fill=tk.X)

    def sort_by_price(self):
        self.clear_content_frame()
        self.gudang.sortByPrice()
        self.display_all()
        
    def sort_by_quantity(self):
        self.clear_content_frame()
        self.gudang.sortByQuantity()
        self.display_all()
        
    def sort_by_id(self):
        self.clear_content_frame()
        self.gudang.sortById()
        self.display_all()

# <---------------------- Main program ---------------------->

gudang = Gudang()
app = GudangApp(gudang)
app.mainloop()

# <---------------------- End Main program ---------------------->