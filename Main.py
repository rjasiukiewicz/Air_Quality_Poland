"----------------------------------------------------Air Quality Poland-----------------------------------------------"
"""
    Air Quality Poland prezentuje dane potyczące jakości powietrza w Polsce, publikowane przez 
    Główny Inspektorat Ochrony Środowiska. Pobrane dane można poddać podstawowej analizie, przedstawić w formie wykresu
    i listy. 
      
"""

import tkinter as tk
from command_full import CommandFull
from command_city import CommandCity
from command_location import CommandLocation
from command_map import CommandMap


root = tk.Tk()
root.title("Air Quality Poland")
root.geometry('600x400')


label1 = tk.Label(root, text="Witaj w aplikacji służącej do przeglądania danych pomiarowych jakości powietrza"
                             " na terytorium Polski.")

label1.pack()

button_full = tk.Button(root, text="Lista wszystkich stacji pomiarowych", command=CommandFull)
button_city = tk.Button(root, text="Wyszukaj stacje po nazwie miejscowości", command=CommandCity)
button_location = tk.Button(root, text="Wyszukaj najbliżej położone stacje", command=CommandLocation)
button_map = tk.Button(root, text="Wybierz punkt na mapie", command=CommandMap)

button_full.place(x=175, y=100, width=250, height=30)
button_city.place(x=175, y=150, width=250, height=30)
button_location.place(x=175, y=200, width=250, height=30)
button_map.place(x=175, y=250, width=250, height=30)

root.mainloop()
