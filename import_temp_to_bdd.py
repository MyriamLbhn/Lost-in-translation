import sqlite3
import csv
import pandas as pd
import requests
import os
from os.path import join, dirname
from dotenv import load_dotenv
from datetime import datetime, timedelta
import logging


def ajouter_temperatures_bdd():
    dotenv_path = join(dirname("LOST-IN-TRANSLATION"), '.env')
    load_dotenv(dotenv_path)

    API_KEY = os.environ.get("API_KEY")

    # Définir les paramètres de la requête API
    url = "http://api.worldweatheronline.com/premium/v1/past-weather.ashx"
    params = {
        "key": API_KEY,
        "q": "Paris",
        "format": "json",
        "tp": "24", # Pour une moyenne quotidienne
    }

    # Initialiser des listes vides pour stocker les données
    date = []
    avgtempC = []

    # Boucle pour récupérer les données par tranches de 33 jours jusqu'au 31 décembre 2022
    start_date = datetime.strptime("2019-01-01", "%Y-%m-%d")
    end_date = datetime.strptime("2022-12-31", "%Y-%m-%d")
    while start_date <= end_date:
        # Calculer la date de fin de la tranche de 33 jours
        next_end_date = start_date + timedelta(days=32)
        if next_end_date > end_date:
            next_end_date = end_date
        # Ajouter la date de début et la date de fin à la requête API
        params["date"] = start_date.strftime("%Y-%m-%d")
        params["enddate"] = next_end_date.strftime("%Y-%m-%d")
        # Envoyer une requête à l'API et stocker la réponse dans une variable
        response = requests.get(url, params=params)
        # Extraire les données d'intérêt de la réponse JSON
        data = response.json()["data"]["weather"]
        # Parcourir les données et ajouter chaque valeur dans sa liste correspondante
        for day in data:
            date.append(day["date"])
            avgtempC.append(day["avgtempC"])
        # Mettre à jour la date de début pour la prochaine tranche de 33 jours
        start_date = next_end_date + timedelta(days=1)

    # Stocker les données dans un DataFrame pandas
    df = pd.DataFrame({
        "date": date,
        "temperature": avgtempC,
    })

    # Écrire les données dans la base de données
    connexion = sqlite3.connect("bdd.db")
    
    logging.basicConfig(level=logging.INFO)

    df.to_sql(name="Temperatures", con=connexion, if_exists="append", index=False)
    logging.info("Données insérées avec succès dans la table 'Temperatures' de la base de données")
    
    connexion.commit()
    connexion.close()

