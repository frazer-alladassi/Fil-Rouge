import pandas as pd
from py2neo import Graph, Node

# Load and Clean up data
path_to_csv = '/Users/frazer/datatourisme.csv'
df = pd.read_csv(path_to_csv)
df = df.drop(['Periodes_regroupees', 'Covid19_mesures_specifiques', 'Covid19_est_en_activite',
              'Covid19_periodes_d_ouvertures_confirmees', 'Description', 'Classements_du_POI'], axis=1)
df = df.dropna(axis=0, how='any', subset=['Adresse_postale', 'Contacts_du_POI'])


# Neo4j Configs
server_url = "http://localhost:7474/db/data"
username = "neo4j"
password = "password"
graph = Graph(server_url, auth=(username, password), name=username)

# Import Dataframe into Neo4j
for index, row in df.iterrows():
    node = Node('Poi', nom=row['Nom_du_POI'], categorie=row['Categories_de_POI'], latitude=float(row['Latitude']), longitude=float(row['Longitude']),
                adresse_postale=row['Adresse_postale'], code_postale_comune=row['Code_postal_et_commune'], createur=row['Createur_de_la_donnee'], site=row['SIT_diffuseur'],
                date_maj=row['Date_de_mise_a_jour'], contacts=row['Contacts_du_POI'], url=row['URI_ID_du_POI'])
    graph.create(node)
