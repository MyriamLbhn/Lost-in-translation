import streamlit as st
import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
from streamlit_folium import folium_static
import datetime
import altair as alt
from scatterplot import scatterplot_temp
from API_SNCF_objets_trouves import update_objets_trouves_current_year
from functions_analyse_visualisation import create_map
from histo_streamlit import get_data, create_plot

def page1():
    st.title("Analyse des objets trouvés dans les gares")


    #bouton "Mettre à jour la base de données"
    update_button = st.button("Mettre à jour la base de données")

    # Si le bouton est cliqué, mettez à jour la base de données
    if update_button:
        with st.spinner("Mise à jour de la base de données..."):
            update_objets_trouves_current_year()
        st.success("Base de données mise à jour avec succès.")
        
    # Menu de selection
    query_all_data = "SELECT * FROM ObjetsTrouves"
    df = get_data(query_all_data)
    type_objet = st.selectbox("Type d'objet", ["Tous"] + list(df['type'].unique()))
    nom_gare = st.selectbox("Nom de la gare", ["Toutes"] + list(df['nom_gare'].unique()))
    annee_en_cours = datetime.datetime.now().year
    annee = st.slider("Année", 2019, annee_en_cours)

    query = f"SELECT semaine, COUNT(*) AS nb_objets FROM ObjetsTrouves WHERE annee = {annee}"
    if type_objet != "Tous": query += f" AND type = '{type_objet}'"
    if nom_gare != "Toutes": query += f" AND nom_gare = '{nom_gare}'"
    query += " GROUP BY semaine"
    df = get_data(query)

    title = f"Nombre d'objets trouvés par semaine pour l'année {annee}"
    if type_objet != "Tous": title += f' de type "{type_objet}"'
    if nom_gare != "Toutes": title += f' à la gare "{nom_gare}"'


    # Affichage de l'histogramme du nombre d'objets trouvées par semaine par an
    fig = create_plot(df, title)
    st.write("Graphique :")
    st.plotly_chart(fig)


    #
    query = f"""
    SELECT ObjetsTrouves.nom_gare, Gares.latitude, Gares.longitude, """
    if annee != 2023:
        query += f"Gares.frequentation_{annee}, "
    else:
        query += "NULL as frequentation, "
    query += f"""COUNT(*)
    FROM ObjetsTrouves
    JOIN Gares ON ObjetsTrouves.nom_gare = Gares.nom_gare
    WHERE strftime('%Y', ObjetsTrouves.date) = '{annee}'
    """
    if type_objet != "Tous": query += f" AND ObjetsTrouves.type = '{type_objet}'"
    query += " GROUP BY ObjetsTrouves.nom_gare"
    data = get_data(query).to_numpy()
    m = create_map(data, annee)

    st.title("Carte des objets trouvés en fonction de la fréquentation des gares")
    # si on montre toutes les gares, on affiche nombre de tous les objets trouvés dans les gares
    if type_objet == "Tous" and nom_gare == "Toutes" or type_objet != "Tous":
        st.write("Voici la carte des objets trouvés en fonction de la fréquentation des gares pour l'année " + str(annee) + ".")
    else:
        st.write("Voici la carte des objets trouvés en fonction de la fréquentation des gares pour l'année " + str(annee) + ".")
        st.write("Pour l'objet " + type_objet + ".")
    st.write("")
    folium_static(m)



def page2():
# Fonction pour déterminer la saison en fonction de la date
    def get_season(date):
        # Convertir la chaîne de caractères en objet datetime
        date_obj = datetime.datetime.strptime(date, '%Y-%m-%d')
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

    def create_boxplot(df):
        boxplot = px.box(df, x="saison", y="nb_objets", title="Nombre d'objets trouvés par saison")
        return boxplot

    # Fonction pour créer le deuxième barplot
    def create_barplot2(df, conn):
        query = """SELECT date , type
        FROM ObjetsTrouves """

        df_test = pd.read_sql_query(query, conn)
        df_test['saison'] = df_test['date'].apply(get_season)
        df_test = df_test.groupby(['saison', 'type'])['date'].count().reset_index()
        df_test.rename(columns={'date': 'nb_objets'}, inplace=True)
        barplot = px.bar(df_test, x="saison", y="nb_objets", color="type", title="Nombre d'objets trouvés par saison et type d'objet", width=1000, height=600)
        return barplot


    # Créer l'interface utilisateur
    st.title("Analyse des objets trouvés")
    st.write("Affichage du scatterplot du nombre d'objets trouvés en fonction de la température.")

    # Récupérer les données
    df , conn = get_data()
        
        
    # Créer le scatterplot
    scatterplot = create_scatterplot(df)
    # Créer le premier barplot
    barplot1 = create_boxplot(df)

    # Créer le deuxième barplot
    barplot2 = create_barplot2(df, conn)
        
    # Afficher le scatterplot
    st.plotly_chart(scatterplot)
        
    # Afficher les barplots
    st.plotly_chart(barplot1)
    st.plotly_chart(barplot2)

    conn.close()


# Créez une barre latérale avec des options pour sélectionner la page
st.sidebar.title("Navigation")
page = st.sidebar.radio("Aller à", ["Page 1", "Page 2"])

# Affichez le contenu de la page sélectionnée
if page == "Page 1":
    page1()
elif page == "Page 2":
    page2()