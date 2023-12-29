import tkinter as tk
import sys
from tkinter import messagebox
from tkinter import ttk
from tkinter import simpledialog

# Set the Cambria font family
cambria_font = ("Cambria", 12)

# Definisikan kelas Lg untuk menyimpan informasi login
class Lg:
    def __init__(self, username="", password=""):
        self.username = username
        self.password = password

# Fungsi untuk membuat akun baru
def buatakun():
    # Buat jendela baru untuk sign-up
    signup_window = tk.Toplevel(root)
    signup_window.title("Sign Up")
    signup_window.geometry("300x150")

    # Label dan entry untuk username
    username_label = ttk.Label(signup_window, text="Username:", font=cambria_font)
    username_label.grid(row=0, column=0, sticky=tk.W)
    username_entry = ttk.Entry(signup_window)
    username_entry.grid(row=0, column=1) 

    # Label dan entry untuk password
    password_label = ttk.Label(signup_window, text="Password:", font=cambria_font)
    password_label.grid(row=1, column=0, sticky=tk.W)
    password_entry = ttk.Entry(signup_window, show="*")
    password_entry.grid(row=1, column=1)

    # Tombol untuk menyimpan data sign-up
    signup_button = ttk.Button(signup_window, text="Sign Up", command=lambda: save_signup(username_entry.get(), password_entry.get(), signup_window))
    signup_button.grid(row=2, column=1, pady=10)

# Fungsi untuk menyimpan data sign-up ke dalam file
def save_signup(username, password, signup_window):
    with open('login.txt', 'a') as file:
        file.write(f"{username},{password}\n")
    print("\nAkun berhasil dibuat!")
    signup_window.destroy()

# Fungsi untuk memeriksa login
def check_login():
    lg = loginakun()
    if lg is not None:
        # Jika login berhasil, tampilkan pesan sukses dan arahkan ke file lain
        messagebox.showinfo("Login Success", "Welcome, " + lg.username + "!")
        root.destroy()

# Fungsi untuk melakukan login
def loginakun():
    lg = None
    with open('login.txt', 'r') as file:
        # Minta input username dan password dari pengguna
        username = simpledialog.askstring("Input", "Masukkan username:")
        password = simpledialog.askstring("Input", "Masukkan password:")
        # Loop melalui file untuk mencocokkan dengan data yang tersimpan
        for line in file:
            # Memastikan bahwa line tidak kosong dan memiliki dua nilai yang dapat dipisahkan oleh koma
            if ',' in line:
                stored_username, stored_password = line.strip().split(',', 1)
                if username == stored_username and password == stored_password:
                    lg = Lg(username, password)
                    print("\nLogin berhasil!")
                    break

    if lg is None:
        print("\nUsername atau password salah!")

    return lg

# Fungsi untuk menutup aplikasi
def close_application():
    confirm = messagebox.askokcancel("Konfirmasi", "Apakah Anda yakin ingin keluar dari aplikasi?")
    if confirm:
        sys.exit()
        
# Membuat instance object tkinter
root = tk.Tk()

# Menambahkan judul pada GUI
root.title("Aplikasi Pencatatan Deadline Tugas")

# Menambahkan judul pada GUI
root.title("Login")

# Membuat frame untuk input login
frame_login = tk.Frame(root, padx=20, pady=20)
frame_login.pack()

# Label for the application title
app_title_label = ttk.Label(frame_login, text="Aplikasi Pencatatan Deadline Tugas", font=cambria_font)
app_title_label.grid(row=0, column=0, columnspan=2, pady=10)

# Menambahkan tombol login
login_button = tk.Button(frame_login, text="Login", command=check_login, font=cambria_font)
login_button.grid(row=2, column=0, padx=5, pady=10)

# Menambahkan tombol sign up
signup_button = tk.Button(frame_login, text="Sign Up", command=buatakun, font=cambria_font)
signup_button.grid(row=2, column=1, padx=5, pady=10)

# Menutup aplikasi saat tombol close pada window login ditekan
def disable_event():
    close_application()

root.protocol("WM_DELETE_WINDOW", disable_event)

# Menjalankan event loop tkinter
root.mainloop()

# Define data_array globally
data_array = [
    {"tanggal": "18 Desember 2023", "keterangan": "FP Basdat"},
    {"tanggal": "18 Desember 2023", "keterangan": "FP DAA"},
    {"tanggal": "18 Desember 2023", "keterangan": "FP RPL"},
    {"tanggal": "18 Desember 2023", "keterangan": "FP TBO"},
    {"tanggal": "19 Desember 2023", "keterangan": "FP PBO"},
    {"tanggal": "21 Desember 2023", "keterangan": "FP KDJK"},
    {"tanggal": "21 Desember 2023", "keterangan": "TEST LISAN BASDAT"},
    {"tanggal": "22 Desember 2023", "keterangan": "TEST KDJK"},
    {"tanggal": "28 Desember 2023", "keterangan": "TEST LISAN TBO DAN REVISI"},
    {"tanggal": "21 Desember 2023", "keterangan": "REVISI IMK"}
]

def boyer_moore_horspool_search(pattern, text):
    m = len(pattern)
    n = len(text)
    pattern = pattern.lower()
    text = text.lower()
    last_occurrence = {pattern[i]: i for i in range(m)}
    i = m - 1  # index in pattern
    j = m - 1  # index in text

    while j < n:
        if pattern[i] == text[j]:
            if i == 0:
                return j  # pattern found
            else:
                i -= 1
                j -= 1
        else:
            last_occ = last_occurrence.get(text[j], -1)
            j = j + m - min(i, 1 + last_occ)
            i = m - 1

    return None

def search_phrase_in_text(phrase, text):
    return phrase.lower() in text.lower()

def boyer_moore_horspool_search_name(name, data_array):
    # Convert the query to lowercase
    name = name.lower()

    for i, item in enumerate(data_array):
        keterangan_lower = item["keterangan"].lower()
        # Search for the entire query phrase in keterangan_lower using the new function
        if search_phrase_in_text(name, keterangan_lower):
            return i  # Return the index instead of the date

    return None

# Fungsi untuk menampilkan hasil pencarian
def show_result(result_index):
    if result_index is not None:
        message = f"Tanggal deadline {data_array[result_index]['tanggal']}"
    else:
        message = "Agenda Tugas yang Anda cari tidak ditemukan."
    result_label.configure(text=message)


# Fungsi untuk menambah data pada array dan memperbarui tampilan tabel
def add_data():
    keterangan = keterangan_entry.get() 
    tanggal = tanggal_entry.get()  # No conversion to lowercase for dates
    data_array.append({"tanggal": tanggal, "keterangan": keterangan})
    update_table()

# Fungsi untuk menghapus data dari array dan memperbarui tampilan tabel
def delete_data():
    item = table.selection()[0]
    index = int(table.index(item))
    del data_array[index]
    update_table()

# Fungsi untuk memperbarui tampilan tabel
def update_table():
    table.delete(*table.get_children())
    for i, data in enumerate(data_array):
        table.insert("", "end", text=i+1, values=(data["keterangan"], data["tanggal"], i))  

# Fungsi untuk mengedit data pada array dan memperbarui tampilan tabel
def edit_data(index):
    # Tampilkan jendela dialog untuk mengedit data
    edit_window = tk.Toplevel(root)
    edit_window.title("Edit Data")
    edit_window.geometry("300x150")  # Set width and height to match the "View Data" window

    # Label dan entry untuk input keterangan
    keterangan_label = ttk.Label(edit_window, text="Agenda Tugas:")
    keterangan_label.grid(row=0, column=0, sticky=tk.W)
    keterangan_entry = ttk.Entry(edit_window)
    keterangan_entry.insert(0, data_array[index]["keterangan"])
    keterangan_entry.grid(row=0, column=1, padx=5, pady=5)

    # Label dan entry untuk input tanggal
    tanggal_label = ttk.Label(edit_window, text="Tanggal deadline:")
    tanggal_label.grid(row=1, column=0, sticky=tk.W)
    tanggal_entry = ttk.Entry(edit_window)
    tanggal_entry.insert(0, data_array[index]["tanggal"])
    tanggal_entry.grid(row=1, column=1, padx=5, pady=5)

    # Tombol untuk menyimpan perubahan
    save_button = ttk.Button(edit_window, text="Save", command=lambda: save_changes(index, keterangan_entry.get(), tanggal_entry.get(), edit_window))
    save_button.grid(row=2, column=1, pady=10)

# Fungsi untuk menyimpan perubahan ke dalam data_array dan memperbarui tampilan tabel
def save_changes(index, keterangan, tanggal, edit_window):
    data_array[index]["keterangan"] = keterangan
    data_array[index]["tanggal"] = tanggal
    edit_window.destroy()  # Tutup jendela edit
    update_table()  # Perbarui tampilan tabel

# Membuat instance object tkinter
root = tk.Tk()

# Menambahkan judul pada GUI
root.title("LIST DEADLINE TUGAS")

# Membuat frame untuk tabel dan input
frame_table = ttk.Frame(root, padding="20")
frame_table.pack(fill="both", expand=True)
frame_input = ttk.Frame(root, padding="10")
frame_input.pack(fill="x", expand=True)
frame_button = ttk.Frame(root, padding="10")
frame_button.pack(fill="x", expand=True)

# Membuat tabel untuk menampilkan data array
table = ttk.Treeview(frame_table, columns=("col1"))
table.heading("#0", text="No.")
table.heading("col1", text="Keterangan")

# Menampilkan tabel ke dalam GUI
table.pack(fill="both", expand=True)

# Menambahkan input untuk menambah data
keterangan_label = ttk.Label(frame_input, text="Agenda Tugas :")
keterangan_label.pack(side="left")
keterangan_entry = ttk.Entry(frame_input)
keterangan_entry.pack(side="left")
tanggal_label = ttk.Label(frame_input, text="Tanggal deadline:")
tanggal_label.pack(side="left")
tanggal_entry = ttk.Entry(frame_input)
tanggal_entry.pack(side="left")

# Menambahkan tombol untuk menambah dan menghapus data
add_button = ttk.Button(frame_button, text="Tambah Data", command=add_data)
add_button.pack(side="left")
delete_button = ttk.Button(frame_button, text="Hapus Data", command=delete_data)
delete_button.pack(side="left", padx=10)

def edit_selected_data():
    selected_item = table.selection()
    if selected_item:
        index = table.index(selected_item)
        edit_data(index)
    else:
        messagebox.showinfo("Info", "Pilih data yang akan diedit.")
        
# Menambahkan tombol "Edit Data"
edit_button = ttk.Button(frame_button, text="Edit Data", command=edit_selected_data)
edit_button.pack(side="left", padx=10)

def view_selected_data():
    selected_item = table.selection()
    if selected_item:
        index = table.index(selected_item)
        view_data(index)
    else:
        messagebox.showinfo("Info", "Pilih data yang akan dilihat.")

def view_data(index):
    # Tampilkan jendela dialog untuk melihat data
    view_window = tk.Toplevel(root)
    view_window.title("Lihat Data")
    view_window.geometry("300x150")  # Set width and height as needed

    # Label untuk menampilkan keterangan
    keterangan_label = ttk.Label(view_window, text="Agenda Tugas:")
    keterangan_label.grid(row=0, column=0, sticky=tk.W)
    keterangan_value = ttk.Label(view_window, text=data_array[index]["keterangan"])
    keterangan_value.grid(row=0, column=1, padx=5, pady=5)

    # Label untuk menampilkan tanggal
    tanggal_label = ttk.Label(view_window, text="Tanggal deadline:")
    tanggal_label.grid(row=1, column=0, sticky=tk.W)
    tanggal_value = ttk.Label(view_window, text=data_array[index]["tanggal"])
    tanggal_value.grid(row=1, column=1, padx=5, pady=5)

# Menambahkan tombol "View Data"
view_button = ttk.Button(frame_button, text="Lihat Data", command=view_selected_data)
view_button.pack(side="left", padx=10)

def search_data():
    result_index = boyer_moore_horspool_search_name(input_entry.get(), data_array)
    show_result(result_index)

# Membuat input label dan button
input_label = ttk.Label(frame_input, text="Cari Agenda :")
input_label.pack(side="left")
input_entry = ttk.Entry(frame_input)
input_entry.pack(side="left")
search_button = ttk.Button(frame_input, text="Cari", command=search_data)
search_button.pack(side="left")

# Menambahkan label untuk menampilkan hasil pencarian
result_label = ttk.Label(root, text="")
result_label.pack()

# Memperbarui tampilan tabel dengan data array
update_table()

# Fungsi untuk menutup aplikasi dengan konfirmasi
def exit_application():
    confirm = messagebox.askokcancel("Konfirmasi", "Apakah Anda yakin ingin keluar dari aplikasi?")
    if confirm:
        root.destroy()
        
# Menambahkan tombol "Exit" dengan konfirmasi
exit_button = ttk.Button(frame_button, text="Exit", command=exit_application)
exit_button.pack(side="left", padx=10)

# Menjalankan GUI
root.mainloop()

# Dibuat oleh :
# Kelompok 1 Kelas C
# I Gede Widnyana 			    (2208561016)
# Ni Made Viona Rara Santhi		(2208561098)