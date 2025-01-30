from tkinter import *
import random

# Laukuma izmērs un kuģu lielumi (kartupeļi)
LAUKUMS = 10
KARTUPEĻU_LIELUMI = [5, 4, 4, 3, 3, 3, 2, 2, 2, 2]
kartupeļa_pozīcija = []

def izveidot_laukumu():
    global Laukums
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
            poga = Button(Laukums,text="",width=4,height=2,bg="gray",relief="solid",borderwidth=2,command=lambda r=rinda, c=kolonna: minēt(r, c),)
            poga.grid(row=rinda, column=kolonna)

def validēt_kartupeļa_koordinātes(kartupeļa_koordinātes):
    for r, c in kartupeļa_koordinātes:
        if any((r + dr, c + dc) in kartupeļa_pozīcija for dr in [-1, 0, 1] for dc in [-1, 0, 1]):
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
kartupeļa_novietojums()

def minēt(rinda, kolonna):    
    rezultāts = Label(Laukums, text="Mēģini atrast kartupeļus!", fg="black", font=("Arial", 12))
    rezultāts.grid(row=LAUKUMS + 1, column=0, columnspan=LAUKUMS + 1)
    if (rinda, kolonna) in kartupeļa_pozīcija:
        rezultāts.config(
            text=f"Trāpījums! Tu trāpīji kuģim pie {chr(64 + kolonna)}{rinda}.", fg="green")
        kartupeļa_pozīcija.remove((rinda, kolonna))
        # Atjauno pogas vizuālo izskatu
        for elements in Laukums.grid_slaves():
            if int(elements.grid_info()["row"]) == rinda and int(elements.grid_info()["column"]) == kolonna:
                elements.config(bg="red", text="X")
                break
            # Pārbauda, vai visi kuģi ir nogremdēti
        if not kartupeļa_pozīcija:
            rezultāts.config(text="Apsveicam! Tu nogremdēji visus kartupeļus!", fg="blue")
    else:
        rezultāts.config(text="Netālu! Mēģini vēlreiz.", fg="red")


# Sākuma logs
sākums = Tk()
sākums.title("menu")
sākumsY = 600
sākumsX = 900
sākums.geometry(f"{sākumsX}x{sākumsY}")

sākums_rāmis = Frame(sākums)
sākums_rāmis.pack()

poga_spēlēt = Button(sākums_rāmis, text = "SPĒLĒT", command = izveidot_laukumu)
poga_spēlēt.pack()

sākums.mainloop()


