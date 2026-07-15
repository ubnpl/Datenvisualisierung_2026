#!/usr/bin/env python
# coding: utf-8

# # Beispiel Mietpreis: Datenvisualisierung auf Karte

# ## Datenbeispiel: Durchschnittlicher Mietpreis nach Zimmerzahl und Kanton
# 
# Datenquelle: Bundesamt für Statistik
# Webseite Datensatz: https://opendata.swiss/de/dataset/durchschnittlicher-mietpreis-in-franken-nach-zimmerzahl-und-kanton2
# Datum Download: 15.07.2026
# 
# Format: Microsoft Excel (.xlsx)

# ### Lesen des .xlsx-files
# 
# Zum importieren von Excel-Files kann das Modul **Pandas** verwendet werden.
# https://pandas.pydata.org/
# 
# 
# Installieren mit Anaconda (im Anaconda Prompt (Windows) oder Terminal (Linux oder MacOS):
# 
#     conda install pandas
# 

# #### Modul Pandas importieren

# In[1]:


#Pandas importieren
import pandas as pd


# In[2]:


from pandas import ExcelWriter
from pandas import ExcelFile


# #### Einen Teilbereich der ersten Seite einlesen 
# 
# Details zum Einlesen des Datenfiles sind im Notebook "Visualisierung mit Histogrammen..." erklärt

# In[3]:


# Zweite Seite mit überspringen der Definierten Reihen einlesen
# Uebersprungene Reihen definieren mit "Skiprows"
df1s = pd.read_excel('je-d-09.03.03.01.xlsx', sheet_name="2024", header=4, skiprows=[32,33,34,35,36,37,38,39,40,41,42])


# In[4]:


df1s


# ## Visualisierung der Daten auf einer Karte
# 
# Die Mietpreise der Schweiz werden auf einer Schweizer Karte angezeigt. Dazu ist die Kombination mit entsprechende Geodaten notwendig.

# #### Module für die Visualisierung importieren: GeoPandas und MatPlotLib
# 
# Matplotlib wird weitering benötigt.

# In[5]:


# Matplotlib zum erstellen der Grafiken
import matplotlib.pyplot as plt


# Geographische Visualisierung der Daten mit **GeoPandas**:
#     
# [https://geopandas.org](https://geopandas.org)
#     
# Installation (Anaconda):
#     
#     conda install geopandas

# In[6]:


# Geopandas importieren
import geopandas as gpd


# #### Benötigte Geodaten bereit stellen

# Zur Visualisierung auf einer Karte müssen die entsprechenden Koordinaten verfügbar sein. Hier brauchen wir eine Karte der Schweiz mit den Kantonsgrenzen, damit wir die durchschnittlichen Mietpreise für jeden Kanton eintragen können. Die entsprechenden Geodaten werden vom Bundesamt für Landestopografie swisstopo zur Verfügung gestellt und können beim Geoportal des Bundes bezogen werden:
# 
# https://data.geo.admin.ch
# 
# Die zur Verfügung gestellten .shp-files können zu .geojson konvertiert werden. Dazu wird das tool 'ogr2ogr' in der commandline mit folgendem Befehl aufgerufen:
#     
# ogr2ogr -f GeoJSON -t_srs EPSG:4326 -simplify 1000 switzerland.geojson swissBOUNDARIES3D_1_5_TLM_KANTONSGEBIET.shp
# 
# Das tool 'ogr2ogr' ist teil GDAL-package https://pypi.org/project/GDAL/ die zusammen mit GeoPandas installiert wird.
# 

# ## Geodaten Visualisieren: Kartendarstellung von .geojson-Files

# In[7]:


# GeoJson-file mit GeoPandas importieren und anzeigen
geo_df = gpd.read_file('switzerland.geojson')
print (geo_df.columns)
geo_df.head()


# #### Kartendarstellung: Kantone und Kantonsgrenzen
# 
# Das .geojson-File enthält Informationen zu Kantonen und Kantonsgrenzen; diese können visualisiert werden.

# In[8]:


# basic map plot
plt.rcParams.update({'font.size': 15}) # Schriftgrösse definieren
fig, ax = plt.subplots(figsize=(20,20)) # Plots initialisieren
geo_df.plot(ax=ax, column='ERSTELL_J', cmap='OrRd', edgecolor='black') # Karte anzeigen
ax.set_title('Kartendarstellung: Grundlagen') # Titel setzen
plt.show()


# #### Kartendarstellung: Einwohnerzahl der Kantone als Heatmap
# 
# Zusätzlich entählt das .geojson-File Informationen zur Einwohnerzahl und anderen Kenndaten der Kantone. Die Einwohnerzahl kann als Heatmap auf der Karte angezeigt werden.

# In[9]:


# Karte mit Kantonsgrenze; Einwohnerzahl als Heatmap
fig, ax = plt.subplots(figsize=(20,10)) # Grfik und Grösse definieren
geo_df.plot(ax=ax, column='EINWOHNERZ', cmap='OrRd', edgecolor='black', legend=True, legend_kwds={"label": "Einwohnerzahl"}) # Karte mit Heatmap (cmap)
ax.set_title('Einwohnerzahl nach Kanton') # Titel festlegen
plt.show()


# ## Geodatenfile Analysieren und Kantonsnamen den Namen im Mietpreis-File zuordnen

# In[10]:


# Anzahl Zeilen im Geodatensatz anzeigen
geo_df.shape


# Im Geodatensatz sind mehr Zeilen als Kantone (für viele Kantone sind meherere Einträge enthalten). Um die Kantonsnamen zu vergleichen sollte für jeden Kanton nur ein Eintrag vorhanden sein. Dies kann hier durch weglassen aller Zeilen mit Kantonsfläche 'nan' (not a number) erreicht werden, da dann nur der Haupteintrag für jeden Kanton ausgewählt wird.

# In[11]:


# Neuen Dataframe erstellen ohne Einträge mit geo_df['KANTONSFLA'] = nan 
geo_notna = geo_df[geo_df['KANTONSFLA'].notna()]


# In[12]:


geo_notna.shape


# Wir haben jetzt in geo_notna für jeden Kanton einen Eintrag gespeichert und können ihn anzeigen lassen:

# In[13]:


# Vergleich der Kantonsnamen nach Index in beiden sortierten Dataframes
for item in geo_notna['NAME']:
    print(item)


# Die Kantonsnamen sind anders als im Datensatz der Mietpreise: Namen sind anders abgekürzt und in der jeweiligen Sprache des Kantons geschrieben.  Um die Geodaten der Kantone den Mietpreisen zuzuordnen muss jeder Kantonname eine Entsprechung haben. Dies erreichten wir in zwei Schritten:
# 
#     1. Alphabetische Sortierung der Kantonsnamen
#     2. Übersetzung einiger Kantonsnamen, bis die Namen korrekt zugeordnet werden können
# 
# Die Zuordnung kann auf verschiedene Arten gelöst werden, z.B. auch mithilfe eines Übersetzungsmoduls. Diese Lösung hier ist sehr einfach, aber nicht systematisch.

# #### Sortieren der Kantonsnamen und Übersetzung für die richtige Zuordnung der Einträge
# Für das sortieren steht in Pandas/Geopandas die Funktion sort_values() zur Verfügung. Die Funktionalität ist analog der sort_values-Funktion in Pandas:
# 
# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.sort_values.html

# In[14]:


# Sortieren der Geodaten nach Kantonsnamen
geo_sort = geo_notna.sort_values('NAME',ignore_index=True)


# In[15]:


# Sortieren der Mietpreise nach Kantonsnamen und Weglassen des Eintrags für die Schweiz
df1s_sorted = df1s[1:].sort_values('Unnamed: 0',ignore_index=True)


# In[16]:


# Vergleich der Kantonsnamen nach Index in beiden sortierten Dataframes
for num in range(df1s_sorted.shape[0]):
    print(num, geo_sort['NAME'][num],"\t", df1s_sorted['Unnamed: 0'][num])


# Die Indices der Kantone stimmen in vier Fällen nicht überein. Dies kann gelöst werden, wenn zwei der Namen ersetzt werden und anschliessend nochmals sortiert wird. 

# In[17]:


# Ersetzung Nr. 1
df1s_r = df1s_sorted.replace({'Unnamed: 0': {'Wallis': 'Valais'}})


# In[18]:


# Ersetzung Nr. 2
df1sr = df1s_r.replace({'Unnamed: 0': {'Tessin': 'Ticino'}})


# In[19]:


# Neue sortierung
df1sr_sorted = df1sr.sort_values('Unnamed: 0',ignore_index=True)


# In[20]:


df1sr_sorted.shape


# In[21]:


# Überprüfen der Entsprechung und Speichern der entsprechenden Indices in der Liste m_kanton
m_kanton = []
for num in range(df1sr_sorted.shape[0]): # Ausgabe der Kantonsnamen in beiden Listen  und Mietpreis
    print(num,'\t\t', geo_sort['NAME'][num],' : ', df1sr_sorted['Unnamed: 0'][num], '\t\t\t\t\t', df1sr_sorted['Durch-schnittlicher Mietpreis '][num]) 
    m_kanton.append(geo_sort['NAME'][num]) # Index speichern


# Die Kantonsnamen sind nun in beiden Listen gleich geordnet. Dadurch kann jeder Eintrag einem Kanton zugeordnet und entsprechend dargestellt werden. Die Zuordnung ist als Indes in der Liste m_kanton gespeichert

# In[22]:


# Index eines Kantons ausgeben lassen
m_kanton.index('Zug')


# In[23]:


# Mietpreis eines Kantons ausgeben lassen
df1sr_sorted['Durch-schnittlicher Mietpreis '][m_kanton.index('Zug')]


# ## Visualisierung der Mietpreise auf der Karte
# 
# Für die Visualisierung der Mietpreise wird eine Liste mit dem Mietpreis für jeden Kanton im ursprünglichen Dataframe geo_df erstellt. 

# In[24]:


# Mietpreis für jeden Kanton im Geodatenframe nach Namen auswählen und in der Liste miet_geo speichern
miet_geo = []
for item in geo_df['NAME']:
    #print(item, m_kanton.index(item))
    miet_geo.append(df1sr_sorted['Durch-schnittlicher Mietpreis '][m_kanton.index(item)])
#miet_geo


# In[25]:


# Transformieren der Liste in ein Dataframe
df_miet_geo = pd.DataFrame(miet_geo,columns =['Miete'])


# In[26]:


# Karte mit Kantonsgrenze; Einwohnerzahl als Heatmap
fig, ax = plt.subplots(figsize=(20,10)) # Grösse festlegen
ax.set_title('Visualisierung der Mietpreise nach Kantonen: Kartendarstellung', 
             bbox={'facecolor':'0.8', 'pad':3}, fontsize=20) # Titel festlegen
geo_df.plot(ax=ax, column=df_miet_geo['Miete'], cmap='OrRd', edgecolor='black', legend=True, legend_kwds={"label": "Mietpreise [CHF]"}) # Karte mit Heatmap (cmap)
plt.savefig('Mietpreis_Karte.png', bbox_inches='tight') # Grafik als .png speichern
plt.show()


# Dies ist eine sehr einfache Kartendarstellung. Grundsätzlich können Geodatensätze vielfältig mit anderen Daten kombiniert werden. Zudem gibt es noch weitere Darstellungsmöglichkeiten, z.B. interaktive Karten. 
# 
# Weitere Beispiele mit Geopandas: https://geopandas.org/en/stable/getting_started/introduction.html

# In[ ]:




