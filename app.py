import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import folium_static
import branca
import datetime
from API_SNCF_objets_trouves import update_objets_trouves_current_year

def get_data(query):
    conn = sqlite3.connect('bdd.db')
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

query_all_data = "SELECT * FROM ObjetsTrouves"
df = get_data(query_all_data)

def create_plot(df, title):
    fig = px.bar(df, x="semaine", y="nb_objets", title=title, labels={"semaine": "Numéro de semaine", "nb_objets": "Nombre d'objets trouvés"})
    return fig

def create_map(data, year):
    m = folium.Map(location=[48.856614, 2.3522219], zoom_start=12)
    for row in data:
        frequentation, nb_objets_trouves = row[3], row[4]
        if year == 2023:
            html = f"<h4>{row[0]}</h4><p>Fréquentation {year} : Inconnue</p><p>Objets trouvés : {nb_objets_trouves}</p>"
        else:
            html = f"<h4>{row[0]}</h4><p>Fréquentation {year} : {frequentation}</p><p>Objets trouvés : {nb_objets_trouves}</p>"
        iframe = branca.element.IFrame(html=html, width=200, height=100)
        popup = folium.Popup(iframe, max_width=2650)
        marker = folium.Marker(location=[row[1], row[2]], popup=popup, icon=folium.Icon(color="blue"))
        marker.add_to(m)
    return m


st.title("Analyse des objets trouvés dans les gares")


# Ajout du bouton "Mettre à jour la base de données"
update_button = st.button("Mettre à jour la base de données")

# Si le bouton est cliqué, mettez à jour la base de données
if update_button:
    with st.spinner("Mise à jour de la base de données..."):
        update_objets_trouves_current_year()
    st.success("Base de données mise à jour avec succès.")

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

fig = create_plot(df, title)
st.write("Graphique :")
st.plotly_chart(fig)

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


import sqlite3
import pandas as pd

# Connexion à la base de données
conn = sqlite3.connect('bdd.db')

# Chargement des données de la table ObjetsTrouves dans un DataFrame
objets_df = pd.read_sql_query('SELECT date, COUNT(*) as nb_objets FROM ObjetsTrouves GROUP BY date', conn)

# Chargement des données de la table Temperatures dans un DataFrame
temps_df = pd.read_sql_query('SELECT date, temperature FROM Temperatures', conn)

# Fusion des deux DataFrames sur la colonne date
df = pd.merge(objets_df, temps_df, on='date', how='inner')

# Fermeture de la connexion à la base de données
conn.close()

import streamlit as st
import altair as alt

# Affichage du scatterplot
scatterplot = alt.Chart(df).mark_circle().encode(
    x='temperature',
    y='nb_objets'
)

st.altair_chart(scatterplot, use_container_width=True)

# Calcul de la corrélation entre la température et le nombre d'objets trouvés
corr = df['temperature'].corr(df['nb_objets'])
st.write(f'Corrélation entre la température et le nombre d\'objets trouvés : {corr:.2f}')

