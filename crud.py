import sqlite3

def new_gare(nom_gare:str, frequentation_2019:str, frequentation_2020:str, frequentation_2021:str, frequentation_2022:str, latitude:float, longitude:float) -> int:
    connexion = sqlite3.connect("bdd.db")
    curseur = connexion.cursor()

    curseur.execute("""
                INSERT INTO Gares (nom_gare, frequentation_2019, frequentation_2020, frequentation_2021, frequentation_2022, latitude, longitude)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (nom_gare, frequentation_2019, frequentation_2020, frequentation_2021, frequentation_2022, latitude, longitude))
    
    connexion.commit()
    connexion.close()

# new_gare("Paris Gare de Lyon",140121852, 67873723,100871407,100871407,48.844304,2.374377)
# new_gare("Paris Montparnasse", 76622754, 40615322, 51406616, 5140616, 48.841020, 2.320378)
# new_gare("Paris Saint-Lazare", 143120561, 152624513, 122002923, 122002923, 48.876301, 2.325402)
# new_gare("Paris Bercy", 4482042, 2592964,3474572, 3474572, 48.840050, 2.381668)
# new_gare("Paris Gare du Nord", 272898471, 107666015, 148849186, 148849186, 48.880948, 2.355314)
# new_gare("Paris Est", 52060520, 27242868, 35041906, 35041906, 48.876790, 2.359284 )
# new_gare("Paris Austerlitz", 22423095, 13602554,22814864, 22814864,48.842946, 2.364951)