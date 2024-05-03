from os import path
from tkinter import *
import sqlite3
from sqlite3 import connect, Error

def createConnection(path:str):
    connection = None
    try:
        connection = connect(path)
        print("Ühendus on olemas!")
    except Error as e:
        print(f"Tekkis viga: {e}")
    return connection

def initializeDatabase(connection):
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Autorid (
            autor_id INTEGER PRIMARY KEY AUTOINCREMENT,
            autor_nimi TEXT NOT NULL,
            sünnikuupäev DATE NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Žanrid (
            žanr_id INTEGER PRIMARY KEY AUTOINCREMENT,
            žanri_nimi TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Raamatud (
            raamat_id INTEGER PRIMARY KEY AUTOINCREMENT,
            pealkiri TEXT NOT NULL,
            väljaandmise_kuupäev DATE NOT NULL,
            žanri_nimi TEXT,
            autor_nimi TEXT,
            FOREIGN KEY (žanri_nimi) REFERENCES Žanrid (žanri_nimi),
            FOREIGN KEY (autor_nimi) REFERENCES Autorid (autor_nimi)
        )
    ''')

    cursor.execute('''
        INSERT INTO Autorid (autor_nimi, sünnikuupäev)
        VALUES ("William Shakespeare","1564-04-26"),
               ("Fjodor Dostojevski","1821-11-11"),
               ("Jane Austin","1775-12-16"),
               ("Miguel de Cervantes", "1547-09-29"),
               ("Charles Dickens", "1812-02-07")
    ''')

    cursor.execute('''
        INSERT INTO Žanrid (žanri_nimi)
        VALUES ("Tragöödia"),
               ("Romaan"),
               ("Romantiline proosa"),
               ("Seiklusromaan"),
               ("Sotsiaalne romaan")
    ''')

    cursor.execute('''
        INSERT INTO Raamatud (pealkiri, väljaandmise_kuupäev, žanri_nimi, autor_nimi)
        VALUES ("Hamlet", "2024-04-26", "Tragöödia", "William Shakespeare"),
               ("Kuritegu ja karistus", "2024-02-13", "Romaan", "Fjodor Dostojevski"),
               ("Emma", "2024-03-06", "Romantiline proosa", "Jane Austin"),
               ("Don Quijote", "2024-05-03","Seiklusromaan", "Miguel de Cervantes"),
               ("Oliver Twist", "2024-05-01", "Sotsiaalne romaan", "Charles Dickens")
    ''')

    connection.commit()

def readQuery(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        if cursor:
            cursor.execute(query)
            result = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Error occurred: {e}")
    return result

def showAutorid(connection, raam):
    q = 50
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Autorid")
    autorid = cursor.fetchall()
    for i, autor in enumerate(autorid):
        a = Label(raam, text=str(autor))
        q += 20
        a.place(x=0, y=q)

raam = Tk()
raam.title("Ramatukogu")
tahvel = Canvas(raam, width=750, height=600, background="white")
tahvel.grid()

dbFilename = "data.db"
dbPath = path.join(path.dirname(__file__), dbFilename)
connection = createConnection(dbPath)
initializeDatabase(connection)

nuppAutorid = Button(raam,
                     text="Показать авторов",
                     font="Algerian",
                     height=2, 
                     width=15,
                     relief=RAISED,
                     command=lambda:showAutorid(connection, raam),
                     bg="lightblue")
nuppAutorid.place(x=0, y=0)

raam.mainloop()