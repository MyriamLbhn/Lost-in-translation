import requests
import sqlite3
import re
from datetime import datetime, date
import logging

import pandas as pd

logging.basicConfig(level=logging.INFO)

def ajouter_objets_trouves_a_bdd():
    gares_parisiennes = ["Paris Gare de Lyon", "Paris Montparnasse", "Paris Gare du Nord", "Paris Est" , "Paris Saint-Lazare" , "Paris Austerlitz" , 'Paris Bercy']
    annees = ["2019", "2020" , "2021" , "2022"]

    connexion = sqlite3.connect("bdd.db")
    curseur = connexion.cursor()

    for gare in gares_parisiennes:
        for annee in annees:
            logging.info(f"Récupération des données pour la gare {gare} en {annee}")
            response = requests.get(f"https://ressources.data.sncf.com/api/records/1.0/search/?dataset=objets-trouves-restitution&q=&rows=-1&sort=-date&facet=date&facet=gc_obo_date_heure_restitution_c&facet=gc_obo_gare_origine_r_name&facet=gc_obo_nature_c&facet=gc_obo_type_c&facet=gc_obo_nom_recordtype_sc_c&refine.gc_obo_gare_origine_r_name={gare}&refine.date={annee}")

            records = response.json()["records"]

            for record in records:
                fields = record["fields"]
                date_string = fields["date"]
                date_string = re.sub(r'\+\d\d:\d\d$', '', date_string)  # Supprime le décalage horaire
                date = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S").strftime('%Y-%m-%d %H:%M:%S')
                type_objet = fields["gc_obo_nature_c"]
                nom_gare = fields["gc_obo_gare_origine_r_name"]
                annee = pd.to_datetime(date).year
                semaine = pd.to_datetime(date).isocalendar().week

                curseur.execute("""
                                INSERT INTO ObjetsTrouves (type, nom_gare, date, annee, semaine)
                                VALUES (?, ?, ?, ?, ?)
                                """, (type_objet, nom_gare, date, annee, semaine))

    connexion.commit()
    connexion.close()


def update_objets_trouves_a_bdd():
    gares_parisiennes = ["Paris Gare de Lyon", "Paris Montparnasse", "Paris Gare du Nord", "Paris Est" , "Paris Saint-Lazare" , "Paris Austerlitz" , 'Paris Bercy']

    # Connexion à la base de données et récupération de la dernière date enregistrée
    connexion = sqlite3.connect("bdd.db")
    curseur = connexion.cursor()
    curseur.execute("SELECT MAX(date) FROM ObjetsTrouves")
    last_date_string = curseur.fetchone()[0]
    last_date = datetime.strptime(last_date_string, '%Y-%m-%d %H:%M:%S') if last_date_string else datetime(2019, 1, 1)
    connexion.close()

    # Récupération des données depuis la dernière date jusqu'à aujourd'hui
    date_today = datetime.today()
    date_start = last_date.date()
    date_end = date_today.date()

    # Insertion des données dans la base de données
    connexion = sqlite3.connect("bdd.db")
    curseur = connexion.cursor()

    for gare in gares_parisiennes:
        logging.info(f"Récupération des données pour la gare {gare} depuis {date_start} jusqu'à {date_end}")
        response = requests.get(f"https://ressources.data.sncf.com/api/records/1.0/search/?dataset=objets-trouves-restitution&q=&rows=-1&sort=-date&facet=date&facet.range=date&facet=gc_obo_date_heure_restitution_c&facet=gc_obo_gare_origine_r_name&facet=gc_obo_nature_c&facet=gc_obo_type_c&facet=gc_obo_nom_recordtype_sc_c&refine.gc_obo_gare_origine_r_name={gare}&facet.range.start={date_start}&facet.range.end={date_end}")

        records = response.json()["records"]
           
        for record in records:
            fields = record["fields"]
            date_string = fields["date"]
            date_string = re.sub(r'\+\d\d:\d\d$', '', date_string)  # Supprime le décalage horaire
            date = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S").strftime('%Y-%m-%d %H:%M:%S')
            type_objet = fields["gc_obo_nature_c"]
            nom_gare = fields["gc_obo_gare_origine_r_name"]
            annee = pd.to_datetime(date).year
            semaine = pd.to_datetime(date).isocalendar().week

            curseur.execute("""
                            INSERT INTO ObjetsTrouves (type, nom_gare, date, annee, semaine)
                            VALUES (?, ?, ?, ?, ?)
                            """, (type_objet, nom_gare, date, annee, semaine))

    connexion.commit()
    connexion.close()

 
# ajouter_objets_trouves_a_bdd()           
update_objets_trouves_a_bdd()