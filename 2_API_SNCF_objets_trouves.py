import requests
import sqlite3
import pandas as pd
import re
from datetime import datetime

gares_parisiennes = ["Paris Gare de Lyon", "Paris Montparnasse", "Paris Gare du Nord", "Paris Est" , "Paris Saint-Lazare" , "Paris Austerlitz" , 'Paris Bercy']
annees = ["2019", "2020" , "2021" , "2022"]

connexion = sqlite3.connect("bdd.db")
curseur = connexion.cursor()

i = 0
for gare in gares_parisiennes:
    for annee in annees:
        print(i)
        response = requests.get(f"https://ressources.data.sncf.com/api/records/1.0/search/?dataset=objets-trouves-restitution&q=&rows=-1&sort=-date&facet=date&facet=gc_obo_date_heure_restitution_c&facet=gc_obo_gare_origine_r_name&facet=gc_obo_nature_c&facet=gc_obo_type_c&facet=gc_obo_nom_recordtype_sc_c&refine.gc_obo_gare_origine_r_name={gare}&refine.date={annee}")
        
        records = response.json()["records"]

        for record in records:
            fields = record["fields"]
            date_string = fields["date"]
            date_string = re.sub(r'\+\d\d:\d\d$', '', date_string)  # Supprime le décalage horaire
            date = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S").strftime('%Y-%m-%d %H:%M:%S')
            type_objet = fields["gc_obo_nature_c"]
            nom_gare = fields["gc_obo_gare_origine_r_name"]

            curseur.execute("""
                            INSERT INTO ObjetsTrouves (type, nom_gare, date)
                            VALUES (?, ?, ?)
                            """, (type_objet, nom_gare, date))
        i += 1

connexion.commit()

# Ajout des colonnes année et semaine

df = pd.read_sql_query('SELECT * FROM ObjetsTrouves', connexion)

df['annee'] = pd.to_datetime(df['date']).dt.year
df['semaine'] = pd.to_datetime(df['date']).dt.isocalendar().week


df.to_sql('ObjetsTrouves', connexion, if_exists='replace', index=False)

connexion.close()