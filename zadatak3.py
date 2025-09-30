class Recept:
    #def klase
    def __init__ (self, naziv):
        self.naziv = naziv
        self.sastojci = []

    def dodaj_sastojak(self, sastojak, qty):
        self.sastojci.append({"Naziv": sastojak, "količina": qty})

    def prikaz(self):
        print(f"Recept: {self.naziv}")
        print("Sastojci:")
        for i in self.sastojci:
            print(f"{i["naziv"]}: i["qty"]}")

#def class Kuharica
class Kuharica:
    def __init__ (self, naziv):
        self.naziv = naziv
        self.recepti = []

    def dodaj_recept(self, recept_obj):
        self.recepti.append(recept_obj)

    def find_rec(self, naziv_recepta):
        for recept in self.recepti:
            if recept.naziv.lower() == naziv_recepta.lower():
                recept.prikaz()

# Kreiranje kuharice
moja_kuharica = Kuharica("Moja prva kuharica")

# Kreiranje dva recepta
palacinke = Recept("Palačinke")
juha = Recept("Juha")

# Dodavanje sastojaka u palačinke
palacinke.dodaj_sastojak("Brašno", "200g")
palacinke.dodaj_sastojak("Jaja", "2 kom")
palacinke.dodaj_sastojak("Mlijeko", "300ml")
palacinke.dodaj_sastojak("Sol", "prstohvat")

# Dodavanje sastojaka u juhu
juha.dodaj_sastojak("Mrkva", "2 kom")
juha.dodaj_sastojak("Krumpir", "1 kom")
juha.dodaj_sastojak("Voda", "1l")
juha.dodaj_sastojak("Sol", "po ukusu")

# Dodavanje recepata u kuharicu
moja_kuharica.dodaj_recept(palacinke)
moja_kuharica.dodaj_recept(juha)

# Pronalaženje i prikaz recepta za palačinke
moja_kuharica.pronađi_recept("Palačinke")

#Treba popravit!!!