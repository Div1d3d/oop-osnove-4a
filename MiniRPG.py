import csv
import os
import tkinter as tk
from tkinter import ttk, messagebox

#Osnovna klasa
class Lik:
    def __init__(self, ime, rasa, klasa, snaga, inteligencija, brzina, hp):
        self.ime = ime
        self.rasa = rasa
        self.klasa = klasa
        self.snaga = snaga
        self.inteligencija = inteligencija
        self.brzina = brzina
        self.hp = hp


class Warrior(Lik):
    def __init__(self, ime, rasa):
        super().__init__(ime, rasa, "Warrior", 8, 5, 5, 200)


class Mage(Lik):
    def __init__(self, ime, rasa):
        super().__init__(ime, rasa, "Mage", 7, 10, 6, 100)


class Assasin(Lik):
    def __init__(self, ime, rasa):
        super().__init__(ime, rasa, "Assasin", 9, 6, 10, 75)


class Admin(Lik):
    def __init__(self, ime, rasa):
        super().__init__(ime, rasa, "Admin", 99, 99, 99, 999)


def stvori_lika(row):
    ime = row.get("ime", "BezImena")
    rasa = row.get("rasa", "Nepoznata")
    klasa = row.get("klasa", "Lik")

    if klasa == "Warrior":
        o = Warrior(ime, rasa)
    elif klasa == "Mage":
        o = Mage(ime, rasa)
    elif klasa == "Assasin":
        o = Assasin(ime, rasa)
    elif klasa == "Admin":
        o = Admin(ime, rasa)
    else:
        o = Lik(ime, rasa, klasa, 5, 5, 5, 100)

    for attr in ("snaga", "inteligencija", "brzina", "hp"):
        try:
            setattr(o, attr, int(row.get(attr, getattr(o, attr))))
        except Exception:
            pass
    return o


#GUI
class RPGKreatorLikova(ttk.Frame):
    CSV_HEADER = ["ime", "rasa", "klasa", "snaga", "inteligencija", "brzina", "hp"]

    def __init__(self, master):
        ttk.Frame.__init__(self, master, padding=10)
        master.title("Mini RPG – Kreiranje likova")
        self.pack(fill="both", expand=True)

        self._likovi = []
        self.csv_path = os.path.join(os.path.dirname(__file__), "likovi.csv")
        self._init_ui()

    def _init_ui(self):
        okvir_unos = ttk.LabelFrame(self, text="Novi lik")
        okvir_unos.pack(fill="x", padx=5, pady=5)

        ttk.Label(okvir_unos, text="Klasa:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.var_klasa = tk.StringVar(value="Warrior")
        self.cb_klasa = ttk.Combobox(
            okvir_unos,
            textvariable=self.var_klasa,
            values=["Warrior", "Mage", "Assasin", "Admin"],
            state="readonly",
            width=20,
        )
        self.cb_klasa.grid(row=0, column=1, sticky="w", padx=5, pady=5)

        ttk.Label(okvir_unos, text="Ime:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.var_ime = tk.StringVar()
        self.ent_ime = ttk.Entry(okvir_unos, textvariable=self.var_ime, width=22)
        self.ent_ime.grid(row=1, column=1, sticky="w", padx=5, pady=5)

        ttk.Label(okvir_unos, text="Rasa:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.var_rasa = tk.StringVar()
        self.ent_rasa = ttk.Entry(okvir_unos, textvariable=self.var_rasa, width=22)
        self.ent_rasa.grid(row=2, column=1, sticky="w", padx=5, pady=5)

        self.btn_kreiraj = ttk.Button(okvir_unos, text="Kreiraj lika", command=self.kreiraj_lika)
        self.btn_kreiraj.grid(row=3, column=0, columnspan=2, sticky="ew", padx=5, pady=(5, 10))

        okvir_glavni = ttk.Frame(self)
        okvir_glavni.pack(fill="both", expand=True, padx=5, pady=5)

        okvir_lista = ttk.LabelFrame(okvir_glavni, text="Kreirani likovi")
        okvir_lista.pack(side="left", fill="both", expand=True, padx=(0, 5))

        self.lb_likovi = tk.Listbox(okvir_lista, height=12)
        self.lb_likovi.pack(fill="both", expand=True, padx=5, pady=5)
        self.lb_likovi.bind("<<ListboxSelect>>", self._on_select)

        okvir_detalji = ttk.LabelFrame(okvir_glavni, text="Detalji lika")
        okvir_detalji.pack(side="right", fill="both", expand=True)

        self.txt_detalji = tk.Text(okvir_detalji, height=12, width=38, state="disabled")
        self.txt_detalji.pack(fill="both", expand=True, padx=5, pady=5)

        okvir_io = ttk.Frame(self)
        okvir_io.pack(fill="x", padx=5, pady=(0, 5))
        ttk.Button(okvir_io, text="Spremi CSV", command=self.spremi_csv).pack(side="left")
        ttk.Button(okvir_io, text="Učitaj CSV", command=self.ucitaj_csv).pack(side="left", padx=5)
        ttk.Button(okvir_io, text="Obriši odabranog", command=self.obrisi_odabranog).pack(side="left", padx=5)

    def kreiraj_lika(self):
        ime = self.var_ime.get().strip()
        rasa = self.var_rasa.get().strip()
        klasa = self.var_klasa.get()

        if not ime:
            messagebox.showwarning("Nedostaje ime", "Unesi ime lika.")
            return
        if not rasa:
            messagebox.showwarning("Nedostaje rasa", "Unesi rasu lika.")
            return

        if klasa == "Warrior":
            lik = Warrior(ime, rasa)
        elif klasa == "Mage":
            lik = Mage(ime, rasa)
        elif klasa == "Assasin":
            lik = Assasin(ime, rasa)
        else:
            lik = Admin(ime, rasa)

        self._likovi.append(lik)
        self._osvjezi_listu()
        self._ocisti_unos()

    def _osvjezi_listu(self):
        self.lb_likovi.delete(0, tk.END)
        for lik in self._likovi:
            self.lb_likovi.insert(tk.END, f"{lik.ime} ({lik.klasa})")

    def _ocisti_unos(self):
        self.var_ime.set("")
        self.var_rasa.set("")
        self.cb_klasa.focus_set()

    def _on_select(self, event=None):
        idxs = self.lb_likovi.curselection()
        if not idxs:
            self._prikazi_detalje(None)
            return
        lik = self._likovi[idxs[0]]
        self._prikazi_detalje(lik)

    def _prikazi_detalje(self, lik):
        self.txt_detalji.configure(state="normal")
        self.txt_detalji.delete("1.0", tk.END)
        if lik is None:
            self.txt_detalji.insert(tk.END, "— Nema odabranog lika —")
        else:
            tekst = (
                f"OSNOVNI DETALJI\n"
                f"Ime: {lik.ime}\n"
                f"Rasa: {lik.rasa}\n"
                f"Klasa: {lik.klasa}\n\n"
                f"ATRIBUTI\n"
                f"Snaga: {lik.snaga}\n"
                f"Inteligencija: {lik.inteligencija}\n"
                f"Brzina: {lik.brzina}\n"
                f"HP: {lik.hp}\n"
            )
            self.txt_detalji.insert(tk.END, tekst)
        self.txt_detalji.configure(state="disabled")

    def obrisi_odabranog(self):
        idxs = self.lb_likovi.curselection()
        if not idxs:
            messagebox.showinfo("Brisanje", "Najprije odaberite lika u listi.")
            return
        idx = idxs[0]
        lik = self._likovi[idx]
        if messagebox.askyesno("Potvrda", f"Trajno brisanje lika '{lik.ime}'?"):
            del self._likovi[idx]
            self._osvjezi_listu()
            self._prikazi_detalje(None)

    #Spremanje (Uzeo sam CSV jer mi je bolji od XML-a za prikazivanje tabličnih podataka)
    def spremi_csv(self):
        if not self._likovi:
            messagebox.showinfo("Spremanje", "Lista je prazna, ništa za spremiti.")
            return
        try:
            with open(self.csv_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=self.CSV_HEADER)
                writer.writeheader()
                for lik in self._likovi:
                    writer.writerow({
                        "ime": lik.ime,
                        "rasa": lik.rasa,
                        "klasa": lik.klasa,
                        "snaga": lik.snaga,
                        "inteligencija": lik.inteligencija,
                        "brzina": lik.brzina,
                        "hp": lik.hp,
                    })
            messagebox.showinfo("Spremljeno", f"Spremljeno u:\n{self.csv_path}")
        except Exception as e:
            messagebox.showerror("Greška pri spremanju", str(e))

    #Učitavanje
    def ucitaj_csv(self):
        if not os.path.exists(self.csv_path):
            messagebox.showinfo("Učitavanje", "Datoteka likovi.csv ne postoji.")
            return
        try:
            likovi = []
            with open(self.csv_path, "r", newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    likovi.append(stvori_lika(row))
            self._likovi = likovi
            self._osvjezi_listu()
            self._prikazi_detalje(None)
            messagebox.showinfo("Učitano", f"Učitano iz {self.csv_path}.")
        except Exception as e:
            messagebox.showerror("Greška pri učitavanju", str(e))

def main():
    root = tk.Tk()
    app = RPGKreatorLikova(root)
    root.mainloop()

if __name__ == "__main__":
    main()