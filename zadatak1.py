# Definicija klase
class Knjiga:
    #Definiranje konstruktora
    def __init__(self, naslov, autor, godina_izdanja):
        #Definiranje svojstava ili atributa
        self.naslov = naslov
        self.autor = autor
        self.godina_izdanja = godina_izdanja

b1 = Knjiga("Hamlet", "William Shakespeare", 1603)
b2 = Knjiga("Gospodar prstenova", "J.R.R. Tolkien", 1954)

print(f"Naslov: {b1.naslov}, Autor: {b1.autor}, Godina izdavanja: {b1.godina_izdanja}")
