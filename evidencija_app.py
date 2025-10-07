import tkinter as tk

class Ucenik:
    def __init__(self, ime, prezime, razred):
        self.ime = ime
        self.prezime = prezime
        self.razred = razred

    def __str__(self):
        return f"Učenik: {self.ime} {self.prezime} iz razreda {self.razred}"

class EvidencijaApp:
    def __init__(self, root):
# --- Struktura prozora ---
        root.title("Evidencija učenika")
        root.geometry("500x400")

# --- Konfiguracija responzivnosti ---
# Glavni prozor: daj "težinu" stupcu 0 i redu 1 (gdje je lista)
        root.columnconfigure(0, weight=1)
        root.rowconfigure(1, weight=1)

# --- Okviri (Frames) za organizaciju ---
# Okvir za formu (unos)
        unos_frame = tk.Frame(root, padx=10, pady=10)
        unos_frame.grid(row=0, column=0, sticky="EW") # Rasteže se horizontalno

# Okvir za prikaz (lista)
        prikaz_frame = tk.Frame(root, padx=10, pady=10)
        prikaz_frame.grid(row=1, column=0, sticky="NSEW") # Rasteže se u svim smjerovima

# Responzivnost unutar okvira za prikaz
        prikaz_frame.columnconfigure(0, weight=1)
        prikaz_frame.rowconfigure(0, weight=1)

# --- Widgeti za unos ---
# Ime
        tk.Label(unos_frame, text="Ime:").grid(row=0, column=0, padx=5, pady=5, sticky="W")
        ime_entry = tk.Entry(unos_frame)
        ime_entry.grid(row=0, column=1, padx=30, pady=5, sticky="EW")

# Prezime
        tk.Label(unos_frame, text="Prezime:").grid(row=1, column=0, padx=5, pady=5, sticky="W")
        prezime_entry = tk.Entry(unos_frame)
        prezime_entry.grid(row=1, column=1, padx=30, pady=5, sticky="EW")

# Razred
        tk.Label(unos_frame, text="Razred:").grid(row=2, column=0, padx=5, pady=5, sticky="W")
        razred_entry = tk.Entry(unos_frame)
        razred_entry.grid(row=2, column=1, padx=30, pady=5, sticky="EW")

# Gumbi
        dodaj_gumb = tk.Button(unos_frame, text="Dodaj učenika")
        dodaj_gumb.grid(row=3, column=0, padx=5, pady=10, sticky="W")

        spremi_gumb = tk.Button(unos_frame, text="Spremi izmjene", width=35)
        spremi_gumb.grid(row=3, column=1, padx=30, pady=10, sticky="E")

# --- Widgeti za prikaz (NOVO GRADIVO: Listbox) ---
        listbox = tk.Listbox(prikaz_frame)
        listbox.grid(row=0, column=0, sticky="NSEW")

# Scrollbar za listbox
        scrollbar = tk.Scrollbar(prikaz_frame, orient="vertical", command=listbox.yview)
        scrollbar.grid(row=0, column=1, sticky="NS")
        listbox.config(yscrollcommand=scrollbar.set)
