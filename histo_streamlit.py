import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

def get_data(type_objet, nom_gare, annee):
    # Connexion à la base de données
    conn = sqlite3.connect('bdd_streamlit.db')
    
    if type_objet == "Tous" and nom_gare == "Toutes":
        query = f"SELECT semaine, COUNT(*) AS nb_objets FROM ObjetsTrouves WHERE annee = {annee} GROUP BY semaine"
    elif type_objet == "Tous":
        query = f"SELECT semaine, SUM(nb_objets) AS nb_objets FROM (SELECT semaine, COUNT(*) AS nb_objets FROM ObjetsTrouves WHERE nom_gare = '{nom_gare}' AND annee = {annee} GROUP BY semaine) GROUP BY semaine"
    elif nom_gare == "Toutes":
        query = f"SELECT semaine, SUM(nb_objets) AS nb_objets FROM (SELECT semaine, COUNT(*) AS nb_objets FROM ObjetsTrouves WHERE type = '{type_objet}' AND annee = {annee} GROUP BY nom_gare, semaine) GROUP BY semaine"
    else:
        query = f"SELECT semaine, COUNT(*) AS nb_objets FROM ObjetsTrouves WHERE type = '{type_objet}' AND nom_gare = '{nom_gare}' AND annee = {annee} GROUP BY semaine"

    # Récupération des données dans un DataFrame
    df = pd.read_sql_query(query, conn)

    # Fermeture de la connexion à la base de données
    conn.close()

    return df


# Fonction pour créer une visualisation interactive avec Plotly
def create_plot(type_objet, nom_gare, annee):
    df = get_data(type_objet, nom_gare, annee)
    if type_objet == "Tous" and nom_gare == "Toutes":
        title = f"Nombre d'objets trouvés par semaine pour l'année {annee} dans les gares parisiennes"
    elif type_objet == "Tous" and nom_gare != "Toutes":
        title = f"Nombre total d'objets trouvés par semaine pour l'année {annee} à {nom_gare}"
    elif type_objet != "Tous" and nom_gare != "Toutes":
        title = f'Nombre de "{type_objet}" trouvé.e.s par semaine pour l\'année {annee} à {nom_gare}'
    else:
        title = f'Nombre de "{type_objet}" trouvé.e.s par semaine pour l\'année {annee}'
    fig = px.histogram(df, x="semaine", y="nb_objets", nbins=50, title=title, labels={"semaine": "Numéro de semaine", "nb_objets": "Nombre d'objets trouvés"})
    return fig


# Connexion à la base de données
conn = sqlite3.connect('bdd_streamlit.db')
    
# Récupération des données dans un DataFrame
df = pd.read_sql_query("SELECT * FROM ObjetsTrouves", conn)
    
# Fermeture de la connexion à la base de données
conn.close()

# Interface utilisateur avec Streamlit
st.title("Analyse des objets trouvés dans les gares")

# Options de filtrage
type_objet = st.selectbox("Type d'objet", ["Tous"] + list(df['type'].unique()))
nom_gare = st.selectbox("Nom de la gare", ["Toutes"] + list(df['nom_gare'].unique()))
annee = st.slider("Année", 2019, 2022, 2019)

# Création du graphique
fig = create_plot(type_objet, nom_gare, annee)

# Affichage du graphique
st.write("Graphique :")
st.plotly_chart(fig)
