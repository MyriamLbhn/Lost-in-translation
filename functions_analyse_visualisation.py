import folium
import branca
import sqlite3
import pandas as pd
import plotly.express as px

def get_data(query):
    conn = sqlite3.connect('bdd.db')
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

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