import shutil
import sqlite3
import pandas as pd


source_file = 'bdd.db'

destination_file = 'bdd_streamlit.db'

shutil.copy(source_file, destination_file)

conn = sqlite3.connect('bdd_streamlit.db')

df = pd.read_sql_query('SELECT * FROM ObjetsTrouves', conn)

df['annee'] = pd.to_datetime(df['date']).dt.year
df['semaine'] = pd.to_datetime(df['date']).dt.isocalendar().week


df.to_sql('ObjetsTrouves', conn, if_exists='replace', index=False)

conn.close()
