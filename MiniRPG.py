"""
1.1.0 Patch
-Nove funkcionalnosti (prema uputama iz datoteke)

1.1.1 Patch
-Rebrandao aplikaciju
-Dodijelio nove nazive itemima/skillovima
-BUGFIX: automatsko deselectanje likova pri odabiru drugog widgeta je stvaralo probleme sa učenjem skillova i dodavanjem itema

1.1.2 Patch
-Vizualno preuredio aplikaciju (paleta boja)

1.1.3 Patch
-Finalna vizualna preuređenja
"""


#Note sebi: iskomentiraj i prouči kod još malo.


import os
import xml.etree.ElementTree as ET
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

# Brendiranje
APP_NAME = "Playgrounded"
APP_VERSION = "1.1.3"
APP_AUTHOR = "Antonio Hrelja i GPT5 (goat)"
APP_TAGLINE = "Mini RPG - Kreiranje lika"

# Paleta
COLOR_BG      = "#0B1220"
COLOR_PANEL   = "#111827"
COLOR_PANEL_2 = "#0F172A"
COLOR_SURFACE = "#1F2937"
COLOR_PRIMARY = "#60A5FA"
COLOR_SECOND  = "#22D3EE"
COLOR_TEXT    = "#E5E7EB"
COLOR_TEXT_MUTED = "#9CA3AF"

HOVER_BG      = "#1E293B"
HOVER_FG      = COLOR_TEXT
SELECT_BG     = "#334155"
SELECT_FG     = COLOR_TEXT
ENTRY_BG      = COLOR_PANEL_2
ENTRY_FG      = COLOR_TEXT
CURSOR_COLOR  = COLOR_SECOND

# Katalog skillova i itema

SKILL_CATALOG = {
    "Warrior": ["Sigma Strike", "Udarčina", "Blok"],
    "Mage":    ["Fireball", "Diddy Spell", "Rulers Hand"],
    "Assassin":["Flashstep", "Backstab", "Mutilate"]
}
ITEM_CATALOG = ["Sword", "Shield", "Potion", "Bow", "Zenith", "Pickaxe", "AK-47"]

# Model
class Skill:
    """Jednostavan model skilla (vještine) identificiran nazivom."""
    def __init__(self, name: str):
        self.name = name

    def to_xml(self) -> ET.Element:
        """Serijalizira skill u <skill name="...">."""
        e = ET.Element("skill")
        e.set("name", self.name)
        return e

    @staticmethod
    def from_xml(elem: ET.Element) -> "Skill":
        """Deserijalizira skill iz <skill> elementa."""
        # Podrška i za staru shemu: atribut "naziv"
        name = elem.get("name") or elem.get("naziv") or "Unknown skill"
        return Skill(name)

    def __str__(self):
        return self.name


class Item:
    """Jednostavan model itema (predmeta) identificiran nazivom."""
    def __init__(self, name: str):
        self.name = name

    def to_xml(self) -> ET.Element:
        """Serijalizira item u <item name="...">."""
        e = ET.Element("item")
        e.set("name", self.name)
        return e

    @staticmethod
    def from_xml(elem: ET.Element) -> "Item":
        """Deserijalizira item iz <item> elementa."""
        name = elem.get("name") or elem.get("naziv") or "Unknown item"
        return Item(name)

    def __str__(self):
        return self.name


class Character:
    """Bazna klasa lika (Lik) s fiksnim atributima po klasi (read-only u UI-ju),
    listom naučenih skills i inventarom items. Implementira i XML (de)serijalizaciju."""

    def __init__(self, name, race, klass, strength, intelligence, speed, hp):
        self.name = name
        self.race = race
        self.klass = klass
        # Fiksni primarni atributi (brojevi); u UI-ju se samo prikazuju
        self.strength = int(strength)
        self.intelligence = int(intelligence)
        self.speed = int(speed)
        self.hp = int(hp)
        # Liste:
        self.learned_skills: list[Skill] = []  # naučeni skills
        self.inventory: list[Item] = []  # items u inventoryu

    # --- skills ---
    def can_learn(self, skill: Skill) -> bool:
        """Provjera smije li lik naučiti skill (prema klasi)."""
        allowed = SKILL_CATALOG.get(self.klass, [])
        return skill.name in allowed

    def learn_skill(self, skill: Skill) -> bool:
        """Pokušaj naučiti skill; True ako uspješno (dozvoljen i nije duplikat)."""
        if not self.can_learn(skill):
            return False
        if any(s.name == skill.name for s in self.learned_skills):
            return False
        self.learned_skills.append(skill)
        return True

    # --- items / inventory ---
    def add_item(self, item: Item):
        """Dodaj item u inventar."""
        self.inventory.append(item)

    def remove_item(self, name: str) -> bool:
        """Ukloni prvi item s odgovarajućim imenom; True ako je uklonjen."""
        for i, it in enumerate(self.inventory):
            if it.name == name:
                del self.inventory[i]
                return True
        return False

    # XML
    def to_xml(self) -> ET.Element:
        """
        Serijalizira cijeli lik:
        <character type="...">
           <name>...</name> <race>...</race> <class>...</class> ...
           <skills> <skill .../> ... </skills>
           <inventory> <item .../> ... </inventory>
        </character>
        """
        e = ET.Element("character")
        e.set("type", self.__class__.__name__)  # Stvarna klasa (Warrior/Mage/Assassin/Character)
        data = {
            "name": self.name,
            "race": self.race,
            "class": self.klass,
            "strength": str(self.strength),
            "intelligence": str(self.intelligence),
            "speed": str(self.speed),
            "hp": str(self.hp),
        }
        for k, v in data.items():
            c = ET.SubElement(e, k)
            c.text = v

        # Skills
        e_sk = ET.SubElement(e, "skills")
        for s in self.learned_skills:
            e_sk.append(s.to_xml())

        # Inventory
        e_inv = ET.SubElement(e, "inventory")
        for it in self.inventory:
            e_inv.append(it.to_xml())

        return e

    @staticmethod
    def from_xml(elem: ET.Element) -> "Character":
        """Deserijalizacija lika."""
        # Dohvati tip klasu
        ctype = elem.get("type") or elem.get("tip") or "Character"

        def get_text(*names, default=""):
            """Vrati tekst prvog pod-čvora koji postoji (po redu imena), inače default."""
            for name in names:
                n = elem.find(name)
                if n is not None and n.text is not None:
                    return n.text
            return default

        # Osnovni atributi
        name = get_text("name", default="Unnamed")
        race = get_text("race", default="Unknown")
        klass = get_text("class", default="Character")
        strength = int(get_text("strength", default="5"))
        intelligence = int(get_text("intelligence", default="5"))
        speed = int(get_text("speed", default="5"))
        hp = int(get_text("hp", default="100"))

        # Instanciraj odgovarajući tip
        if ctype == "Warrior":
            obj = Warrior(name, race)
        elif ctype == "Mage":
            obj = Mage(name, race)
        elif ctype == "Assassin":
            obj = Assassin(name, race)
        else:
            obj = Character(name, race, klass, strength, intelligence, speed, hp)

        skills_root = elem.find("skills")
        if skills_root is not None:
            for s_el in skills_root.findall("skill") + skills_root.findall("vjestina"):
                obj.learned_skills.append(Skill.from_xml(s_el))

        inv_root = elem.find("inventory")
        if inv_root is not None:
            for i_el in inv_root.findall("item") + inv_root.findall("predmet"):
                obj.inventory.append(Item.from_xml(i_el))

        return obj


# Konkretné klase s fiksnim atributima po klasi
class Warrior(Character):
    def __init__(self, name, race):
        super().__init__(name, race, "Warrior", 8, 5, 5, 200)

class Mage(Character):
    def __init__(self, name, race):
        super().__init__(name, race, "Mage", 7, 10, 6, 100)

class Assassin(Character):
    def __init__(self, name, race):
        super().__init__(name, race, "Assassin", 9, 6, 10, 75)


def create_character_by_class(name: str, race: str, klass: str) -> Character:
    """Factory: vrati primjerak klase prema nazivu."""
    if klass == "Warrior":  return Warrior(name, race)
    if klass == "Mage":     return Mage(name, race)
    if klass == "Assassin": return Assassin(name, race)
    return Character(name, race, klass, 5, 5, 5, 100)


# =========================
# GUI
# =========================
class PlaygroundedApp(ttk.Frame):
    """
    Glavni GUI okvir:
    - Dark tema, PG logo, menu (File/Prikaz/Pomoć)
    - Kreiranje lika; lista likova; detalji (read-only atributi)
    - Skills (učenje/brisanje) i Inventory (dodaj/ukloni)
    - XML spremanje/učitavanje (pojedinačni lik / cijelo stanje)
    """
    APP_STATE_FILE = "app_state.xml"

    def __init__(self, master):
        super().__init__(master, padding=10)
        self.master.title(f"{APP_NAME} – {APP_TAGLINE}")
        self.master.configure(bg=COLOR_BG)
        self.pack(fill="both", expand=True)
        self._characters: list[Character] = []  # svi likovi u aplikaciji

        self._init_style()
        self._init_menu()
        self._init_ui()
        self._update_status("Dobrodošli u Playgrounded!")

    # --- Stilovi (dark) ---
    def _init_style(self):
        """Konfigurira ttk stilove za dark temu i bolji kontrast."""
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except:
            pass

        # Global
        style.configure(".", background=COLOR_BG, foreground=COLOR_TEXT)

        # Okviri i naslovi
        style.configure("TFrame", background=COLOR_BG)
        style.configure("TLabelframe", background=COLOR_PANEL, foreground=COLOR_TEXT, borderwidth=0)
        style.configure("TLabelframe.Label", background=COLOR_PANEL, foreground=COLOR_PRIMARY)
        style.configure("TLabel", background=COLOR_BG, foreground=COLOR_TEXT)

        # Gumbi (tamni hover)
        style.configure("TButton", padding=6, background=COLOR_PANEL, foreground=COLOR_TEXT)
        style.map("TButton",
                  background=[("active", HOVER_BG), ("pressed", HOVER_BG)],
                  foreground=[("disabled", COLOR_TEXT_MUTED)])

        style.configure("Accent.TButton", padding=8, background=COLOR_PRIMARY, foreground="#0B1220")
        style.map("Accent.TButton",
                  background=[("active", "#3B82F6"), ("pressed", "#2563EB")],
                  foreground=[("disabled", "#0B1220")])

        # Entry (tamna polja + svijetli tekst, vidljiv kursor)
        style.configure("Dark.TEntry",
                        fieldbackground=ENTRY_BG,
                        foreground=ENTRY_FG,
                        insertcolor=CURSOR_COLOR)
        style.map("Dark.TEntry",
                  fieldbackground=[("!disabled", ENTRY_BG), ("focus", ENTRY_BG), ("readonly", ENTRY_BG)],
                  foreground=[("disabled", COLOR_TEXT_MUTED)])

        # Combobox (tamno polje i strelica)
        style.configure("Dark.TCombobox",
                        fieldbackground=ENTRY_BG,
                        foreground=ENTRY_FG,
                        arrowcolor=ENTRY_FG)
        style.map("Dark.TCombobox",
                  fieldbackground=[("readonly", ENTRY_BG), ("focus", ENTRY_BG), ("active", ENTRY_BG)],
                  foreground=[("disabled", COLOR_TEXT_MUTED)],
                  arrowcolor=[("disabled", COLOR_TEXT_MUTED)])

        # (Za Treeview selekcije ako se doda kasnije)
        style.map("Treeview", background=[("selected", SELECT_BG)], foreground=[("selected", SELECT_FG)])

    # --- Menu (tamni hover) ---
    def _init_menu(self):
        """Kreira menu traku: Datoteka / Prikaz / Pomoć."""
        menubar = tk.Menu(self.master, tearoff=0,
                          bg=COLOR_PANEL, fg=COLOR_TEXT,
                          activebackground=HOVER_BG, activeforeground=HOVER_FG)

        # Datoteka
        m_file = tk.Menu(menubar, tearoff=0,
                         bg=COLOR_PANEL, fg=COLOR_TEXT,
                         activebackground=HOVER_BG, activeforeground=HOVER_FG)
        m_file.add_separator()
        m_file.add_command(label="Spremi stanje aplikacije", command=self._cmd_save_app_state)
        m_file.add_command(label="Učitaj stanje aplikacije", command=self._cmd_load_app_state)
        m_file.add_separator()
        m_file.add_command(label="Spremi odabranog lika...", command=self._cmd_save_character_xml)
        m_file.add_command(label="Učitaj lika iz datoteke...", command=self._cmd_load_character_xml)
        m_file.add_separator()
        m_file.add_command(label="Izlaz", command=self.master.quit)
        menubar.add_cascade(label="Datoteka", menu=m_file)

        # Prikaz
        m_view = tk.Menu(menubar, tearoff=0,
                         bg=COLOR_PANEL, fg=COLOR_TEXT,
                         activebackground=HOVER_BG, activeforeground=HOVER_FG)
        m_view.add_command(label="O klasama", command=self._cmd_about_classes)
        menubar.add_cascade(label="Prikaz", menu=m_view)

        # Pomoć
        m_help = tk.Menu(menubar, tearoff=0,
                         bg=COLOR_PANEL, fg=COLOR_TEXT,
                         activebackground=HOVER_BG, activeforeground=HOVER_FG)
        m_help.add_command(label="O aplikaciji", command=self._cmd_about_app)
        menubar.add_cascade(label="Pomoć", menu=m_help)

        self.master.config(menu=menubar)

    # --- UI layout ---
    def _init_ui(self):
        """Sastavlja layout: header (logo + naslov), form za novi lik, listu, detalje, status."""
        # Header
        header = ttk.Frame(self); header.pack(fill="x", pady=(0, 10))
        logo = tk.Canvas(header, width=56, height=56, bg=COLOR_BG, highlightthickness=0)
        logo.pack(side="left")
        self._draw_logo(logo)
        ttk.Label(header, text=APP_NAME, font=("Segoe UI", 18, "bold"),
                  foreground=COLOR_PRIMARY).pack(anchor="w")
        ttk.Label(header, text=APP_TAGLINE, foreground=COLOR_TEXT_MUTED).pack(anchor="w")

        # Unos novog lika
        lf_new = ttk.LabelFrame(self, text="Novi lik"); lf_new.pack(fill="x", padx=2, pady=4)

        ttk.Label(lf_new, text="Klasa:").grid(row=0, column=0, sticky="w", padx=6, pady=6)
        self.var_class = tk.StringVar(value="Warrior")
        self.cb_class = ttk.Combobox(
            lf_new, textvariable=self.var_class,
            values=["Warrior", "Mage", "Assassin"], state="readonly", width=18,
            style="Dark.TCombobox"
        )
        self.cb_class.grid(row=0, column=1, sticky="w", padx=6, pady=6)

        ttk.Label(lf_new, text="Ime:").grid(row=1, column=0, sticky="w", padx=6, pady=6)
        self.var_name = tk.StringVar()
        ent_name = ttk.Entry(lf_new, textvariable=self.var_name, width=22, style="Dark.TEntry")
        ent_name.grid(row=1, column=1, sticky="w", padx=6, pady=6)

        ttk.Label(lf_new, text="Rasa:").grid(row=2, column=0, sticky="w", padx=6, pady=6)
        self.var_race = tk.StringVar()
        ent_race = ttk.Entry(lf_new, textvariable=self.var_race, width=22, style="Dark.TEntry")
        ent_race.grid(row=2, column=1, sticky="w", padx=6, pady=6)

        ttk.Button(lf_new, text="Kreiraj lika", style="Accent.TButton",
                   command=self.create_character).grid(row=3, column=0, columnspan=2, sticky="ew", padx=6, pady=(8, 10))

        # Glavni sadržaj
        main = ttk.Frame(self); main.pack(fill="both", expand=True)

        # Lista likova
        lf_list = ttk.LabelFrame(main, text="Kreirani likovi")
        lf_list.pack(side="left", fill="both", expand=True, padx=(0,6), pady=4)
        self.lb_characters = tk.Listbox(
            lf_list, height=16, exportselection=False,
            bg=COLOR_PANEL_2, fg=COLOR_TEXT,
            selectbackground=SELECT_BG, selectforeground=SELECT_FG,
            borderwidth=0, highlightthickness=0
        )
        self.lb_characters.pack(fill="both", expand=True, padx=8, pady=8)
        self.lb_characters.bind("<<ListboxSelect>>", self._on_select)

        btns_list = ttk.Frame(lf_list); btns_list.pack(fill="x", padx=8, pady=(0,8))
        ttk.Button(btns_list, text="Obriši odabranog", command=self.delete_selected).pack(side="left")
        ttk.Button(btns_list, text="Spremi odabranog", command=self._cmd_save_character_xml).pack(side="left", padx=8)

        # Detalji lika (read-only atributi + Skills + Inventory)
        lf_details = ttk.LabelFrame(main, text="Detalji lika")
        lf_details.pack(side="right", fill="both", expand=True, padx=(6,0), pady=4)

        # Atributi (READ-ONLY)
        frame_attr = ttk.LabelFrame(lf_details, text="Atributi")
        frame_attr.pack(fill="x", padx=8, pady=8)

        self.lbl_attr_str = ttk.Label(frame_attr, text="Snaga: -")
        self.lbl_attr_int = ttk.Label(frame_attr, text="Inteligencija: -")
        self.lbl_attr_spd = ttk.Label(frame_attr, text="Brzina: -")
        self.lbl_attr_hp  = ttk.Label(frame_attr, text="HP: -")

        self.lbl_attr_str.grid(row=0, column=0, sticky="w", padx=6, pady=4)
        self.lbl_attr_int.grid(row=0, column=1, sticky="w", padx=6, pady=4)
        self.lbl_attr_spd.grid(row=0, column=2, sticky="w", padx=6, pady=4)
        self.lbl_attr_hp.grid(row=0, column=3, sticky="w", padx=6, pady=4)

        # Skills
        frame_skills = ttk.LabelFrame(lf_details, text="Skills")
        frame_skills.pack(fill="both", expand=True, padx=8, pady=8)

        self.lb_skills = tk.Listbox(
            frame_skills, height=6, exportselection=False,
            bg=COLOR_PANEL_2, fg=COLOR_TEXT,
            selectbackground=SELECT_BG, selectforeground=SELECT_FG,
            borderwidth=0, highlightthickness=0
        )
        self.lb_skills.pack(side="left", fill="both", expand=True, padx=8, pady=8)

        side_skill = ttk.Frame(frame_skills); side_skill.pack(side="left", fill="y", padx=8, pady=8)
        ttk.Label(side_skill, text="Dostupni skills za klasu", foreground=COLOR_TEXT_MUTED, background=COLOR_BG)\
            .pack(anchor="w")
        self.var_skill_combo = tk.StringVar()
        self.cb_skill = ttk.Combobox(side_skill, textvariable=self.var_skill_combo,
                                     state="readonly", width=28, style="Dark.TCombobox")
        self.cb_skill.pack(fill="x", pady=6)
        ttk.Button(side_skill, text="Nauči skill", command=self._cmd_learn_skill, style="Accent.TButton").pack(fill="x")
        ttk.Button(side_skill, text="Ukloni odabrani skill", command=self._cmd_remove_skill).pack(fill="x", pady=(6,0))

        # Inventory
        frame_inv = ttk.LabelFrame(lf_details, text="Inventory")
        frame_inv.pack(fill="both", expand=True, padx=8, pady=8)

        self.lb_inventory = tk.Listbox(
            frame_inv, height=6, exportselection=False,
            bg=COLOR_PANEL_2, fg=COLOR_TEXT,
            selectbackground=SELECT_BG, selectforeground=SELECT_FG,
            borderwidth=0, highlightthickness=0
        )
        self.lb_inventory.pack(side="left", fill="both", expand=True, padx=8, pady=8)

        side_inv = ttk.Frame(frame_inv); side_inv.pack(side="left", fill="y", padx=8, pady=8)
        ttk.Label(side_inv, text="Dodaj item", foreground=COLOR_TEXT_MUTED, background=COLOR_BG).pack(anchor="w")
        self.var_item_combo = tk.StringVar()
        self.cb_item = ttk.Combobox(side_inv, textvariable=self.var_item_combo,
                                    state="readonly", values=ITEM_CATALOG, width=28, style="Dark.TCombobox")
        self.cb_item.pack(fill="x", pady=6)
        ttk.Button(side_inv, text="Dodaj item", command=self._cmd_add_item, style="Accent.TButton").pack(fill="x")
        ttk.Button(side_inv, text="Ukloni odabrani item", command=self._cmd_remove_item).pack(fill="x", pady=(6,0))

        # Statusna traka
        self.var_status = tk.StringVar()
        status = tk.Label(self, textvariable=self.var_status, anchor="w",
                          bg=COLOR_SURFACE, fg=COLOR_TEXT, padx=8)
        status.pack(fill="x", side="bottom", pady=(8, 0))

    # --- Logo (PG) ---
    def _draw_logo(self, c: tk.Canvas):
        """Crta minimalistički PG logo (krug + ispunjeni krug + slova PG)."""
        c.create_oval(2, 2, 54, 54, fill=COLOR_PANEL_2, outline=COLOR_SECOND, width=2)
        c.create_oval(8, 8, 48, 48, fill=COLOR_PRIMARY, outline="", width=0)
        c.create_text(28, 28, text="PG", fill="#0B1220", font=("Segoe UI", 16, "bold"))

    # --- helpers ---
    def _update_status(self, text: str):
        """Postavi poruku u statusnoj traci."""
        self.var_status.set(text)

    def _refresh_list(self):
        """Osvježi prikaz liste likova."""
        self.lb_characters.delete(0, tk.END)
        for ch in self._characters:
            self.lb_characters.insert(tk.END, f"{ch.name} ({ch.klass})")
        self._update_status(f"Likova: {len(self._characters)}")

    def _get_selected_character(self) -> Character | None:
        """Vrati trenutno odabranog lika (ili None ako nema selekcije)."""
        idxs = self.lb_characters.curselection()
        return self._characters[idxs[0]] if idxs else None

    # --- callbacks / poslovna logika GUI-ja ---
    def create_character(self):
        """Kreiraj novog lika prema unosu (ime, rasa, klasa)."""
        name = self.var_name.get().strip()
        race = self.var_race.get().strip()
        klass = self.var_class.get()

        if not name:
            messagebox.showwarning("Nedostaje ime", "Unesi ime lika.")
            return
        if not race:
            messagebox.showwarning("Nedostaje rasa", "Unesi rasu lika.")
            return

        ch = create_character_by_class(name, race, klass)
        self._characters.append(ch)
        self._refresh_list()
        self._populate_details(ch)
        self._update_status(f"Kreiran lik: {ch.name} ({ch.klass})")
        self.var_name.set(""); self.var_race.set(""); self.cb_class.focus_set()

    def _on_select(self, event=None):
        """
        Reakcija na promjenu selekcije.
        Bugfix: ignoriraj “lažni” deselect (npr. zbog promjene fokusa na Combobox),
        da se panel detalja ne prazni.
        """
        ch = self._get_selected_character()
        if ch is None:
            return
        self._populate_details(ch)

    def _populate_details(self, ch: Character | None):
        """Napuni desni panel detaljima o liku: atributi, skills, inventory."""
        if ch is None:
            # reset UI polja
            self.lbl_attr_str.config(text="Snaga: -")
            self.lbl_attr_int.config(text="Inteligencija: -")
            self.lbl_attr_spd.config(text="Brzina: -")
            self.lbl_attr_hp.config(text="HP: -")
            self.lb_skills.delete(0, tk.END)
            self.lb_inventory.delete(0, tk.END)
            self.cb_skill["values"] = []; self.cb_skill.set("")
            return

        # Atributi (read-only)
        self.lbl_attr_str.config(text=f"Snaga: {ch.strength}")
        self.lbl_attr_int.config(text=f"Inteligencija: {ch.intelligence}")
        self.lbl_attr_spd.config(text=f"Brzina: {ch.speed}")
        self.lbl_attr_hp.config(text=f"HP: {ch.hp}")

        # Skills (naučeni)
        self.lb_skills.delete(0, tk.END)
        for s in ch.learned_skills:
            self.lb_skills.insert(tk.END, s.name)

        # Inventory (items)
        self.lb_inventory.delete(0, tk.END)
        for it in ch.inventory:
            self.lb_inventory.insert(tk.END, it.name)

        # Dostupni skills po klasi (ponude u kombu)
        self.cb_skill["values"] = SKILL_CATALOG.get(ch.klass, [])
        self.cb_skill.set("")

    # --- Skills (učenje/uklanjanje) ---
    def _cmd_learn_skill(self):
        """Pokušaj naučiti skill odabran u comboboxu za trenutno odabranog lika."""
        ch = self._get_selected_character()
        if not ch:
            messagebox.showinfo("Skills", "Odaberite lika.")
            return
        name = self.var_skill_combo.get()
        if not name:
            messagebox.showwarning("Skills", "Odaberite skill iz padajućeg izbornika.")
            return
        s = Skill(name)
        if not ch.can_learn(s):
            messagebox.showerror("Zabranjeno", f"{ch.klass} ne može naučiti: {name}")
            return
        if not ch.learn_skill(s):
            messagebox.showinfo("Skills", f"Skill '{name}' je već naučen.")
            return
        self.lb_skills.insert(tk.END, name)
        self._update_status(f"{ch.name} je naučio skill: {name}")

    def _cmd_remove_skill(self):
        """Ukloni trenutno označeni skill iz liste naučenih."""
        ch = self._get_selected_character()
        if not ch:
            messagebox.showinfo("Skills", "Odaberite lika.")
            return
        idxs = self.lb_skills.curselection()
        if not idxs:
            messagebox.showinfo("Skills", "Odaberite skill u listi.")
            return
        name = self.lb_skills.get(idxs[0])
        ch.learned_skills = [s for s in ch.learned_skills if s.name != name]
        self.lb_skills.delete(idxs[0])
        self._update_status(f"Uklonjen skill: {name}")

    # --- Inventory (dodaj/ukloni) ---
    def _cmd_add_item(self):
        """Dodaj item iz comboboxa u inventar odabranog lika."""
        ch = self._get_selected_character()
        if not ch:
            messagebox.showinfo("Inventory", "Odaberite lika.")
            return
        name = self.var_item_combo.get()
        if not name:
            messagebox.showwarning("Inventory", "Odaberite item iz padajućeg izbornika.")
            return
        ch.add_item(Item(name))
        self.lb_inventory.insert(tk.END, name)
        self._update_status(f"Dodan item: {name}")

    def _cmd_remove_item(self):
        """Ukloni trenutno označeni item iz inventara odabranog lika."""
        ch = self._get_selected_character()
        if not ch:
            messagebox.showinfo("Inventory", "Odaberite lika.")
            return
        idxs = self.lb_inventory.curselection()
        if not idxs:
            messagebox.showinfo("Inventory", "Odaberite item u listi.")
            return
        name = self.lb_inventory.get(idxs[0])
        if ch.remove_item(name):
            self.lb_inventory.delete(idxs[0])
            self._update_status(f"Uklonjen item: {name}")

    # --- CRUD / pomoćno ---
    def delete_selected(self):
        """Obriši trenutno odabranog lika (uz potvrdu)."""
        ch = self._get_selected_character()
        if not ch:
            messagebox.showinfo("Brisanje", "Odaberite lika u listi.")
            return
        if messagebox.askyesno("Potvrda", f"Trajno obrisati lika '{ch.name}'?"):
            idx = self.lb_characters.curselection()[0]
            del self._characters[idx]
            self._refresh_list()
            self._populate_details(None)
            self._update_status("Lik obrisan.")

    # --- XML: pojedinačni lik ---
    def _cmd_save_character_xml(self):
        """Spremi trenutno odabranog lika u XML"""
        ch = self._get_selected_character()
        if not ch:
            messagebox.showinfo("Spremanje", "Odaberite lika.")
            return
        default_name = f"{ch.name}.xml"
        path = filedialog.asksaveasfilename(defaultextension=".xml", initialfile=default_name, filetypes=[("XML datoteke", "*.xml")])
        if not path:
            return
        try:
            ET.ElementTree(ch.to_xml()).write(path, encoding="utf-8", xml_declaration=True)
            self._update_status(f"Spremljen lik u {os.path.basename(path)}")
            messagebox.showinfo("Spremljeno", f"Spremljeno u:\n{path}")
        except Exception as e:
            messagebox.showerror("Greška pri spremanju", str(e))

    def _cmd_load_character_xml(self):
        """Učitaj lika iz XML-a"""
        path = filedialog.askopenfilename(filetypes=[("XML datoteke", "*.xml")])
        if not path:
            return
        try:
            tree = ET.parse(path)
            ch = Character.from_xml(tree.getroot())
            # Ako postoji isti naziv, dodaj sufiks (2), (3)...
            existing = {c.name for c in self._characters}
            base = ch.name
            i = 2
            while ch.name in existing:
                ch.name = f"{base} ({i})"
                i += 1
            self._characters.append(ch)
            self._refresh_list()
            messagebox.showinfo("Učitano", f"Učitano iz:\n{path}")
        except Exception as e:
            messagebox.showerror("Greška pri učitavanju", str(e))

    # --- XML: stanje aplikacije (svi likovi) ---
    def _cmd_save_app_state(self):
        """Spremi sve likove u jedan XML"""
        path = filedialog.asksaveasfilename(defaultextension=".xml", initialfile=self.APP_STATE_FILE, filetypes=[("XML datoteke", "*.xml")])
        if not path:
            return
        try:
            root = ET.Element("playgrounded_state")
            root.set("version", APP_VERSION)
            e_chars = ET.SubElement(root, "characters")
            for ch in self._characters:
                e_chars.append(ch.to_xml())
            ET.ElementTree(root).write(path, encoding="utf-8", xml_declaration=True)
            self._update_status(f"Stanje aplikacije spremljeno ({len(self._characters)} likova).")
            messagebox.showinfo("Spremljeno", f"Spremljeno u:\n{path}")
        except Exception as e:
            messagebox.showerror("Greška pri spremanju", str(e))

    def _cmd_load_app_state(self):
        """Učitaj kompletno stanje aplikacije iz XML-a"""
        path = filedialog.askopenfilename(filetypes=[("XML datoteke", "*.xml")])
        if not path:
            return
        try:
            tree = ET.parse(path)
            root = tree.getroot()

            characters = []

            for e in root.findall("./characters/character"):
                characters.append(Character.from_xml(e))

            self._characters = characters
            self._refresh_list()
            self._update_status(f"Stanje učitano: {len(self._characters)} likova.")
            messagebox.showinfo("Učitano", f"Učitano iz:\n{path}")
        except Exception as e:
            messagebox.showerror("Greška pri učitavanju", str(e))

    #Info prozori
    def _cmd_about_app(self):
        """Prikaži *About* prozor s logom i metapodacima aplikacije."""
        win = tk.Toplevel(self.master); win.title("O aplikaciji"); win.resizable(False, False)
        frm = ttk.Frame(win, padding=12); frm.pack(fill="both", expand=True)
        c = tk.Canvas(frm, width=80, height=80, bg=COLOR_BG, highlightthickness=0)
        c.grid(row=0, column=0, rowspan=3, padx=(0, 12))
        c.create_oval(4, 4, 76, 76, fill=COLOR_PANEL_2, outline=COLOR_SECOND, width=2)
        c.create_oval(12, 12, 68, 68, fill=COLOR_PRIMARY, outline="", width=0)
        c.create_text(40, 40, text="PG", fill="#0B1220", font=("Segoe UI", 26, "bold"))
        ttk.Label(frm, text=APP_NAME, font=("Segoe UI", 14, "bold"),
                  foreground=COLOR_PRIMARY).grid(row=0, column=1, sticky="w")
        ttk.Label(frm, text=APP_TAGLINE, foreground=COLOR_TEXT_MUTED).grid(row=1, column=1, sticky="w")
        ttk.Label(frm, text=f"Verzija: {APP_VERSION}\nAutor: {APP_AUTHOR}").grid(row=2, column=1, sticky="w", pady=(6,0))
        ttk.Button(frm, text="Zatvori", command=win.destroy).grid(row=3, column=0, columnspan=2, pady=(12, 0))

    def _cmd_about_classes(self):
        #Sažet opis klasa i njihovi skillovi
        txt = (
            "Warrior: Klasa koja se bazira na snazi i obrani, mana joj je niska brzina i malen domet. Skillovi: Sigma Strike, Udarčina, Blok.\n\n"
            "Mage: Klasa koja se bazira na strategičnom igranju, mana joj je to što nije efektivna u close-quarter combatu. Skills: Fireball, Diddy Spell, Rulers Hand.\n\n"
            "Assassin: Klasa sa ogromnom brzinom i damageom - samo isključi mozak i igraj, mana joj je nizak hp - jedan krivi pokret i gotov si. Skills: Flashstep, Backstab, Mutilate.\n\n"
            "Note: Atributi i skillovi klasa specifični su za svaku klasu, odnosno svaki karakter može naučiti samo određene vještine."
        )
        messagebox.showinfo("O klasama", txt)



# Entry
def main():
    root = tk.Tk()
    try:
        root.tk.call("tk", "scaling", 1.2)
    except:
        pass
    app = PlaygroundedApp(root)
    root.minsize(1000, 560)
    root.configure(bg=COLOR_BG)
    root.mainloop()

if __name__ == "__main__":
    main()