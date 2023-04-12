import sqlite3

connexion = sqlite3.connect("bdd.db")
curseur = connexion.cursor()

curseur.execute("""
                CREATE TABLE IF NOT EXISTS ObjetsTrouves (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    type TEXT NOT NULL,
                    nom_gare TEXT NOT NULL,
                    date DATETIME NOT NULL,
                    annee INTEGER,
                    semaine INTEGER,
                    FOREIGN KEY(date) REFERENCES Temperatures(date)
                    FOREIGN KEY(nom_gare) REFERENCES Gares(nom_gare)
                )
                """)
connexion.commit()


curseur.execute("""
                CREATE TABLE IF NOT EXISTS Temperatures (
                    date DATETIME PRIMARY KEY,
                    temperature INTEGER NOT NULL
                )
                """)
connexion.commit()

curseur.execute("""
                CREATE TABLE IF NOT EXISTS Gares (
                    nom_gare TEXT PRIMARY KEY,
                    frequentation_2019 INTEGER NOT NULL,
                    frequentation_2020 INTEGER NOT NULL,
                    frequentation_2021 INTEGER NOT NULL,
                    frequentation_2022 INTEGER NOT NULL,
                    latitude FLOAT,
                    longitude FLOAT 
                )
                """)
connexion.commit()

connexion.close()