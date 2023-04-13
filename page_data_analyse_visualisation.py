import streamlit as st
from streamlit_folium import folium_static
import datetime
from API_SNCF_objets_trouves import update_objets_trouves_current_year
from functions_analyse_visualisation import create_map, get_data, create_plot


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


