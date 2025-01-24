from tkinter import *
import random
from random import randint

#laukums un kartupeļu lielumi
LAUKUMS=10
KARTUPEĻU_LIELUMI=[5,4,4,3,3,3,2,2,2,2]
logs=Tk()

def izveidot_laukumu():
    #izveido laukus no A līdz J
    for col in range (LAUKUMS+1):
        if col == 0:
            Label(logs, text="", width=4, height=2).grid(row=0, column=col)
        else:
            Label(logs, text=chr(64 + col), width=4, height=2).grid(row=0, column=col)
    #izveido laukus no 1 līdz 10
    for row in range(1, LAUKUMS + 1):
        Label(logs, text=str(row), width=4, height=2).grid(row=row, column=0)
        for col in range(1, LAUKUMS + 1):
            poga = Button(logs, text="", width=4, height=2, bg="gray", relief="solid", borderwidth=2)
            poga.grid(row=row, column=col)

def kartupeļa_novietojums():
    global kartupeļa_pozīcija
    kartupeļa_pozīcija=[]
    def validēt_kartupeļa_koordinātes():
        for r,c in kartupeļa_novietojums:
            if any((r+dr+c+dc) in kartupeļa_novietojums for dr in [-1, 0, 1] for dc in [-1, 0, 1]):
                return False
            return True
    # Kods ņemts no chatgpt
    for lielums in KARTUPEĻU_LIELUMI:
        novietots=False
        while not novietots:
            orientācija = random.choice(["Horizontāls", "Vertikāls"])
        if orientācija == "Horizontāls":
            rinda = random.randint(1, LAUKUMS)
            kolonna = random.randint(1, LAUKUMS - lielums + 1)
            kuģa_koordinātes = [(rinda, kolonna + i) for i in range(lielums)]
        else:  # "Vertikāls"
            rinda = random.randint(1, LAUKUMS - lielums + 1)
            kolonna = random.randint(1, LAUKUMS)
            kuģa_koordinātes = [(rinda + i, kolonna) for i in range(lielums)]

        if validēt_kartupeļa_koordinātes(kartupeļa_novietojums):
            kartupeļa_pozīcija.extend(kuģa_koordinātes)
            novietots = True

izveidot_laukumu()  
logs.mainloop()

