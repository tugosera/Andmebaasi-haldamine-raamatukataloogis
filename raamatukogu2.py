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

create_autori = """
INSERT INTO Autorid (autor_nimi, sünnikuupäev)
VALUES
("William Shakespeare","1564-04-26"),
("Fjodor Dostojevski","1821-11-11"),
("Jane Austin","1775-12-16"),
("Miguel de Cervantes", "1547-09-29"),
("Charles Dickens", "1812-02-07");
"""

create_zanri = '''
        INSERT INTO Zanrid (žanri_nimi)
        VALUES ("Tragöödia"),
               ("Romaan"),
               ("Romantiline proosa"),
               ("Seiklusromaan"),
               ("Sotsiaalne romaan")
    '''
    
create_raamatu = '''
        INSERT INTO Raamatud (pealkiri, väljaandmise_kuupäev, žanri_nimi, autor_nimi)
        VALUES ("Hamlet", "2024-04-26", "Tragöödia", "William Shakespeare"),
               ("Kuritegu ja karistus", "2024-02-13", "Romaan", "Fjodor Dostojevski"),
               ("Emma", "2024-03-06", "Romantiline proosa", "Jane Austin"),
               ("Don Quijote", "2024-05-03","Seiklusromaan", "Miguel de Cervantes"),
               ("Oliver Twist", "2024-05-01", "Sotsiaalne romaan", "Charles Dickens")
    '''
# execute_query(conn, create_zanri)
# execute_query(conn, create_raamatu)
# execute_query(conn, create_autori)

select_autorid = "SELECT * from Autorid"
select_zanrid = "SELECT * from Zanrid"
select_raamatud = "SELECT * from Raamatud"

def add_zanr_query(connection, user_data):
    query = "INSERT INTO Zanrid(žanri_nimi) VALUES (?)"
    cursor = connection.cursor()
    cursor.execute(query, user_data)
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
    
def delete_data_from_tabelautor(connection, query):
    try:
        cursor=connection.cursor()
        cursor.execute(query)
        connection.commit()
        print("Andmed on kustutatud")
    except Error as e:
        print(f"Viga '{e}' andmete kustutamisega")

while True:
    a=int (input("Че делать ? (0=покажи авторов, 1=добавь автора, 2=удали автора, 3=покажи жанры, 6=покажи книги) \n"))
    if a == 0:
        Autorid = execute_read_query(conn, select_autorid)
        for autor in Autorid:
            print(autor)
    
    elif a == 1:
        insert_autor=(input("Nimi: "),input("sünnikuupäev(year-month-day): "))
        print(insert_autor)
        add_autor_query(conn,insert_autor)
    
    elif a == 2:
        delete_autor = input("Id: ")
        print(delete_autor)
        delete_autor_query(conn, delete_autor)
        
    elif a == 3:
        Zanrid = execute_read_query(conn, select_zanrid)
        for Zanr in Zanrid:
            print(Zanr)
            
    elif a == 4: 
        insert_zanr=(input("zanrti nimi: "))
        print(insert_zanr)
        add_zanr_query(conn,insert_zanr)
        
    # elif a == 5:
            
    elif a == 6:
        Raamatud = execute_read_query(conn, select_raamatud)
        for Raamat in Raamatud:
            print(Raamat)
        

