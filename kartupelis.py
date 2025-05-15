from tkinter import *
import random

# Laukuma izmērs un kuģu lielumi (kartupeļi)
LAUKUMS = 10
KARTUPEĻU_LIELUMI = [5, 4, 4, 3, 3, 3, 2, 2, 2, 2]
kartupeļa_pozīcija = []
rezultāta_label = None
laika_label = None
dzivibu_label = None
spēle_beigusies = False
Laukums = None
sākums = None
atkārtot_poga = None
menu_poga = None
atlikusas_sekundes = 60
dzivibas = 10


def izveidot_laukumu():
    global Laukums, rezultāta_label, spēle_beigusies, atkārtot_poga, menu_poga
    spēle_beigusies = False
    Laukums = Tk()
    Laukums.title("Kartupelis")

    # Izveido kolonnu galvenes (no A līdz J)
    for kolonna in range(LAUKUMS + 1):
        if kolonna == 0:
            Label(Laukums, text="", width=4, height=2).grid(row=0, column=kolonna)
        else:
            Label(Laukums, text=chr(64 + kolonna), width=4, height=2).grid(row=0, column=kolonna)
    
    # Izveido rindu galvenes (no1 līdz 10) un pogas 
    for rinda in range(1, LAUKUMS + 1):
        Label(Laukums, text=str(rinda), width=4, height=2).grid(row=rinda, column=0)
        for kolonna in range(1, LAUKUMS + 1):
            poga = Button(Laukums, text="", width=4, height=2, bg="gray", relief="solid", 
                         borderwidth=2, command=lambda r=rinda, c=kolonna: minēt(r, c))
            poga.grid(row=rinda, column=kolonna)
    
    # Izveido rezultāta labeli vienu reizi
    rezultāta_label = Label(Laukums, text="Mēģini atrast kartupeļus!", fg="black", font=("Arial", 12))
    rezultāta_label.grid(row=LAUKUMS + 1, column=0, columnspan=LAUKUMS + 1)

    # Pogas rāmis
    pogu_rāmis = Frame(Laukums)
    pogu_rāmis.grid(row=LAUKUMS + 2, column=0, columnspan=LAUKUMS + 1, pady=10)
    
    # Pogas tiks izveidotas, bet paslēptas līdz spēles beigām
    atkārtot_poga = Button(pogu_rāmis, text="Mēģināt vēlreiz", command=atkārtot, state=DISABLED)
    atkārtot_poga.pack(side=LEFT, padx=10)
    
    menu_poga = Button(pogu_rāmis, text="Atgriezties izvēlnē", command=atpakaļ_uz_izvēlni, state=DISABLED)
    menu_poga.pack(side=LEFT, padx=10)

    global laika_label, atlikusas_sekundes
    atlikusas_sekundes = 60  # Restartē taimeri

    laika_label = Label(Laukums, text=f"Atlikušais laiks: {atlikusas_sekundes} s", fg="black", font=("Arial", 12))
    laika_label.grid(row=LAUKUMS + 3, column=0, columnspan=LAUKUMS + 1)

    global dzivibu_label, dzivibas
    dzivibas = 10  # Restartē dzīvības


    dzivibu_label = Label(Laukums, text=f"Dzīvības: {dzivibas}", fg="black", font=("Arial", 12))
    dzivibu_label.grid(row=LAUKUMS + 4, column=0, columnspan=LAUKUMS + 1)

    sākt_taimeri()

def atkārtot():
    global Laukums
    if Laukums:
        Laukums.destroy()
    kartupeļa_novietojums()
    izveidot_laukumu()

def atpakaļ_uz_izvēlni():
    global Laukums, sākums
    if Laukums:
        Laukums.destroy()
    izveidot_izvelni()

def izveidot_izvelni():
    global sākums
    sākums = Tk()
    sākums.title("Menu")
    sākumsY = 600
    sākumsX = 900
    sākums.geometry(f"{sākumsX}x{sākumsY}")

    sākums_rāmis = Frame(sākums)
    sākums_rāmis.pack(pady=50)

    poga_spēlēt = Button(sākums_rāmis, text="SPĒLĒT", command=lambda: [sākums.destroy(), kartupeļa_novietojums(), izveidot_laukumu()])
    poga_spēlēt.pack(pady=20)

    poga_beigt = Button(sākums_rāmis, text="IZIET", command=sākums.destroy)
    poga_beigt.pack(pady=20)

    sākums.mainloop()

def validēt_kartupeļa_koordinātes(kartupeļa_koordinātes):
    for r, c in kartupeļa_koordinātes:
        # Pārbauda tikai ortogonālos kaimiņus (nevis diagonālos)
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            if (r + dr, c + dc) in kartupeļa_pozīcija:
                return False
    return True

def kartupeļa_novietojums():
    global kartupeļa_pozīcija
    kartupeļa_pozīcija = []

    for lielums in KARTUPEĻU_LIELUMI:
        novietots = False
        while not novietots:
            orientācija = random.choice(["Horizontāls", "Vertikāls"])
            if orientācija == "Horizontāls":
                rinda = random.randint(1, LAUKUMS)
                kolonna = random.randint(1, LAUKUMS - lielums + 1)
                kartupeļa_koordinātes = [(rinda, kolonna + i) for i in range(lielums)]
            else:
                rinda = random.randint(1, LAUKUMS - lielums + 1)
                kolonna = random.randint(1, LAUKUMS)
                kartupeļa_koordinātes = [(rinda + i, kolonna) for i in range(lielums)]

            if validēt_kartupeļa_koordinātes(kartupeļa_koordinātes):
                kartupeļa_pozīcija.extend(kartupeļa_koordinātes)
                novietots = True

def atspējot_pogas():
    global spēle_beigusies, atkārtot_poga, menu_poga
    spēle_beigusies = True
    
    # Atspējo spēles laukuma pogas
    for rinda in range(1, LAUKUMS + 1):
        for kolonna in range(1, LAUKUMS + 1):
            for elements in Laukums.grid_slaves():
                if (int(elements.grid_info()["row"]) == rinda and 
                    int(elements.grid_info()["column"]) == kolonna and 
                    isinstance(elements, Button)):
                    elements.config(state=DISABLED)
    
    # Ieslēdz pogas "Mēģināt vēlreiz" un "Atgriezties izvēlnē"
    atkārtot_poga.config(state=NORMAL)
    menu_poga.config(state=NORMAL)

def minēt(rinda, kolonna):
    global spēle_beigusies, dzivibas
    if spēle_beigusies:
        return
        
    if (rinda, kolonna) in kartupeļa_pozīcija:
        rezultāta_label.config(text=f"Trāpījums! Tu trāpīji kuģim pie {chr(64 + kolonna)}{rinda}.", fg="green")
        kartupeļa_pozīcija.remove((rinda, kolonna))
        
        # Atjauno pogas vizuālo izskatu
        for elements in Laukums.grid_slaves():
            info = elements.grid_info()
            if int(info["row"]) == rinda and int(info["column"]) == kolonna:
                elements.config(bg="cyan", text="⚫", state=DISABLED)
                break
        
        # Pārbauda, vai visi kuģi ir nogremdēti
        if not kartupeļa_pozīcija:
            rezultāta_label.config(text="Apsveicam! Tu nogremdēji visus kartupeļus!", fg="blue")
            atspējot_pogas()
    else:
        rezultāta_label.config(text="Netrāpīji! Mēģini vēlreiz.", fg="red")
        # Atjauno netrāpītās šūnas izskatu
        for elements in Laukums.grid_slaves():
            info = elements.grid_info()
            if int(info["row"]) == rinda and int(info["column"]) == kolonna:
                elements.config(bg="white", state=DISABLED)
                break
        dzivibas -= 1
        dzivibu_label.config(text=f"Dzīvības: {dzivibas}")

        if dzivibas <= 0:
            rezultāta_label.config(text="Tu zaudēji! Tev beidzās dzīvības!", fg="orange")
            atspējot_pogas()

def sākt_taimeri():
    global atlikusas_sekundes
    if atlikusas_sekundes > 0 and not spēle_beigusies:
        laika_label.config(text=f"Atlikušais laiks: {atlikusas_sekundes} s")
        atlikusas_sekundes -= 1
        Laukums.after(1000, sākt_taimeri)
    elif not spēle_beigusies:
        rezultāta_label.config(text="Laiks beidzies! Tu neatradi visus kartupeļus.", fg="orange")
        atspējot_pogas()

# Uzsākt spēli, parādot izvēlni
izveidot_izvelni()