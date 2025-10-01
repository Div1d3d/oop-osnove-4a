import tkinter as tk

def click():
    ime = ime_input.get()
    poz.config(text=f"Wsg, {ime}")

#Kreiranje glavnog prozora
prozor = tk.Tk()
prozor.title("Ovo NIJE moj prvi GUI")

#statični widget
poz_poruka = tk.Label(prozor, text="Wsp")
poz_poruka.pack()

uputa = tk.Label(prozor, text="Ime:")
uputa.pack()
ime_input=tk.Entry(prozor)
ime_input.pack()

btn = tk.Button(prozor, text="Bam", command=click)
btn.pack()

poz=tk.Label(prozor, text="")
poz.pack()

prozor.geometry("800x600")

tk.mainloop()