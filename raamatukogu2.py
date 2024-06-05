from sqlite3 import *
from sqlite3 import Error
import sqlite3
import tkinter as tk
from tkinter import *

connection = sqlite3.connect('my_database.db')

def create_connection(path:str):
    connection = None
    try:
        connection = connect(path)
        print("Ühendus on olemas!")
    except Error as e:
        print(f"Tekkis viga: {e}")
    return connection

conn=create_connection(".\my_database.db")

def execute_query(connection, query):
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        print("Tabel on loodut")
    except Error as e:
        print(f"Viga '{e}'tabeli loomisega")

create_autori_table = """
CREATE TABLE IF NOT EXISTS Autorid (
autor_id INTEGER PRIMARY KEY AUTOINCREMENT,
autor_nimi TEXT NOT NULL,
sünnikuupäev DATE NOT NULL
);
"""

create_zanri_table = '''
        CREATE TABLE IF NOT EXISTS Zanrid (
            žanr_id INTEGER PRIMARY KEY AUTOINCREMENT,
            žanri_nimi TEXT NOT NULL)
    '''

create_raamatu_table = '''
        CREATE TABLE IF NOT EXISTS Raamatud (
            raamat_id INTEGER PRIMARY KEY AUTOINCREMENT,
            pealkiri TEXT NOT NULL,
            väljaandmise_kuupäev DATE NOT NULL,
            žanri_nimi TEXT,
            autor_nimi TEXT,
            FOREIGN KEY (žanri_nimi) REFERENCES Žanrid (žanri_nimi),
            FOREIGN KEY (autor_nimi) REFERENCES Autorid (autor_nimi))
    '''

execute_query(conn, create_autori_table)
execute_query(conn, create_zanri_table)
execute_query(conn, create_raamatu_table)

def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"viga '{e}'")

select_autorid = "SELECT * from Autorid"
select_zanrid = "SELECT * from Zanrid"
select_raamatud = "SELECT * from Raamatud"

def add_zanr_query(connection, user_data):
    query = "INSERT INTO Zanrid(žanri_nimi) VALUES (?)"
    cursor = connection.cursor()
    cursor.execute(query, (user_data,))
    connection.commit()
    print("žanr lisatud edukalt!")

def add_autor_query(connection, user_data):
    query = "INSERT INTO Autorid(autor_nimi, sünnikuupäev) VALUES (?,?)"
    cursor = connection.cursor()
    cursor.execute(query, user_data)
    connection.commit()
    print("Autor lisatud edukalt!")

def delete_autor_query(conn, delete_autor):
    query = "DELETE FROM Autorid WHERE autor_id = ?"
    cursor = connection.cursor()
    cursor.execute(query, (delete_autor,))
    connection.commit()
    print("Autor kustutatud edukalt!")

def delete_zanr_query(conn, delete_zanr):
    query = "DELETE FROM Zanrid WHERE žanr_id = ?"
    cursor = connection.cursor()
    cursor.execute(query, (delete_zanr,))
    connection.commit()
    print("Žanr kustutatud edukalt!")

def add_raamat_query(connection, user_data):
    query = "INSERT INTO Raamatud(pealkiri, väljaandmise_kuupäev, žanri_nimi, autor_nimi) VALUES (?,?,?,?)"
    cursor = connection.cursor()
    cursor.execute(query, user_data)
    connection.commit()
    print("Raamat lisatud edukalt!")

def delete_raamat_query(conn, delete_raamat):
    query = "DELETE FROM Raamatud WHERE raamat_id = ?"
    cursor = connection.cursor()
    cursor.execute(query, (delete_raamat,))
    connection.commit()
    print("Raamat kustutatud edukalt!")

def update_autor_query(connection, user_data):
    query = "UPDATE Autorid SET autor_nimi = ?, sünnikuupäev = ? WHERE autor_id = ?"
    cursor = connection.cursor()
    cursor.execute(query, user_data)
    connection.commit()
    print("Autor oli redigeeritud!")

def update_zanr_query(connection, user_data):
    query = "UPDATE Zanrid SET žanri_nimi = ? WHERE žanr_id = ?"
    cursor = connection.cursor()
    cursor.execute(query, user_data)
    connection.commit()
    print("Zanr oli redigeeritud!")

def update_raamat_query(connection, user_data):
    query = "UPDATE Raamatud SET pealkiri = ?, väljaandmise_kuupäev = ?, žanri_nimi = ?, autor_nimi = ? WHERE raamat_id = ?"
    cursor = connection.cursor()
    cursor.execute(query, user_data)
    connection.commit()
    print("Raamat oli redigeeritud!")

def open_autorid_window():
    new_window = Toplevel(aken)
    new_window.title("Autorid")
    new_window.geometry("800x600")
    
    autorid = execute_read_query(conn, select_autorid)
    
    text_area = Text(new_window)
    text_area.pack(expand=True, fill='both')
    
    for autor in autorid:
        text_area.insert(END, f"{autor}\n")

def open_raamatud_window():
    new_window = Toplevel(aken)
    new_window.title("Raamatud")
    new_window.geometry("800x600")
    
    raamatud = execute_read_query(conn, select_raamatud)
    
    text_area = Text(new_window)
    text_area.pack(expand=True, fill='both')
    
    for raamat in raamatud:
        text_area.insert(END, f"{raamat}\n")

def open_zanrid_window():
    new_window = Toplevel(aken)
    new_window.title("Žanrid")
    new_window.geometry("800x600")
    
    zanrid = execute_read_query(conn, select_zanrid)
    
    text_area = Text(new_window)
    text_area.pack(expand=True, fill='both')
    
    for zanr in zanrid:
        text_area.insert(END, f"{zanr}\n")

def open_add_autor_window():
    new_window = Toplevel(aken)
    new_window.title("Lisa Autor")
    new_window.geometry("400x300")

    nimi_label = Label(new_window, text="Nimi")
    nimi_label.pack()
    nimi_entry = Entry(new_window)
    nimi_entry.pack()

    sünnikuupäev_label = Label(new_window, text="Sünnikuupäev (YYYY-MM-DD)")
    sünnikuupäev_label.pack()
    sünnikuupäev_entry = Entry(new_window)
    sünnikuupäev_entry.pack()

    def add_autor():
        nimi = nimi_entry.get()
        sünnikuupäev = sünnikuupäev_entry.get()
        add_autor_query(conn, (nimi, sünnikuupäev))
        new_window.destroy()

    submit_button = Button(new_window, text="Lisa", command=add_autor)
    submit_button.pack()

def open_delete_autor_window():
    new_window = Toplevel(aken)
    new_window.title("Kustuta Autor")
    new_window.geometry("400x200")

    id_label = Label(new_window, text="Autor ID")
    id_label.pack()
    id_entry = Entry(new_window)
    id_entry.pack()

    def delete_autor():
        autor_id = id_entry.get()
        delete_autor_query(conn, autor_id)
        new_window.destroy()

    submit_button = Button(new_window, text="Kustuta", command=delete_autor)
    submit_button.pack()

def open_add_zanr_window():
    new_window = Toplevel(aken)
    new_window.title("Lisa Žanr")
    new_window.geometry("400x200")

    nimi_label = Label(new_window, text="Žanri Nimi")
    nimi_label.pack()
    nimi_entry = Entry(new_window)
    nimi_entry.pack()

    def add_zanr():
        nimi = nimi_entry.get()
        add_zanr_query(conn, nimi)
        new_window.destroy()

    submit_button = Button(new_window, text="Lisa", command=add_zanr)
    submit_button.pack()

def open_delete_zanr_window():
    new_window = Toplevel(aken)
    new_window.title("Kustuta Žanr")
    new_window.geometry("400x200")

    id_label = Label(new_window, text="Žanr ID")
    id_label.pack()
    id_entry = Entry(new_window)
    id_entry.pack()

    def delete_zanr():
        zanr_id = id_entry.get()
        delete_zanr_query(conn, zanr_id)
        new_window.destroy()

    submit_button = Button(new_window, text="Kustuta", command=delete_zanr)
    submit_button.pack()

def open_add_raamat_window():
    new_window = Toplevel(aken)
    new_window.title("Lisa Raamat")
    new_window.geometry("400x300")

    pealkiri_label = Label(new_window, text="Pealkiri")
    pealkiri_label.pack()
    pealkiri_entry = Entry(new_window)
    pealkiri_entry.pack()

    kuupäev_label = Label(new_window, text="Väljaandmise Kuupäev (YYYY-MM-DD)")
    kuupäev_label.pack()
    kuupäev_entry = Entry(new_window)
    kuupäev_entry.pack()

    zanr_label = Label(new_window, text="Žanri Nimi")
    zanr_label.pack()
    zanr_entry = Entry(new_window)
    zanr_entry.pack()

    autor_label = Label(new_window, text="Autori Nimi")
    autor_label.pack()
    autor_entry = Entry(new_window)
    autor_entry.pack()

    def add_raamat():
        pealkiri = pealkiri_entry.get()
        kuupäev = kuupäev_entry.get()
        zanr = zanr_entry.get()
        autor = autor_entry.get()
        add_raamat_query(conn, (pealkiri, kuupäev, zanr, autor))
        new_window.destroy()

    submit_button = Button(new_window, text="Lisa", command=add_raamat)
    submit_button.pack()

def open_delete_raamat_window():
    new_window = Toplevel(aken)
    new_window.title("Kustuta Raamat")
    new_window.geometry("400x200")

    id_label = Label(new_window, text="Raamat ID")
    id_label.pack()
    id_entry = Entry(new_window)
    id_entry.pack()

    def delete_raamat():
        raamat_id = id_entry.get()
        delete_raamat_query(conn, raamat_id)
        new_window.destroy()

    submit_button = Button(new_window, text="Kustuta", command=delete_raamat)
    submit_button.pack()

def open_update_autor_window():
    new_window = Toplevel(aken)
    new_window.title("Redigeeri Autor")
    new_window.geometry("400x300")

    id_label = Label(new_window, text="Autor ID")
    id_label.pack()
    id_entry = Entry(new_window)
    id_entry.pack()

    nimi_label = Label(new_window, text="Uus Nimi")
    nimi_label.pack()
    nimi_entry = Entry(new_window)
    nimi_entry.pack()

    sünnikuupäev_label = Label(new_window, text="Uus Sünnikuupäev (YYYY-MM-DD)")
    sünnikuupäev_label.pack()
    sünnikuupäev_entry = Entry(new_window)
    sünnikuupäev_entry.pack()

    def update_autor():
        autor_id = id_entry.get()
        uus_nimi = nimi_entry.get()
        uus_sünnikuupäev = sünnikuupäev_entry.get()
        update_autor_query(conn, (uus_nimi, uus_sünnikuupäev, autor_id))
        new_window.destroy()

    submit_button = Button(new_window, text="Redigeeri", command=update_autor)
    submit_button.pack()

def open_update_zanr_window():
    new_window = Toplevel(aken)
    new_window.title("Redigeeri Žanr")
    new_window.geometry("400x200")

    id_label = Label(new_window, text="Žanr ID")
    id_label.pack()
    id_entry = Entry(new_window)
    id_entry.pack()

    nimi_label = Label(new_window, text="Uus Žanri Nimi")
    nimi_label.pack()
    nimi_entry = Entry(new_window)
    nimi_entry.pack()

    def update_zanr():
        zanr_id = id_entry.get()
        uus_nimi = nimi_entry.get()
        update_zanr_query(conn, (uus_nimi, zanr_id))
        new_window.destroy()

    submit_button = Button(new_window, text="Redigeeri", command=update_zanr)
    submit_button.pack()

def open_update_raamat_window():
    new_window = Toplevel(aken)
    new_window.title("Redigeeri Raamat")
    new_window.geometry("400x400")

    id_label = Label(new_window, text="Raamat ID")
    id_label.pack()
    id_entry = Entry(new_window)
    id_entry.pack()

    pealkiri_label = Label(new_window, text="Uus Pealkiri")
    pealkiri_label.pack()
    pealkiri_entry = Entry(new_window)
    pealkiri_entry.pack()

    kuupäev_label = Label(new_window, text="Uus Väljaandmise Kuupäev (YYYY-MM-DD)")
    kuupäev_label.pack()
    kuupäev_entry = Entry(new_window)
    kuupäev_entry.pack()

    zanr_label = Label(new_window, text="Uus Žanri Nimi")
    zanr_label.pack()
    zanr_entry = Entry(new_window)
    zanr_entry.pack()

    autor_label = Label(new_window, text="Uus Autori Nimi")
    autor_label.pack()
    autor_entry = Entry(new_window)
    autor_entry.pack()

    def update_raamat():
        raamat_id = id_entry.get()
        uus_pealkiri = pealkiri_entry.get()
        uus_kuupäev = kuupäev_entry.get()
        uus_zanr = zanr_entry.get()
        uus_autor = autor_entry.get()
        update_raamat_query(conn, (uus_pealkiri, uus_kuupäev, uus_zanr, uus_autor, raamat_id))
        new_window.destroy()

    submit_button = Button(new_window, text="Redigeeri", command=update_raamat)
    submit_button.pack()

aken = Tk()
aken.geometry("1200x800")
aken.title("Raamatukogu")

avtori = Button(aken, text="Näita Autorid", font="Algerian", height=2, width=15, relief=RAISED, command=open_autorid_window, bg="lightblue")
knigi = Button(aken, text="Näita Raamatud", font="Algerian", height=2, width=15, relief=RAISED, command=open_raamatud_window, bg="lightblue")
janri = Button(aken, text="Näita Žanrid", font="Algerian", height=2, width=15, relief=RAISED, command=open_zanrid_window, bg="lightblue")

add_autor_button = Button(aken, text="Lisa Autor", font="Algerian", height=2, width=15, relief=RAISED, command=open_add_autor_window, bg="lightgreen")
delete_autor_button = Button(aken, text="Kustuta Autor", font="Algerian", height=2, width=15, relief=RAISED, command=open_delete_autor_window, bg="red")
add_zanr_button = Button(aken, text="Lisa Žanr", font="Algerian", height=2, width=15, relief=RAISED, command=open_add_zanr_window, bg="lightgreen")
delete_zanr_button = Button(aken, text="Kustuta Žanr", font="Algerian", height=2, width=15, relief=RAISED, command=open_delete_zanr_window, bg="red")
add_raamat_button = Button(aken, text="Lisa Raamat", font="Algerian", height=2, width=15, relief=RAISED, command=open_add_raamat_window, bg="lightgreen")
delete_raamat_button = Button(aken, text="Kustuta Raamat", font="Algerian", height=2, width=15, relief=RAISED, command=open_delete_raamat_window, bg="red")

update_autor_button = Button(aken, text="Redigeeri Autor", font="Algerian", height=2, width=15, relief=RAISED, command=open_update_autor_window, bg="lightyellow")
update_zanr_button = Button(aken, text="Redigeeri Žanr", font="Algerian", height=2, width=15, relief=RAISED, command=open_update_zanr_window, bg="lightyellow")
update_raamat_button = Button(aken, text="Redigeeri Raamat", font="Algerian", height=2, width=15, relief=RAISED, command=open_update_raamat_window, bg="lightyellow")

avtori.place(x=0, y=0)
knigi.place(x=200, y=0)
janri.place(x=400, y=0)

add_autor_button.place(x=0, y=100)
delete_autor_button.place(x=200, y=100)
add_zanr_button.place(x=400, y=100)
delete_zanr_button.place(x=600, y=100)
add_raamat_button.place(x=800, y=100)
delete_raamat_button.place(x=1000, y=100)

update_autor_button.place(x=0, y=200)
update_zanr_button.place(x=200, y=200)
update_raamat_button.place(x=400, y=200)

aken.mainloop()

