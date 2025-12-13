# Playgrounded

## O aplikaciji
- Playgrounded je mini RPG desktop aplikacija (Tkinter) za kreiranje likova s fiksnim atributima po klasi, sustavom **skills** i **items** te spremanjem/učitavanjem podataka u XML formatu.
- Najrecentnija verzija: 1.1.3

Aplikacija je zamišljena kao jednostavan “character creator” gdje korisnik:
- kreira lika (Warrior / Mage / Assassin)
- uči class-specific skillove
- dodaje i uklanja iteme iz inventorya
- sprema i učitava pojedinačne likove i kompletno stanje aplikacije

UI Glavnog prozora sa nekoliko primjera kreairanih likova<img width="2559" height="1390" alt="image" src="https://github.com/user-attachments/assets/84050133-c0b9-42a9-a6f3-1da6e5084ae8" />

## Ključne funkcionalnosti
- Kreiranje lika (Warrior, Mage, Assassin) s fiksnim atributima
- Trenutno dostupni skillovi po liku:
  - Warrior: Sigma Strike, Udarčina, Blok
  - Mage: Fireball, Diddy Spell, Rulers Hand
  - Assassin: Flashstep, Backstab, Mutilate
- Items: Sword, Shield, Potion, Bow, Zenith, Pickaxe, AK-47
- Detaljni prikaz odabranog lika (atributi + skills + inventory)
- Spremanje/učitavanje:
  - spremanje odabranog lika u XML datoteku (npr. `ImeLika.xml`)
  - spremanje/učitavanje stanja aplikacije u `app_state.xml`

## Pokretanje
- Kloniraj repozitorij:
  - `git clone <repo-url>`
- Uđi u direktorij projekta:
  - `cd <repo-folder>`
- Pokreni aplikaciju:
  - `python main.py`

> Ako se tvoja datoteka zove drugačije (npr. `playgrounded.py`), pokreni:
> - `python playgrounded.py`

## Spremanje i učitavanje (XML)
Aplikacija koristi XML za trajnost podataka.

- Spremanje odabranog lika:
  - Iz menija **Datoteka → Spremi odabranog lika...**
- Učitavanje lika:
  - Iz menija **Datoteka → Učitaj lika iz datoteke...**
- Spremanje cijelog stanja:
  - Iz menija **Datoteka → Spremi stanje aplikacije**
- Učitavanje cijelog stanja:
  - Iz menija **Datoteka → Učitaj stanje aplikacije**
 
## Tehnologije
- Python 3 (Logika)
- Tkinter (GUI)
- XML (Spremanje)

## Autor
- Antonio Hrelja i GPT5 (goat)
