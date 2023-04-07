import sqlite3
import csv

connexion = sqlite3.connect("bdd.db")
curseur = connexion.cursor()

with open("data_meteo_paris.csv", "r") as csvfile:
    reader=csv.reader(csvfile)
    next(reader, None)
    for row in reader:
        date=row[0]
        temperature=int(row[1])
        
        curseur.execute("""
                        INSERT INTO Temperatures (date, temperature)
                        VALUES (?, ?)
                        """, (date, temperature))

connexion.commit()
connexion.close()