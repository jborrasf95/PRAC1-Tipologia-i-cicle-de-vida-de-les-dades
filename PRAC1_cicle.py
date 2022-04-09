from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np


pd.set_option('display.max_columns', None)

# Creem les llistes on s'emmagatzemaràn els valors
titles = []
location = []
features = []
description = []
prices = []

# Iniciem un contador
count = 0

# Fem un bucle per tal de fer scrap a les 35 primeres pagines
for i in range(35):
    # Rescatem l'informació de la primera pàgina
    if count == 0:
        # Introduim l'adreça
        web_site = 'https://www.habitaclia.com/alquiler-en-valles_occidental.htm'

        # Fem els requests i la sopa
        r = requests.get(web_site)
        soup = BeautifulSoup(r.text, 'html.parser')

        # Recuperem les dades que ens interessen gràcies a findall
        titles_list_dirty = soup.find_all('h3', class_='list-item-title')
        features_list_dirty = soup.find_all('p', class_='list-item-feature')
        location_list_dirty = soup.find_all('p', class_='list-item-location')
        description_list_dirty = soup.find_all('p', class_='list-item-description')

        # Extreiem els textos
        titles_lst = [pt.get_text(strip=True) for pt in titles_list_dirty]
        features_lst = [pt.get_text(strip=True) for pt in features_list_dirty]
        location_lst = [pt.get_text(strip=True) for pt in location_list_dirty]
        description_lst = [pt.get_text(strip=True) for pt in description_list_dirty]
        prices_lst = [p.string for p in soup.find_all('span', itemprop="price")]

        # Eliminem els espais que queden després de rescatar la variable features
        ','.join(features_lst)

        # Emmagatzemem els resultats a les llistes creades anteriorment
        titles.append(titles_lst)
        features.append(features_lst)
        location.append(location_lst)
        description.append(description_lst)
        prices.append(prices_lst)

        count = count + 1
    # Fem el mateix procediment però amb les seguents pàgines
    else:
        web_site = 'https://www.habitaclia.com/alquiler-en-valles_occidental{}{}.htm'.format("-", count)

        r = requests.get(web_site)
        soup = BeautifulSoup(r.text, 'html.parser')

        titles_list_dirty = soup.find_all('h3', class_='list-item-title')
        features_list_dirty = soup.find_all('p', class_='list-item-feature')
        location_list_dirty = soup.find_all('p', class_='list-item-location')
        description_list_dirty = soup.find_all('p', class_='list-item-description')

        titles_lst = [pt.get_text(strip=True) for pt in titles_list_dirty]
        features_lst = [pt.get_text(strip=True) for pt in features_list_dirty]
        location_lst = [pt.get_text(strip=True) for pt in location_list_dirty]
        description_lst = [pt.get_text(strip=True) for pt in description_list_dirty]
        prices_lst = [p.string for p in soup.find_all('span', itemprop="price")]

        ','.join(features_lst)

        titles.append(titles_lst)
        features.append(features_lst)
        location.append(location_lst)
        description.append(description_lst)
        prices.append(prices_lst)

        count = count + 1

# Ajuntem les llistes per tal de que no estiguin aniuades
titles_flat = np.array(titles).flatten()
location_flat = np.array(location).flatten()
features_flat = np.array(features).flatten()
description_flat = np.array(description).flatten()
prices_flat = np.array(prices).flatten()

# Creem el dataframe amb les dades
real_state_df =pd.DataFrame({
    "Títol": titles_flat,
    "Ubicació": location_flat,
    "Features": features_flat,
    "Descripció breu": description_flat,
    "Preu" : prices_flat

})

# Separem les columnes Ubicació per tenir la ciutat i el barri
real_state_df[['Ciutat', 'Barri']] = real_state_df['Ubicació'].str.split(' - ', 1, expand=True)

# Fem el mateix amb les Features
real_state_df[['m2', 'Features_1']] = real_state_df['Features'].str.split('- ', 1, expand=True)
real_state_df[['Habitacions', 'Features_2']] = real_state_df['Features_1'].str.split(' - ', 1, expand=True)
real_state_df[['Lavabos', 'Preu m2']] = real_state_df['Features_2'].str.split(' - ', 1, expand=True)

# Eliminem les columnes antigues
real_state_df = real_state_df.drop(['Ubicació', 'Features', 'Features_1', 'Features_2'], axis=1)

# Extraiem només els valors numèrics de les variables amb una unitat de mesura de tipus string
real_state_df['Habitacions'] = real_state_df['Habitacions'].str.extract("(\d*\.?\d+)", expand=True)
real_state_df['Lavabos'] = real_state_df['Lavabos'].str.extract("(\d*\.?\d+)", expand=True)
real_state_df['Preu'] = real_state_df['Preu'].str.extract("(\d*\.?\d+)", expand=True)
real_state_df['Preu m2'] = real_state_df['Preu m2'].str.extract("(\d*\.?\d+)", expand=True)
real_state_df['m2'] = real_state_df['m2'].str.extract("(\d*\.?\d+)", expand=True)

# Normalitzem aluns registres que no s'han acabat de rescatar de forma adient
real_state_df.loc[real_state_df['Ciutat'] == 'MatadeperaVer mapa', 'Ciutat'] = 'Matadepera'

real_state_df.loc[real_state_df['Barri'] == 'VolpelleresVer mapa', 'Barri'] = 'Volpelleres'
real_state_df.loc[real_state_df['Barri'] == 'TorreblancaVer mapa', 'Barri'] = 'Torreblanca'
real_state_df.loc[real_state_df['Barri'] == 'CentreVer mapa', 'Barri'] = 'Centre'
real_state_df.loc[real_state_df['Barri'] == 'Cementiri VellVer mapa', 'Barri'] = 'Cementiri Vell'
real_state_df.loc[real_state_df['Barri'] == 'EixampleVer mapa', 'Barri'] = 'Torreblanca'
real_state_df.loc[real_state_df['Barri'] == 'Eixample-Sant OleguerVer mapa', 'Barri'] = 'Eixample-Sant Oleguer'
real_state_df.loc[real_state_df['Barri'] == 'Parc CentralVer mapa', 'Barri'] = 'Parc Central'
real_state_df.loc[real_state_df['Barri'] == 'MercatVer mapa', 'Barri'] = 'Mercat'
real_state_df.loc[real_state_df['Barri'] == 'Arxiu-EstacióVer mapa', 'Barri'] = 'Arxiu-Estació'

# Reorganitzem les columnes
real_state_df = real_state_df[['Títol', "Ciutat", "Barri", "Descripció breu", "m2", "Habitacions", "Lavabos", "Preu m2", "Preu"]]

# Guardem el dataset resultat en forma de csv
real_state_df.to_csv ('C:/Users/joanb/Desktop/preus_lloguer_vocc.csv', index = False, header=True)


