import os
import subprocess
from import_temp_to_bdd import ajouter_temperatures_bdd
from import_freq import collect_data_for_gares_parisiennes
from API_SNCF_objets_trouves import ajouter_objets_trouves


def supprimer_fichier_bdd():
    if os.path.exists("bdd.db"):
        os.remove("bdd.db")
        print("Le fichier bdd a été supprimé.")
    else:
        print("Le fichier bdd n'existe pas.")

supprimer_fichier_bdd()

subprocess.call(["python", "create_database.py"])

ajouter_temperatures_bdd()

collect_data_for_gares_parisiennes()

ajouter_objets_trouves()





