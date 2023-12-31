"----------------------------------------------------command_full----------------------------------------------------"
"""
    Moduł stanowiący instrukcję przycisku "Pełna lista stacji pomiarowych" głównego okna. Zawiera klasę CommandFull,
która kolejno:
- wyświetla okno z listboxem, w którym umieszczona jest pełna lista stacji pomiarowych,
- po wybraniu id stacji - wyświetla listę stanowisk pomiarowych, gdzie każde stanowisko mierzy inny parametr,
- po wybraniu id parametru - wyświetla wykres danych oraz ich listę,
- po zamknięciu okienka wykresu, a następnie kliknięciu przysciku analizuj - wyświetla linię trendu oraz prostą analizę 
  danych.

"""

from get_stations_data import get_stations_data
from get_sensors_data import get_sensors_data
from get_measurements_data import get_measurements_data
from tkinter import *
import tkinter as tk
import sqlite3
from measurement_analysis import MeasurementAnalysis
from print_analysis import AnalysisWindow

class CommandFull(Tk):
    """
        Klasa wyświetla listę wszytskich stacji pomiarowych i finalnie umożliwia przeglądanie pomiarów wybranych
    parametrów, zarówno w formie wykresu, jak i listy. Pozwala także na prostą analizę danych za pomocą dedykowanego
    przycisku.
    """
    def __init__(self, *args, **kwargs):
        """
        Inicjalizuje instancję klasy CommandFull.

        Args:
            *args: Pozycyjne argumenty przekazywane do klasy bazowej Tk.
            **kwargs: Nazwane argumenty przekazywane do klasy bazowej Tk.
        """
        super().__init__(*args, **kwargs)
        self.title("Air Quality Poland")
        self.geometry('1200x700')

        label_name = tk.Label(self, text="Pełna lista stacji pomiarowych")
        label_line = tk.Label(self, text="")
        label_name.pack()
        label_line.pack()

        self.frame = Frame(self)
        self.frame.pack(fill=BOTH, expand=NO)

        self.listbox = Listbox(self, font=("Courier", 10))
        self.listbox.pack(side=TOP, fill=BOTH, expand=YES)
        scrollbar_vertical = Scrollbar(self.listbox, orient=VERTICAL, command=self.listbox.yview)
        scrollbar_horizontal = Scrollbar(self.listbox, orient=HORIZONTAL, command=self.listbox.xview)
        self.listbox.config(yscrollcommand=scrollbar_vertical.set)
        self.listbox.config(xscrollcommand=scrollbar_horizontal.set)
        scrollbar_vertical.pack(side=RIGHT, fill=Y)
        scrollbar_horizontal.pack(side=BOTTOM, fill=X)

        headers = ("ID", "Nazwa stacji", "Szer.geog.", "Dług.geog.", "ID miasta", "Miasto", "Gmina", "Powiat", "Wojewódźtwo")
        column_widths = (5, 50, 10, 10, 10, 20, 20, 25, 25)
        header_row = " | ".join(
            header.center(width) for header, width in zip(headers, column_widths))
        self.listbox.insert(tk.END, header_row)

        self.label_staionId = Label(self.frame, text="Podaj id stacji w celu wyświetlenia stanowisk pomiarowych")
        self.label_id = Label(self.frame, text="Podaj id stanowiska w celu wyświetlenia danych pomiarowych")
        self.label_analysis = Label(self.frame, text="Analiza danych")

        self.entry_staionId = Entry(self.frame, bd=5)
        self.entry_id = Entry(self.frame, bd=5)

        self.button_stationId = Button(self.frame, text="Szukaj", command=self.show_sensors_data)
        self.button_id = Button(self.frame, text="Szukaj", command=self.show_measurements_data)
        self.button_analysis = Button(self.frame, text="Analiza danych", command=AnalysisWindow)

        self.label_staionId.grid(row=1, column=0, padx=10)
        self.label_id.grid(row=2, column=0, padx=10)
        self.label_analysis.grid(row=3, column=0, padx=10)

        self.entry_staionId.grid(row=1, column=1, padx=10)
        self.entry_id.grid(row=2, column=1, padx=10)

        self.button_stationId.grid(row=1, column=2, padx=10)
        self.button_id.grid(row=2, column=2, padx=10)
        self.button_analysis.grid(row=3, column=2, padx=10)

        get_stations_data()

        self.conn = sqlite3.connect('database.db')
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM stations')
        result = cursor.fetchall()

        for row in result:
            formatted_row = " | ".join(
                str(item).center(width) for item, width in zip(row, column_widths))
            self.listbox.insert(tk.END, formatted_row)

        self.mainloop()

    def show_measurements_data(self):
        """
            Wyświetla dane pomiarowe dla wybranego stanowiska.

            Pobiera wartość ID stanowiska z pola entry_id, pobiera z bazy danych odpowiednie dane pomiarowe
        i wyświetla je w listboxie. Następnie generuje wykres na podstawie tych danych.
        """

        self.listbox.delete(0, tk.END)

        headers = ("Data pobrania", "Dane pomiarowe")
        column_widths = (20, 20)
        header_row = " | ".join(
            header.center(width) for header, width in zip(headers, column_widths))
        self.listbox.insert(tk.END, header_row)

        id = int(self.entry_id.get())
        get_measurements_data(id)

        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM measurements')
        result = cursor.fetchall()

        for row in result:
            formatted_row = " | ".join(
                str(item).center(width) for item, width in zip(row, column_widths))
            self.listbox.insert(tk.END, formatted_row)

        MeasurementAnalysis().chart()

    def show_sensors_data(self):
        """
            Wyświetla listę stanowisk pomiarowych dla wybranej stacji. Każde stanowisko bada osobny parametr.

            Pobiera wartość ID stacji z pola entry_stationId, pobiera z bazy danych odpowiednie stanowiska pomiarowe
        i wyświetla je w listboxie.
        """
        self.listbox.delete(0, END)

        headers = ("ID stanowiska", "ID stacji", "Nazwa parametru", "Symbol parametru", "Kod parametru", "ID parametru")
        column_widths = (15, 15, 25, 25, 25, 20)
        header_row = " | ".join(
            header.center(width) for header, width in zip(headers, column_widths))
        self.listbox.insert(tk.END, header_row)

        stationId = int(self.entry_staionId.get())
        get_sensors_data(stationId)

        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM sensors')
        result = cursor.fetchall()

        for row in result:
            formatted_row = " | ".join(
                str(item).center(width) for item, width in zip(row, column_widths))
            self.listbox.insert(tk.END, formatted_row)

if __name__ == '__main__': CommandFull()
