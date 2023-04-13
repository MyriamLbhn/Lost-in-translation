from functions_data_science import get_data, create_scatterplot, create_boxplot, create_barplot2

# Récupérer les données
df, conn = get_data()

# Créer le scatterplot
scatterplot = create_scatterplot(df)

# Créer le premier barplot
barplot1 = create_boxplot(df)

# Créer le deuxième barplot
barplot2 = create_barplot2(df, conn)

conn.close()