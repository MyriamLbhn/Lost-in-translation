import sqlite3
import pandas as pd

def scatterplot_temp():
    # Connexion à la base de données
    conn = sqlite3.connect('bdd.db')

    # Chargement des données de la table ObjetsTrouves dans un DataFrame
    objets_df = pd.read_sql_query('SELECT date, COUNT(*) as nb_objets FROM ObjetsTrouves GROUP BY date', conn)

    # Chargement des données de la table Temperatures dans un DataFrame
    temps_df = pd.read_sql_query('SELECT date, temperature FROM Temperatures', conn)

    # Convertir les colonnes "date" en objet datetime et les reformater au format "YYYY-MM-DD"
    objets_df['date'] = pd.to_datetime(objets_df['date']).dt.strftime('%Y-%m-%d')
    temps_df['date'] = pd.to_datetime(temps_df['date']).dt.strftime('%Y-%m-%d')

    # Groupby sur la colonne date pour avoir la somme des entrées pour les objets par date
    objets_df = objets_df.groupby('date')['nb_objets'].sum().reset_index()

    # Groupby sur la colonne date pour avoir la température moyenne par date
    temps_df = temps_df.groupby('date')['temperature'].mean().reset_index()

    # Fusion des deux DataFrames sur la colonne date
    df = pd.merge(objets_df, temps_df, on='date', how='inner')

    # Fermeture de la connexion à la base de données
    conn.close()

    return df




