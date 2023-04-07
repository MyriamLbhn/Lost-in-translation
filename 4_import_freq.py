import sqlite3
import requests
import json

gares_parisiennes = ["Paris Gare de Lyon", "Paris Montparnasse", "Paris Gare du Nord", "Paris Est", "Paris Saint-Lazare", "Paris Austerlitz", "Paris Bercy"]

def get_gare_coordinates(gare):
    nominatim_url = "https://nominatim.openstreetmap.org/search"
    params = {
        'q': gare,
        'format': 'json'
    }
    
    response = requests.get(nominatim_url, params=params)
    data = response.json()
    
    if data:
        return float(data[0]['lat']), float(data[0]['lon'])
    else:
        return None

for gare in gares_parisiennes:
    url = f"https://ressources.data.sncf.com/api/records/1.0/search/?dataset=frequentation-gares&q={gare}&sort=-total_voyageurs_non_voyageurs_2021&facet=nom_gare&facet=code_postal&facet=segmentation_drg"

    connexion = sqlite3.connect('bdd.db')
    cur = connexion.cursor()

    response = requests.get(url)

    content = json.loads(response.content)

    records = content["records"]

    fields = records[0]["fields"]

    total_passengers_19 = fields["total_voyageurs_non_voyageurs_2019"]
    total_passengers_20 = fields["total_voyageurs_non_voyageurs_2020"]
    total_passengers_21 = fields["total_voyageurs_non_voyageurs_2021"]
    total_passengers_22 = fields["total_voyageurs_non_voyageurs_2021"]

    coords = get_gare_coordinates(gare)
    if coords:
        latitude, longitude = coords
    else:
        latitude, longitude = None, None

    cur.execute('''INSERT OR REPLACE INTO Gares
                    (nom_gare, frequentation_2019, frequentation_2020, frequentation_2021, frequentation_2022, latitude, longitude)
                    VALUES (?, ?, ?, ?, ?, ?, ?)''', (gare, total_passengers_19,
                                            total_passengers_20,
                                            total_passengers_21,
                                            total_passengers_22,
                                            latitude, longitude))

    connexion.commit()
    connexion.close()