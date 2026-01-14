import sqlite3


#Inicijalizacija
def inicijalizacija():
    conn = sqlite3.connect("Imenik.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Kontakti (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ime_prezime TEXT NOT NULL,
            broj_mobitela TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


#Novi kontakt
def unesi_kontakt():
    ime_prezime = input("Unesite ime i prezime: ")
    broj_mobitela = input("Unesite broj mobitela: ")

    conn = sqlite3.connect("Imenik.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO Kontakti (ime_prezime, broj_mobitela) VALUES (?, ?)",
        (ime_prezime, broj_mobitela)
    )

    conn.commit()
    conn.close()

    print("Kontakt uspješno dodan!")


#Ispis spremljenih
def ispisi_kontakte():
    conn = sqlite3.connect("Imenik.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Kontakti")
    kontakti = cursor.fetchall()

    conn.close()

    if not kontakti:
        print("Imenik je prazan.")
        return

    print("\nID | Ime i prezime | Broj mobitela")
    print("-" * 40)
    for kontakt in kontakti:
        print(f"{kontakt[0]} | {kontakt[1]} | {kontakt[2]}")


#Brisanje
def obrisi_kontakt():
    id_kontakta = input("Unesite ID kontakta za brisanje: ")

    conn = sqlite3.connect("Imenik.db")
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM Kontakti WHERE id = ?",
        (id_kontakta,)
    )

    conn.commit()
    conn.close()

    print("Kontakt obrisan (ako je postojao).")


#Logika
def main():
    inicijalizacija()

    while True:
        print("\nTELEFONSKI IMENIK")
        print("1. Unos novog kontakta")
        print("2. Ispis svih kontakata")
        print("3. Brisanje kontakta")
        print("4. Izlaz")

        izbor = input("Odaberite opciju (1-4): ")

        if izbor == "1":
            unesi_kontakt()
        elif izbor == "2":
            ispisi_kontakte()
        elif izbor == "3":
            obrisi_kontakt()
        elif izbor == "4":
            print("Izlaz iz programa.")
            break
        else:
            print("Pokušajte ponovno.")


if __name__ == "__main__":

    main()
