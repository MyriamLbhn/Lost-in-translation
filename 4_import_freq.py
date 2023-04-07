import sqlite3
import requests
import json

gares_parisiennes = ["Paris Gare de Lyon", "Paris Montparnasse", "Paris Gare du Nord", "Paris Est" , "Paris Saint-Lazare" , "Paris Austerlitz" , 'Paris Bercy']

for gare in gares_parisiennes:
    # Set API endpoint and parameters
    url = f"https://ressources.data.sncf.com/api/records/1.0/search/?dataset=frequentation-gares&q={gare}&sort=-total_voyageurs_non_voyageurs_2021&facet=nom_gare&facet=code_postal&facet=segmentation_drg"


    # Connect to the SQLite database
    connexion = sqlite3.connect('bdd.db')
    cur = connexion.cursor()

    # Make the API request
    response = requests.get(url)

    # Get the response content as a JSON object
    content = json.loads(response.content)

    # Extract the relevant data from the JSON object and add it to the Gares table
    records = content["records"]

    fields = records[0]["fields"]
    # print(fields)
    total_passengers_19 = fields["total_voyageurs_non_voyageurs_2019"]
    total_passengers_20 = fields["total_voyageurs_non_voyageurs_2020"]
    total_passengers_21 = fields["total_voyageurs_non_voyageurs_2021"]
    total_passengers_22 = fields["total_voyageurs_non_voyageurs_2021"]

    with open('output_fields.json', 'w') as outfile:
        json.dump(fields, outfile)


    cur.execute('''INSERT OR REPLACE INTO Gares
                    (nom_gare, frequentation_2019, frequentation_2020, frequentation_2021, frequentation_2022, latitude, longitude)
                    VALUES (?, ?, ?, ?, ?, NULL, NULL)''', (gare, total_passengers_19,
                                            total_passengers_20,
                                            total_passengers_21,
                                            total_passengers_22))

    # Commit the changes and close the connection to the database
    connexion.commit()
    connexion.close()
