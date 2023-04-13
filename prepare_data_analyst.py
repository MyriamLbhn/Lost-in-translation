from functions_analyse_visualisation import get_data , create_plot , create_map

query_all_data = "SELECT * FROM ObjetsTrouves"
df = get_data(query_all_data)

# Préparation des données pour les widgets
type_objet = ["Tous"] + list(df['type'].unique())
nom_gare = ["Toutes"] + list(df['nom_gare'].unique())

