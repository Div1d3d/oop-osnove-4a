#Definicija osnove klase Zaposlenik i konstruktora
class Zaposlenik:
    def __init__(self, ime, prezime, placa):
        self.ime = ime
        self.prezime = prezime
        self.placa = placa

    def prikazi_info(self):
        print(f"{self.ime} {self.prezime} ima plaću: {self.placa} EUR")

class Programer(Zaposlenik):
    def __init__(self, ime, prezime, placa, pJezici):
        #Pozivamo konstruktore parent klase
        super().__init__(ime, prezime, placa)
        #Novi atribut specifičan za programere
        self.pJezici = pJezici

    def prikazi_info(self):
        #Pozivamo metode parent klase
        super().prikazi_info()
        #Dodatan info o programeru
        print(f"Zna ove programske jezike: {', '.join(self.pJezici)}")

class Menadzer(Zaposlenik):
    def __init__(self, ime, prezime, placa, tim):
        # Pozivamo konstruktore parent klase
        super().__init__(ime, prezime, placa)
        #Novi atribut - lista članova tima
        self.tim = tim

    def prikazi_info(self):
        super().prikazi_info()
        # Ispis članova tima
        print("Tim:", ", ".join(self.tim))

    def dodaj_clana(self, novi_clan):
        #Dodaje novog člana u listu tim
        self.tim.append(novi_clan)
        print(f"{novi_clan} je dodan u tim menadžera {self.ime} {self.prezime}.")

if __name__ == "__main__":
    z1 = Zaposlenik("Endi", "Čekić", 2500)
    p1 = Programer("Zvonimir", "Fadiga", 6767, ["Python", "JavaScript"])
    m1 = Menadzer("Antonio", "Hrelja", 25000, ["Endi Čekić", "Zvonimir Fadiga"])

    print("Zaposlenik info:")
    z1.prikazi_info()

    print("Programer info:")
    p1.prikazi_info()

    print("Menadzer info:")
    m1.prikazi_info()

    print("Dodavanje novog člana u tim:")
    m1.dodaj_clana("Lovro Šverko")

    print("Menadzer info nakon dodavanja novog člana:")
    m1.prikazi_info()