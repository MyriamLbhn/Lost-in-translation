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
