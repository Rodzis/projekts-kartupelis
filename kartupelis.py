from tkinter import *
import random
from datetime import datetime

# Konstantes
LAUKUMS = 10
KARTUPEĻU_IZMĒRI = [5, 4, 4, 3, 3, 3, 2, 2, 2, 2]
REZULTĀTU_FAILS = "rezultati.txt"

# Globālie mainīgie
kartupelu_pozicijas = []
rezultata_uzraksts = None
laika_uzraksts = None
dzivibu_uzraksts = None
spele_beigusies = False
Speles_laukums = None
izvelnes_logs = None
atkartot_poga = None
izvelnes_poga = None
rezultatu_poga = None
atlikusas_sekundes = 60
dzivibas = 10
grutibas_pakape = "Vidēja"

def aprekinat_rezultatu():
    global atlikusas_sekundes, dzivibas, grutibas_pakape
    
    # Nosaka grūtības reizinātāju
    if grutibas_pakape == "Vieglā":
        reizinatajs = 1
    elif grutibas_pakape == "Vidēja":
        reizinatajs = 5
    else:  # Grūtā
        reizinatajs = 10
    
    # Aprēķina rezultātu pēc atlikušā laika un dzīvībām
    laika_rezultats = atlikusas_sekundes * reizinatajs
    dzivibu_rezultats = dzivibas * reizinatajs
    kopējais_rezultats = laika_rezultats + dzivibu_rezultats
    
    return kopējais_rezultats

def saglabat_rezultatu():
    rezultats = aprekinat_rezultatu()
    tagad = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open(REZULTĀTU_FAILS, "a", encoding="utf-8") as fails:
        fails.write(f"{tagad} | Grūtība: {grutibas_pakape} | Rezultāts: {rezultats} | Atlikušais laiks: {atlikusas_sekundes}s | Atlikušās dzīvības: {dzivibas}\n")

def paradit_rezultatu_tabulu():
    rezultatu_logs = Toplevel()
    rezultatu_logs.title("Rezultātu tabula")
    rezultatu_logs.geometry("600x400")
    
    teksta_lauks = Text(rezultatu_logs, wrap=WORD)
    teksta_lauks.pack(expand=True, fill=BOTH)
    
    ritjosla = Scrollbar(teksta_lauks)
    ritjosla.pack(side=RIGHT, fill=Y)
    teksta_lauks.config(yscrollcommand=ritjosla.set)
    ritjosla.config(command=teksta_lauks.yview)
    
    try:
        with open(REZULTĀTU_FAILS, "r", encoding="utf-8") as fails:
            rezultati = fails.readlines()
            if not rezultati:
                teksta_lauks.insert(END, "Vēl nav rezultātu!\n")
            else:
                teksta_lauks.insert(END, "=== REZULTĀTU TABULA ===\n\n")
                for rezultats in reversed(rezultati):  # Rāda jaunākos pirmos
                    teksta_lauks.insert(END, rezultats)
    except FileNotFoundError:
        teksta_lauks.insert(END, "Rezultātu fails vēl nav izveidots.\n")

def izveidot_speles_laukumu():
    global Speles_laukums, rezultata_uzraksts, spele_beigusies, atkartot_poga, izvelnes_poga, rezultatu_poga
    global laika_uzraksts, atlikusas_sekundes, dzivibu_uzraksts, dzivibas

    spele_beigusies = False
    Speles_laukums = Tk()
    Speles_laukums.title("Kartupeļu medības")

    if grutibas_pakape == "Vieglā":
        atlikusas_sekundes = 120
        dzivibas = 20
    elif grutibas_pakape == "Vidēja":
        atlikusas_sekundes = 100
        dzivibas = 15
    else:
        atlikusas_sekundes = 60
        dzivibas = 10

    # Izveido kolonnu virsrakstus (A-J)
    for kolonna in range(LAUKUMS + 1):
        if kolonna == 0:
            Label(Speles_laukums, text="", width=4, height=2).grid(row=0, column=kolonna)
        else:
            Label(Speles_laukums, text=chr(64 + kolonna), width=4, height=2).grid(row=0, column=kolonna)

    # Izveido spēles laukumu ar pogām
    for rinda in range(1, LAUKUMS + 1):
        Label(Speles_laukums, text=str(rinda), width=4, height=2).grid(row=rinda, column=0)
        for kolonna in range(1, LAUKUMS + 1):
            poga = Button(Speles_laukums, text="", width=4, height=2, bg="pelēks", relief="solid", 
                         borderwidth=2, command=lambda r=rinda, c=kolonna: minejums(r, c))
            poga.grid(row=rinda, column=kolonna)

    rezultata_uzraksts = Label(Speles_laukums, text="Mēģini atrast kartupeļus!", fg="melns", font=("Arial", 12))
    rezultata_uzraksts.grid(row=LAUKUMS + 1, column=0, columnspan=LAUKUMS + 1)

    pogu_apvienojums = Frame(Speles_laukums)
    pogu_apvienojums.grid(row=LAUKUMS + 2, column=0, columnspan=LAUKUMS + 1, pady=10)

    atkartot_poga = Button(pogu_apvienojums, text="Mēģināt vēlreiz", command=atkartot, state=DISABLED)
    atkartot_poga.pack(side=LEFT, padx=10)
    
    izvelnes_poga = Button(pogu_apvienojums, text="Atgriezties izvēlnē", command=atgriezties_izvelne, state=DISABLED)
    izvelnes_poga.pack(side=LEFT, padx=10)
    
    rezultatu_poga = Button(pogu_apvienojums, text="Rezultātu tabula", command=paradit_rezultatu_tabulu)
    rezultatu_poga.pack(side=LEFT, padx=10)

    laika_uzraksts = Label(Speles_laukums, text=f"Atlikušais laiks: {atlikusas_sekundes} s", fg="melns", font=("Arial", 12))
    laika_uzraksts.grid(row=LAUKUMS + 3, column=0, columnspan=LAUKUMS + 1)

    dzivibu_uzraksts = Label(Speles_laukums, text=f"Dzīvības: {dzivibas} ❤️", fg="melns", font=("Arial", 12))
    dzivibu_uzraksts.grid(row=LAUKUMS + 4, column=0, columnspan=LAUKUMS + 1)

    sakt_taimeri()

def atkartot():
    global Speles_laukums
    if Speles_laukums:
        Speles_laukums.destroy()
    izvietot_kartupelus()
    izveidot_speles_laukumu()

def atgriezties_izvelne():
    global Speles_laukums, izvelnes_logs
    if Speles_laukums:
        Speles_laukums.destroy()
    izveidot_izvelni()

def izveidot_izvelni():
    global izvelnes_logs, grutibas_pakape
    izvelnes_logs = Tk()
    izvelnes_logs.title("Izvēlne")
    izvelnes_logs.geometry("900x600")

    izvelnes_apvienojums = Frame(izvelnes_logs)
    izvelnes_apvienojums.pack(pady=50)

    Label(izvelnes_apvienojums, text="Izvēlies grūtības pakāpi:").pack(pady=10)
    grutibas_mainigais = StringVar(value="Vidēja")

    Radiobutton(izvelnes_apvienojums, text="Vieglā", variable=grutibas_mainigais, value="Vieglā").pack()
    Radiobutton(izvelnes_apvienojums, text="Vidēja", variable=grutibas_mainigais, value="Vidēja").pack()
    Radiobutton(izvelnes_apvienojums, text="Grūtā", variable=grutibas_mainigais, value="Grūtā").pack()

    def sakt_spele_ar_grutibam():
        global grutibas_pakape
        grutibas_pakape = grutibas_mainigais.get()
        izvelnes_logs.destroy()
        izvietot_kartupelus()
        izveidot_speles_laukumu()

    Button(izvelnes_apvienojums, text="SPĒLĒT", command=sakt_spele_ar_grutibam).pack(pady=20)
    Button(izvelnes_apvienojums, text="REZULTĀTU TABULA", command=paradit_rezultatu_tabulu).pack(pady=10)
    Button(izvelnes_apvienojums, text="IZIET", command=izvelnes_logs.destroy).pack(pady=20)

    izvelnes_logs.mainloop()

def parbaudit_kartupelu_koordinates(kartupelu_koordinates):
    for r, c in kartupelu_koordinates:
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            if (r + dr, c + dc) in kartupelu_pozicijas:
                return False
    return True

def izvietot_kartupelus():
    global kartupelu_pozicijas
    kartupelu_pozicijas = []

    for izmers in KARTUPEĻU_IZMĒRI:
        izvietots = False
        while not izvietots:
            virziens = random.choice(["Horizontāls", "Vertikāls"])
            if virziens == "Horizontāls":
                rinda = random.randint(1, LAUKUMS)
                kolonna = random.randint(1, LAUKUMS - izmers + 1)
                kartupelu_koordinates = [(rinda, kolonna + i) for i in range(izmers)]
            else:
                rinda = random.randint(1, LAUKUMS - izmers + 1)
                kolonna = random.randint(1, LAUKUMS)
                kartupelu_koordinates = [(rinda + i, kolonna) for i in range(izmers)]

            if parbaudit_kartupelu_koordinates(kartupelu_koordinates):
                kartupelu_pozicijas.extend(kartupelu_koordinates)
                izvietots = True

def atspējot_pogas():
    global spele_beigusies, atkartot_poga, izvelnes_poga
    spele_beigusies = True
    
    # Saglabā rezultātu, kad spēle beidzas
    saglabat_rezultatu()
    
    for rinda in range(1, LAUKUMS + 1):
        for kolonna in range(1, LAUKUMS + 1):
            for elements in Speles_laukums.grid_slaves():
                if (int(elements.grid_info()["row"]) == rinda and 
                    int(elements.grid_info()["column"]) == kolonna and 
                    isinstance(elements, Button)):
                    elements.config(state=DISABLED)
    
    atkartot_poga.config(state=NORMAL)
    izvelnes_poga.config(state=NORMAL)

def minejums(rinda, kolonna):
    global spele_beigusies, dzivibas
    if spele_beigusies:
        return
        
    if (rinda, kolonna) in kartupelu_pozicijas:
        rezultata_uzraksts.config(text=f"Trāpījums! Tu trāpīji kuģim pie {chr(64 + kolonna)}{rinda}.", fg="zaļš")
        kartupelu_pozicijas.remove((rinda, kolonna))
        
        dzivibas += 1
        dzivibu_uzraksts.config(text=f"Dzīvības: {dzivibas} ❤️")

        for elements in Speles_laukums.grid_slaves():
            info = elements.grid_info()
            if int(info["row"]) == rinda and int(info["column"]) == kolonna:
                elements.config(bg="zils", text="⚫", state=DISABLED)
                break

        if not kartupelu_pozicijas:
            rezultata_uzraksts.config(text="Apsveicam! Tu nogremdēji visus kartupeļus!", fg="zils")
            atspējot_pogas()
    else:
        rezultata_uzraksts.config(text="Netrāpīji! Mēģini vēlreiz.", fg="sarkans")
        dzivibas -= 1
        dzivibu_uzraksts.config(text=f"Dzīvības: {dzivibas} ❤️")

        for elements in Speles_laukums.grid_slaves():
            info = elements.grid_info()
            if int(info["row"]) == rinda and int(info["column"]) == kolonna:
                elements.config(bg="balts", state=DISABLED)
                break
        
        if dzivibas <= 0:
            rezultata_uzraksts.config(text="Tu zaudēji visas dzīvības!", fg="oranžs")
            atspējot_pogas()

def sakt_taimeri():
    global atlikusas_sekundes
    if atlikusas_sekundes >= 0 and not spele_beigusies:
        laika_uzraksts.config(text=f"Atlikušais laiks: {atlikusas_sekundes} s")
        atlikusas_sekundes -= 1
        Speles_laukums.after(1000, sakt_taimeri)
    elif not spele_beigusies:
        rezultata_uzraksts.config(text="Laiks beidzies! Tu neatradi visus kartupeļus.", fg="oranžs")
        atspējot_pogas()

# Sākt spēli, parādot izvēlni
izveidot_izvelni()