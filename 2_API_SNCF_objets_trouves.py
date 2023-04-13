import requests
import sqlite3
import re
from datetime import datetime
import logging

import pandas as pd

logging.basicConfig(level=logging.INFO)

annees = []
current_year = datetime.now().year

for year in range(2019, current_year + 1):
    annees.append(str(year))
    
gares_parisiennes = ["Paris Gare de Lyon", "Paris Montparnasse", "Paris Gare du Nord", "Paris Est" , "Paris Saint-Lazare" , "Paris Austerlitz" , 'Paris Bercy']

    
def ajouter_objets_trouves():
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
                
                # Obtenir le numéro de semaine correspondant à la date
                semaine = pd.to_datetime(date).isocalendar().week

                # Vérifier si la semaine correspond à la dernière semaine de l'année précédente
                if semaine in[52,53] and pd.to_datetime(date).strftime('%Y') != str(annee):
                    semaine = 0




                curseur.execute("""
                                INSERT INTO ObjetsTrouves (type, nom_gare, date, annee, semaine)
                                VALUES (?, ?, ?, ?, ?)
                                """, (type_objet, nom_gare, date, annee, semaine))

    connexion.commit()
    connexion.close()


def update_objets_trouves_current_year():
    # Connexion à la base de données et récupération de l'année en cours
    connexion = sqlite3.connect("bdd.db")
    curseur = connexion.cursor()
    current_year = datetime.now().year
    
    # Effacer toutes les données de l'année en cours
    curseur.execute(f"DELETE FROM ObjetsTrouves WHERE annee = {current_year}")
    connexion.commit()
    
    # Récupération des données pour l'année en cours
    logging.info(f"Récupération des données pour l'année en cours")
    for gare in gares_parisiennes:
        response = requests.get(f"https://ressources.data.sncf.com/api/records/1.0/search/?dataset=objets-trouves-restitution&q=&rows=-1&sort=-date&facet=date&facet=gc_obo_date_heure_restitution_c&facet=gc_obo_gare_origine_r_name&facet=gc_obo_nature_c&facet=gc_obo_type_c&facet=gc_obo_nom_recordtype_sc_c&refine.gc_obo_gare_origine_r_name={gare}&refine.date={current_year}")
        
        records = response.json()["records"]
        for record in records:
            fields = record["fields"]
            date_string = fields["date"]
            date_string = re.sub(r'\+\d\d:\d\d$', '', date_string)  # Supprime le décalage horaire
            date = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S").strftime('%Y-%m-%d %H:%M:%S')
            type_objet = fields["gc_obo_nature_c"]
            nom_gare = fields["gc_obo_gare_origine_r_name"]
            semaine = pd.to_datetime(date).isocalendar().week
            
            curseur.execute("""
                            INSERT INTO ObjetsTrouves (type, nom_gare, date, annee, semaine)
                            VALUES (?, ?, ?, ?, ?)
                            """, (type_objet, nom_gare, date, current_year, semaine))

    connexion.commit()
    connexion.close()


# def delete_entry(date):
#     connexion = sqlite3.connect("bdd.db")
#     cursor = connexion.cursor()

#     # convertir la date en format datetime
#     date_obj = datetime.strptime(date, '%Y-%m-%d').date()

#     # supprimer les entrées à partir de la date indiquée jusqu'à aujourd'hui
#     cursor.execute("""
#                     DELETE FROM ObjetsTrouves
#                         WHERE date >= ?
#                     """, (date_obj,))

#     connexion.commit()
#     connexion.close()

ajouter_objets_trouves()