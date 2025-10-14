import tkinter as tk
from tkinter import filedialog, messagebox
import csv
import xml.etree.ElementTree as ET

class Ucenik:
    def __init__(self, ime, prezime, razred):
        self.ime = ime
        self.prezime = prezime
        self.razred = razred

    def __str__(self):
        return f"Učenik: {self.ime} {self.prezime} iz razreda {self.razred}"

class EvidencijaApp:
    def __init__(self, root):
        self.ucenici = []
        self.odabrani_ucenik_index = None

        root.title("Evidencija učenika")
        root.geometry("550x500")

        root.columnconfigure(0, weight=1)
        root.rowconfigure(1, weight=1)

        unos_frame = tk.Frame(root, padx=10, pady=10)
        unos_frame.grid(row=0, column=0, sticky="EW")

        prikaz_frame = tk.Frame(root, padx=10, pady=10)
        prikaz_frame.grid(row=1, column=0, sticky="NSEW")

        prikaz_frame.columnconfigure(0, weight=1)
        prikaz_frame.rowconfigure(0, weight=1)

        tk.Label(unos_frame, text="Ime:").grid(row=0, column=0, padx=5, pady=5, sticky="W")
        self.ime_entry = tk.Entry(unos_frame)
        self.ime_entry.grid(row=0, column=1, padx=30, pady=5, sticky="EW")

        tk.Label(unos_frame, text="Prezime:").grid(row=1, column=0, padx=5, pady=5, sticky="W")
        self.prezime_entry = tk.Entry(unos_frame)
        self.prezime_entry.grid(row=1, column=1, padx=30, pady=5, sticky="EW")

        tk.Label(unos_frame, text="Razred:").grid(row=2, column=0, padx=5, pady=5, sticky="W")
        self.razred_entry = tk.Entry(unos_frame)
        self.razred_entry.grid(row=2, column=1, padx=30, pady=5, sticky="EW")

        dodaj_gumb = tk.Button(unos_frame, text="Dodaj učenika", command=self.dodaj_ucenika)
        dodaj_gumb.grid(row=3, column=0, padx=5, pady=10, sticky="W")

        spremi_gumb = tk.Button(unos_frame, text="Spremi izmjene", width=35, command=self.spremi_izmjene)
        spremi_gumb.grid(row=3, column=1, padx=30, pady=10, sticky="E")

        csv_gumb_spremi = tk.Button(unos_frame, text="Spremi CSV", width=10, command=self.spremi_u_csv)
        csv_gumb_spremi.grid(row=0, column=2, padx=5, pady=5, sticky="W")

        csv_gumb_ucitaj = tk.Button(unos_frame, text="Učitaj CSV", width=10, command=self.ucitaj_iz_csv)
        csv_gumb_ucitaj.grid(row=1, column=2, padx=5, pady=5, sticky="E")

        xml_gumb_spremi = tk.Button(unos_frame, text="Spremi XML", width=10, command=self.spremi_u_xml)
        xml_gumb_spremi.grid(row=2, column=2, padx=5, pady=5, sticky="W")

        xml_gumb_ucitaj = tk.Button(unos_frame, text="Učitaj XML", width=10, command=self.ucitaj_iz_xml)
        xml_gumb_ucitaj.grid(row=3, column=2, padx=5, pady=5, sticky="E")

        self.listbox = tk.Listbox(prikaz_frame)
        self.listbox.grid(row=0, column=0, sticky="NSEW")
        self.listbox.bind("<<ListboxSelect>>", self.odaberi_ucenika)

        scrollbar = tk.Scrollbar(prikaz_frame, orient="vertical", command=self.listbox.yview)
        scrollbar.grid(row=0, column=1, sticky="NS")
        self.listbox.config(yscrollcommand=scrollbar.set)

    def dodaj_ucenika(self):
        ime = self.ime_entry.get()
        prezime = self.prezime_entry.get()
        razred = self.razred_entry.get()

        if ime and prezime and razred:
            ucenik = Ucenik(ime, prezime, razred)
            self.ucenici.append(ucenik)
            self.osvjezi_prikaz()

            self.ime_entry.delete(0, tk.END)
            self.prezime_entry.delete(0, tk.END)
            self.razred_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Alo", "Fali ti nešto ig")

    def osvjezi_prikaz(self):
        self.listbox.delete(0, tk.END)
        for ucenik in self.ucenici:
            self.listbox.insert(tk.END, str(ucenik))

    def odaberi_ucenika(self, event):
        selected_index = self.listbox.curselection()
        if selected_index:
            self.odabrani_ucenik_index = selected_index[0]
            ucenik = self.ucenici[self.odabrani_ucenik_index]

            self.ime_entry.delete(0, tk.END)
            self.ime_entry.insert(0, ucenik.ime)
            self.prezime_entry.delete(0, tk.END)
            self.prezime_entry.insert(0, ucenik.prezime)
            self.razred_entry.delete(0, tk.END)
            self.razred_entry.insert(0, ucenik.razred)

    def spremi_izmjene(self):
        if self.odabrani_ucenik_index is not None:
            ucenik = self.ucenici[self.odabrani_ucenik_index]
            ucenik.ime = self.ime_entry.get()
            ucenik.prezime = self.prezime_entry.get()
            ucenik.razred = self.razred_entry.get()

            self.osvjezi_prikaz()

            self.ime_entry.delete(0, tk.END)
            self.prezime_entry.delete(0, tk.END)
            self.razred_entry.delete(0, tk.END)

            self.odabrani_ucenik_index = None

    def spremi_u_csv(self):
        if not self.ucenici:
            messagebox.showinfo("Cooked si", "Bossman šta spremamo uopće?")
            return

        filepath = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV", "*.csv")])
        if filepath:
            with open(filepath, "w", newline="", encoding="utf-8") as file: #CSV na windowsu je kinda mid i voli dodavat prazne redove, pa sam dodao newline cisto za clearat taj problem
                writer = csv.writer(file)
                writer.writerow(["Ime", "Prezime", "Razred"])
                for ucenik in self.ucenici:
                    writer.writerow([ucenik.ime, ucenik.prezime, ucenik.razred])
            messagebox.showinfo("GG!", "CSV kao cool sigma vodič")

    def ucitaj_iz_csv(self):
        filepath = filedialog.askopenfilename(filetypes=[("CSV", "*.csv")])
        if filepath:
            with open(filepath, "r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                self.ucenici = [Ucenik(row["Ime"], row["Prezime"], row["Razred"]) for row in reader]
            self.osvjezi_prikaz()
            messagebox.showinfo("Eko na", "Torna si podatke")

    def spremi_u_xml(self):
        if not self.ucenici:
            messagebox.showinfo("Cooked si", "Bossman šta spremamo uopće?")
            return

        filepath = filedialog.asksaveasfilename(defaultextension=".xml", filetypes=[("XML datoteke", "*.xml")])
        if filepath:
            root = ET.Element("Ucenici")
            for u in self.ucenici:
                ucenik_el = ET.SubElement(root, "Ucenik")
                ET.SubElement(ucenik_el, "Ime").text = u.ime
                ET.SubElement(ucenik_el, "Prezime").text = u.prezime
                ET.SubElement(ucenik_el, "Razred").text = u.razred

            tree = ET.ElementTree(root)
            tree.write(filepath, encoding="utf-8", xml_declaration=True)
            messagebox.showinfo("Awesome sauce", "XML sigma")

    def ucitaj_iz_xml(self):
        filepath = filedialog.askopenfilename(filetypes=[("XML datoteke", "*.xml")])
        if filepath:
            tree = ET.parse(filepath)
            root = tree.getroot()

            self.ucenici = []
            for u_el in root.findall("Ucenik"):
                ime = u_el.find("Ime").text or ""
                prezime = u_el.find("Prezime").text or ""
                razred = u_el.find("Razred").text or ""
                self.ucenici.append(Ucenik(ime, prezime, razred))

            self.osvjezi_prikaz()
            messagebox.showinfo("Kul", "Najbeskorisniji messagebox oat")


if __name__ == "__main__":
    root = tk.Tk()
    app = EvidencijaApp(root)
    root.mainloop()