import sqlite3
import pandas as pd
import folium
import branca
import plotly.express as px

def get_data(query):
    conn = sqlite3.connect('bdd.db')
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def create_plot(type_objet, nom_gare, annee):
    query = f"SELECT semaine, COUNT(*) AS nb_objets FROM ObjetsTrouves WHERE annee = {annee}"
    if type_objet != "Tous": query += f" AND type = '{type_objet}'"
    if nom_gare != "Toutes": query += f" AND nom_gare = '{nom_gare}'"
    query += " GROUP BY semaine"
    df = get_data(query)

    title = f"Nombre d'objets trouvés par semaine pour l'année {annee}"
    if type_objet != "Tous": title += f' de type "{type_objet}"'
    if nom_gare != "Toutes": title += f' à la gare "{nom_gare}"'

    fig = px.bar(df, x="semaine", y="nb_objets", title=title, labels={"semaine": "Numéro de semaine", "nb_objets": "Nombre d'objets trouvés"})
    return fig

def create_map(type_objet, nom_gare, annee):
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

    m = folium.Map(location=[48.856614, 2.3522219], zoom_start=12)
    for row in data:
        frequentation, nb_objets_trouves = row[3], row[4]
        if annee == 2023:
            html = f"<h4>{row[0]}</h4><p>Fréquentation {annee} : Inconnue</p><p>Objets trouvés : {nb_objets_trouves}</p>"
        else:
            html = f"<h4>{row[0]}</h4><p>Fréquentation {annee} : {frequentation}</p><p>Objets trouvés : {nb_objets_trouves}</p>"
        iframe = branca.element.IFrame(html=html, width=200, height=100)
        popup = folium.Popup(iframe, max_width=2650)
        marker = folium.Marker(location=[row[1], row[2]], popup=popup, icon=folium.Icon(color="blue"))
        marker.add_to(m)
    return m