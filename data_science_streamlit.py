from datetime import datetime
import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import numpy as np

# Fonction pour déterminer la saison en fonction de la date
def get_season(date):
    # Convertir la chaîne de caractères en objet datetime
    date_obj = datetime.strptime(date, "%Y-%m-%d")
    month = date_obj.month
    day = date_obj.day

    # Déterminer la saison en fonction du mois et du jour
    if (month == 3 and day >= 20) or (month == 4) or (month == 5) or (month == 6 and day < 21):
        return 'Printemps'
    elif (month == 6 and day >= 21) or (month == 7) or (month == 8) or (month == 9 and day < 23):
        return 'Été'
    elif (month == 9 and day >= 23) or (month == 10) or (month == 11) or (month == 12 and day < 21):
        return 'Automne'
    else:
        return 'Hiver'
    
    
# Fonction pour récupérer les données
def get_data():
    # Établir une connexion à la base de données
    conn = sqlite3.connect('bdd.db')

    # Récupérer les données dans un DataFrame
    query = """
        SELECT ObjetsTrouves.date , Temperatures.temperature, COUNT(*) as nb_objets
        FROM ObjetsTrouves
        JOIN Temperatures ON ObjetsTrouves.date = Temperatures.date
        GROUP BY ObjetsTrouves.date, Temperatures.temperature 
    """
    df = pd.read_sql_query(query, conn)

    # Ajouter la saison
    df['saison'] = df['date'].apply(get_season)


    return df , conn

# Fonction pour créer le scatterplot
def create_scatterplot(df):
    # Grouper les données par température et calculer le nombre total d'objets trouvés
    grouped_data = df.groupby("temperature")["nb_objets"].sum().reset_index()

    # Créer le scatterplot
    scatterplot = px.scatter(grouped_data, x="temperature", y="nb_objets", title="Nombre d'objets trouvés en fonction de la température")
    # Ajouter une ligne de régression pour visualiser la corrélation entre les deux variables
    scatterplot.add_traces(px.scatter(grouped_data, x="temperature", y="nb_objets", trendline="ols").data[1])

    return scatterplot

# Fonction pour créer le premier barplot
def create_barplot1(df):
    grouped_data = df.groupby("saison")["nb_objets"].median().apply(np.floor).reset_index()
    barplot = px.bar(grouped_data, x="saison", y="nb_objets", title="Nombre d'objets trouvés par saison")
    return barplot

# Fonction pour créer le deuxième barplot
def create_barplot2(df, conn):
    query = """SELECT date , type
    FROM ObjetsTrouves """

    df_test = pd.read_sql_query(query, conn)
    df_test['saison'] = df_test['date'].apply(get_season)
    df_test = df_test.groupby(['saison', 'type'])['date'].count().reset_index()
    df_test.rename(columns={'date': 'nb_objets'}, inplace=True)
    barplot = px.bar(df_test, x="saison", y="nb_objets", color="type", title="Nombre d'objets trouvés par saison et type d'objet", width=1200, height=600)
    return barplot

# Fonction principale pour créer l'interface utilisateur
def main():
    # Créer l'interface utilisateur
    st.title("Analyse des objets trouvés")
    st.write("Affichage du scatterplot du nombre d'objets trouvés en fonction de la température.")

    # Récupérer les données
    df , conn = get_data()
     
     
    # Créer le scatterplot
    scatterplot = create_scatterplot(df)
    # Créer le premier barplot
    barplot1 = create_barplot1(df)

    # Créer le deuxième barplot
    barplot2 = create_barplot2(df, conn)
     
    # Afficher le scatterplot
    st.plotly_chart(scatterplot)
     
    # Afficher les barplots
    st.plotly_chart(barplot1)
    st.plotly_chart(barplot2)
    
    conn.close()


if __name__ == '__main__':
    main()