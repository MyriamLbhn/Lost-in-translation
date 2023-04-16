# Projet : Analyse des objets trouvés dans les gares parisiennes

Ce projet vise à analyser les objets trouvés dans les gares parisiennes en utilisant les données fournies par l'API SNCF. Le script principal récupère les données depuis l'API, les traite et les stocke dans une base de données SQLite pour une analyse ultérieure.

## Fonctionnalités de l'application

1. **Récupération des données des objets trouvés :** Utilisation de l'API open data de la SNCF pour récupérer les données entre 2019 et 2022 sur les gares parisiennes et stockage des données dans une base de données SQL.
2. **Récupération des températures journalières :** Collecte des températures moyennes journalières sur Paris entre 2019 et 2022.
3. **Data Analyse Visualisation (Streamlit) :**
   - Affichage de la somme du nombre d'objets trouvés par semaine entre 2019 et 2022 sur un histogramme Plotly (avec la possibilité de filtrer par type d'objet).
   - Carte de Paris affichant le nombre d'objets trouvés en fonction de la fréquentation des voyageurs dans chaque gare, avec possibilité de filtrer par année et par type d'objets.
4. **Data Analyse pour Data Science (Streamlit) :**
   - Scatterplot du nombre d'objets trouvés en fonction de la température pour évaluer la corrélation entre les deux variables.
   - Analyse de la médiane du nombre d'objets trouvés en fonction de la saison et évaluation de la corrélation entre ces deux variables.
   - Affichage du nombre d'objets trouvés en fonction du type d'objet et de la saison pour évaluer la corrélation entre ces deux variables.
5. **Conclusion globale :** Intégration de la conclusion globale de l'étude dans l'application Streamlit.
6. **Bonus - Mise à jour des données :** Bouton dans l'application Streamlit permettant la mise à jour des données de l'app en récupérant toutes les données nécessaires jusqu'à la dernière date disponible.

## Installation
1. Clonez ce dépôt ou téléchargez les fichiers dans un dossier de votre choix.
2. Installez les bibliothèques requises à l'aide de `pip install -r requirements.txt` ou installez-les manuellement.
3. Obtenez une clé API pour WorldWeatherOnline à partir de leur site web : https://www.worldweatheronline.com/developer/ .
4. Créez un fichier `.env` à la racine du projet et ajoutez-y la clé API de la manière suivante :
    
    ```bash
    API_KEY=<votre clé API>
    ```
5. Exécutez le script `create_database.py` pour créer la base de données et les tables nécessaires .
6. Exécutez le script `script.py` pour récupérer les données à partir des API et les stocker dans la base de données.

## Structure de la base de données

La base de données est composée de trois tables :

1. **ObjetsTrouves** : Contient les informations sur les objets trouvés dans les gares parisiennes.
2. **Temperatures** : Contient les informations sur les températures enregistrées.
3. **Gares** : Contient les informations sur les gares parisiennes, notamment la fréquentation et les coordonnées géographiques.

## Lancer l'application Streamlit

L'application Streamlit permet d'explorer et d'analyser les objets trouvés dans les gares parisiennes. Pour lancer l'application, suivez les étapes ci-dessous :

1. Assurez-vous d'avoir suivi les étapes d'installation et d'exécution pour préparer la base de données.
2. Installez Streamlit à l'aide de la commande suivante : `pip install streamlit`
3. Exécutez la commande suivante pour lancer l'application : `streamlit run app.py`
4. Streamlit ouvrira automatiquement un navigateur et affichera l'application. Utilisez les options de navigation et les contrôles interactifs pour explorer les données et les visualisations.
