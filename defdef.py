from os import path
from tkinter import *
import sqlite3
from sqlite3 import connect, Error

selectAutorid = "SELECT * FROM Autorid"
selectŽanrid = "SELECT * FROM Žanrid"
selectRaamatud = "SELECT * FROM Raamatud"

def createConnection(path:str):
    connection = None
    try:
        connection = connect(path)
        print("Ühendus on olemas!")
    except Error as e:
        print(f"Tekkis viga: {e}")
    return connection

filename = path.abspath(__file__)
dbDirectory = filename.rstrip('Töö andmebaasiga.py')
dbPath = path.join(dbDirectory, "data.db")
connection = createConnection(dbPath)


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



def showŽanrid():
    Žanrid = readQuery(connection, selectŽanrid)
    for Žaner in Žanrid:
        print(Žanrid)
    print()

def showRaamatud():
    Raamatud = readQuery(connection, selectRaamatud)
    for raamat in Raamatud:
        print(Raamatud)
    print()
