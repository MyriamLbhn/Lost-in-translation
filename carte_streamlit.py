import streamlit as st
import sqlite3
from PIL import Image
import folium
from streamlit_folium import folium_static
import branca

# Connexion à la base de données
conn = sqlite3.connect("bdd.db")
c = conn.cursor()

# Récupération des types d'objets
c.execute("SELECT DISTINCT type FROM ObjetsTrouves")
objet_types = [row[0] for row in c.fetchall()]

# Mise en forme de Streamlit
st.set_page_config(
    page_title="Objets trouvés - Fréquentation des gares",
    page_icon=":train:",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Sélection de l'année et du type d'objet
year = st.sidebar.selectbox("Année", [2019, 2020, 2021, 2022])
selected_objet_type = st.sidebar.selectbox("Type d'objet", ["Tous"] + objet_types)

# Récupération des données des objets trouvés et des gares pour l'année sélectionnée
query = f"""
SELECT ObjetsTrouves.nom_gare, Gares.latitude, Gares.longitude, Gares.frequentation_{year}, COUNT(*) 
FROM ObjetsTrouves 
JOIN Gares ON ObjetsTrouves.nom_gare = Gares.nom_gare 
WHERE strftime('%Y', ObjetsTrouves.date) = '{year}'
"""

if selected_objet_type != "Tous":
    query += f" AND ObjetsTrouves.type = '{selected_objet_type}'"

query += " GROUP BY ObjetsTrouves.nom_gare"

c.execute(query)
data = c.fetchall()

# Création de la carte
m = folium.Map(location=[48.856614, 2.3522219], zoom_start=12)

# Ajout des marqueurs sur la carte
for row in data:
    # Récupération de la fréquentation et du nombre d'objets trouvés pour l'année sélectionnée
    frequentation = row[3]
    nb_objets_trouves = row[4]

    # Création du contenu HTML pour les bulles d'information
    html = f"""
        <h4>{row[0]}</h4>
        <p>Fréquentation {year} : {frequentation}</p>
        <p>Objets trouvés : {nb_objets_trouves}</p>
    """
    iframe = branca.element.IFrame(html=html, width=200, height=100)
    popup = folium.Popup(iframe, max_width=2650)

    # Création du marqueur
    marker = folium.Marker(
        location=[row[1], row[2]],
        popup=popup,
        icon=folium.Icon(color="blue"),
    )
    marker.add_to(m)

# Affichage de la carte dans Streamlit
st.title("Carte des objets trouvés en fonction de la fréquentation des gares")
st.write(f"Nombre d'objets trouvés en {year} :")
st.write("")

# Fermeture de la connexion à la base de données
conn.close()

# Affichage de la carte dans Streamlit
folium_static(m)