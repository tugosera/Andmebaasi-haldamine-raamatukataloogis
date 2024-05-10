from sqlite3 import * 
from sqlite3 import Error
import sqlite3

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
        print (f"Viga '{e}'tabeli loomisega")


create_autori_table = """
CREATE TABLE IF NOT EXISTS Autorid (
autor_id INTEGER PRIMARY KEY AUTOINCREMENT,
autor_nimi TEXT NOT NULL,
sünnikuupäev DATE NOT NULL
);
"""

execute_query(conn, create_autori_table)

def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"viga '{e}'")

create_autori = """
INSERT INTO Autorid (autor_nimi, sünnikuupäev)
VALUES
("William Shakespeare","1564-04-26"),
("Fjodor Dostojevski","1821-11-11"),
("Jane Austin","1775-12-16"),
("Miguel de Cervantes", "1547-09-29"),
("Charles Dickens", "1812-02-07");
"""

#execute_query(conn, create_autori)

select_autorid = "SELECT * from Autorid"

Autorid = execute_read_query(conn, select_autorid)
for autor in Autorid:
    print(autor)

def add_autor_query(connection, user_data):
    query = "INSERT INTO Autorid(autor_nimi, sünnikuupäev) VALUES (?,?)"
    cursor = connection.cursor()
    cursor.execute(query, user_data)
    connection.commit()
    print("Autor lisatud edukalt!")

a=int (input("Kas tahad lisada autori? (1=ja, 2=ei)"))
if a == 1:

    insert_autor=(input("Nimi: "),input("sünnikuupäev(year-month-day): "))
    print(insert_autor)
    add_autor_query(conn,insert_autor)
elif a == 2:
    print("ladn")

def delete_data_from_tabelautor(connection, query):
    try:
        cursor=connection.cursor()
        cursor.execute(query)
        connection.commit()
        print("Andmed on kustutatud")
    except Error as e:
        print(f"Viga '{e}' andmete kustutamisega")

def delete_autor_query(conn, (delete_autor,)):
    query = "DELETE FROM Autorid WHERE autor_id = ?"
    cursor = connection.cursor()
    cursor.execute(query, delete_autor)
    connection.commit()
    print("Autor kustutatud edukalt!")

delete_autor = input("Id: ")
print(delete_autor)
delete_autor_query(conn, delete_autor)
