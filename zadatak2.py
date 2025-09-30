class BankovniRacun:
    #def klase
    def __init__(self, ime_vlasnika, broj_racuna):
        #konstruktor
        self.ime_vlasnika = ime_vlasnika
        self.broj_racuna = broj_racuna
        self.stanje = 0.0

    def uplati(self, iznos):
        #metoda za uplatu
        if iznos > 0:
            self.stanje += iznos
            print(f"Uplaćeno: {iznos:.2f} EUR.")
        else:
            print("Iznos za uplatu mora biti pozitivan.")

    def isplati(self, iznos):
        #metoda za isplatu
        if iznos <= 0:
            print("Iznos za isplatu mora biti pozitivan.")
        elif iznos > self.stanje:
            print("Nedovoljno para na računu.")
        else:
            self.stanje -= iznos
            print(f"Isplaćeno: {iznos:.2f} EUR.")

    def info(self):
        #metoda za dobivanje informacija o računu
        print("Informacije o računu")
        print(f"Vlasnik: {self.ime_vlasnika}")
        print(f"Broj računa: {self.broj_racuna}")
        print(f"Stanje: {self.stanje:.2f} EUR")

test_racun = BankovniRacun("Antonio Hrelja", "123")

test_racun.info()
test_racun.uplati(100)
test_racun.isplati(150)
test_racun.isplati(50)
test_racun.info()