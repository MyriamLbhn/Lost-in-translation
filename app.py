import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import folium_static
import branca



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
        html = f"<h4>{row[0]}</h4><p>Fréquentation {year} : {frequentation}</p><p>Objets trouvés : {nb_objets_trouves}</p>"
        iframe = branca.element.IFrame(html=html, width=200, height=100)
        popup = folium.Popup(iframe, max_width=2650)
        marker = folium.Marker(location=[row[1], row[2]], popup=popup, icon=folium.Icon(color="blue"))
        marker.add_to(m)
    return m

st.title("Analyse des objets trouvés dans les gares")

type_objet = st.selectbox("Type d'objet", ["Tous"] + list(df['type'].unique()))
nom_gare = st.selectbox("Nom de la gare", ["Toutes"] + list(df['nom_gare'].unique()))
annee = st.slider("Année", 2019, 2022, 2019)

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
SELECT ObjetsTrouves.nom_gare, Gares.latitude, Gares.longitude, Gares.frequentation_{annee}, COUNT(*) 
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