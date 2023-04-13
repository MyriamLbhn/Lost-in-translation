import datetime
import streamlit as st
from API_SNCF_objets_trouves import update_objets_trouves_current_year
from functions_analyse_visualisation import create_map, create_plot
from prepare_data_science import scatterplot, barplot1, barplot2
import streamlit as st
from prepare_data_analyst import type_objet, nom_gare
from streamlit_folium import folium_static

def page1():
    st.title("Analyse des objets trouvés dans les gares")

    # Bouton "Mettre à jour la base de données"
    update_button = st.button("Mettre à jour la base de données")

    # Si le bouton est cliqué, mettez à jour la base de données
    if update_button:
        with st.spinner("Mise à jour de la base de données..."):
            update_objets_trouves_current_year()
        st.success("Base de données mise à jour avec succès.")
        
    # Menu de sélection
    type_objet_choice = st.selectbox("Type d'objet", type_objet)
    nom_gare_choice = st.selectbox("Nom de la gare", nom_gare)
    annee_en_cours = datetime.datetime.now().year
    annee = st.slider("Année", 2019, annee_en_cours)

    # Affichage de l'histogramme du nombre d'objets trouvées par semaine par an
    fig = create_plot(type_objet_choice, nom_gare_choice, annee)
    st.write("Graphique :")
    st.plotly_chart(fig)

    # Affichage de la carte des objets trouvés en fonction de la fréquentation des gares
    m = create_map(type_objet_choice, nom_gare_choice, annee)
    st.title("Carte des objets trouvés en fonction de la fréquentation des gares")
    st.write("Voici la carte des objets trouvés en fonction de la fréquentation des gares pour l'année " + str(annee) + ".")
    st.write("")
    folium_static(m)



def page2():
    st.title("Analyse des objets trouvés")
    st.write("Affichage du scatterplot du nombre d'objets trouvés en fonction de la température.")

    # Afficher le scatterplot
    st.plotly_chart(scatterplot)

    # Afficher les barplots
    st.plotly_chart(barplot1)
    st.plotly_chart(barplot2)


st.sidebar.title("Navigation")
page = st.sidebar.radio("Aller à", ["Page 1", "Page 2"])

# Affichez le contenu de la page sélectionnée
if page == "Page 1":
    page1()
elif page == "Page 2":
    page2()