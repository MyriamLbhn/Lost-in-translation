import requests
import pandas as pd

gares_parisiennes = ["Paris Gare de Lyon", "Paris Montparnasse", "Paris Gare du Nord", "Paris Est" , "Paris Saint-Lazare" , "Paris Austerlitz" , 'Paris Bercy']
annees = ["2019", "2020" , "2021" , "2022"]

# Création d'un DataFrame vide
df = pd.DataFrame()
i = 0
for gare in gares_parisiennes:
    for annee in annees:
        print(i)
        response = requests.get(f"https://ressources.data.sncf.com/api/records/1.0/search/?dataset=objets-trouves-restitution&q=&rows=-1&sort=-date&facet=date&facet=gc_obo_date_heure_restitution_c&facet=gc_obo_gare_origine_r_name&facet=gc_obo_nature_c&facet=gc_obo_type_c&facet=gc_obo_nom_recordtype_sc_c&refine.gc_obo_gare_origine_r_name={gare}&refine.date={annee}")
        
        # Récupération des enregistrements
        records = response.json()["records"]

        # Conversion des enregistrements en DataFrame
        records_df = pd.DataFrame([record["fields"] for record in records])

        # Ajout des enregistrements au DataFrame global
        df = pd.concat([df, records_df], ignore_index=True)
        i += 1
# Enregistrement du DataFrame dans un fichier CSV
df.to_csv("objets_trouves.csv", index=False)