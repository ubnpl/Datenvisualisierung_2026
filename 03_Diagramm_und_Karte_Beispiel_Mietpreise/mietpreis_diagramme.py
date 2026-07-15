#!/usr/bin/env python
# coding: utf-8

# # Beispiel Mietpreis: Visualisierung mit Histogrammen und Tortendiagramm

# ## Datenbeispiel: Durchschnittlicher Mietpreis Schweiz nach Zimmerzahl und Kanton
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


# ## 1. Datenfile anlesen und Daten anzeigen
# 
# Einlesen des Datenfiles mit Pandas. Es können verschiedene Seiten und beliebige Ausschitte der Daten ausgewählt und eingelesen werde. Die Daten werden dann in einem Dictionary gespeichert. Dokumentation zur Datenstruktur Dictionary: https://realpython.com/python-dicts/

# #### Erste Seite des Excel-Files lesen und anzeigen

# In[3]:


# Erste Seite des Excel-Files (default wenn keine Seite spezifiziert ist)
# Spezifikation Reihen über "header=4"
# Spezifikation Spalten über "usecols="B,D"" möglich
df = pd.read_excel('je-d-09.03.03.01.xlsx', header=4)


# In[4]:


# Eingelesene Daten anzeigen
df


# #### Zweite Seite des Excel-Files lesen und anzeigen

# In[5]:


# Zweite Seite des Excel-Files mit Namen "2023" einlesen
df2 = pd.read_excel('je-d-09.03.03.01.xlsx', sheet_name="2023", header=4)


# In[6]:


df2


# #### Einen Teilbereich der ersten Seite einlesen (ohne Anmerkungen)

# In[7]:


# Zweite Seite mit überspringen der Definierten Reihen einlesen
# Uebersprungene Reihen definieren mit "Skiprows"
df1s = pd.read_excel('je-d-09.03.03.01.xlsx', sheet_name="2024", header=4, skiprows=[32,33,34,35,36,37,38,39,40,41,42])


# In[8]:


df1s


# #### Struktur der Dataframes
# 
# Datenstruktur: Dicitionnary; die spalten des Excel-Sheets sind über keys() zugänglich

# In[9]:


# Verfügbare Keys anzeigen lassen
df1s.keys()


# In[10]:


# Eine bestimmte Spalte auswählen
df1s['Durch-schnittlicher Mietpreis ']


# In[11]:


# Bestimmte Felder einer bestimmten Zeile ausgeben
df1s['Durch-schnittlicher Mietpreis '][2:7]


# ## Visualisierung der Daten mit MatPlotLib: Histogramme
# 
# Visualisierung der durschnittlichen Mitpreise für alle Kantone und den schweizer Durschnitt als Histogramm

# #### Notwendige Module importieren

# In[12]:


# Matplotlib zum erstellen der Grafiken
import matplotlib.pyplot as plt


# In[13]:


# Numpy zur Transformation der Daten
import numpy as np


# #### Visualisierung 1: Durschnittlicher Mietpreis nach Kanton
# 
# Einfachster Fall: einen einzelnen Datensatz als Histogramm visualisieren. Die Kantonsnamen werden auf der x-Achse aufgetragen, die Höhe der Mietpreise auf der y-Achse.

# In[15]:


plt.figure().set_figheight(5)   # Höhe der Grafik
plt.figure().set_figwidth(15)    # Breite der Grafik

plt.rcParams.update({'font.size': 11}) # Schriftgrösse definieren

plt.bar(df1s['Unnamed: 0'], df1s['Durch-schnittlicher Mietpreis '])  # Barplot erstellen

plt.xlabel('Kanton') # Beschriftung x-Achse
plt.ylabel('Durchschnittlicher Mietpreis [CHF]')  # Beschriftung y-Achse

plt.legend(['Mietpreis 2024']) # Datensatz beschriften
plt.xticks(rotation=90) # Labels um 90 Grad drehen

plt.title("Visualisierung 1: Durschnittlicher Mietpreis")

plt.show()


# #### Visualisierungen 2: Vergleich Mietpreise nach Kanton und Wohnungsgrösse, Darstellung übereinander
# 
# Für den Vergleich zweier Datensätze können verschiedene Darstellung gewählt werden. Zuerst werden die Datensätze übereinander dargestellt, das heisst der zweite Datensatz wird über dem ersten angezeigt.

# In[16]:


plt.figure().set_figheight(5)   # Höhe der Grafik
plt.figure().set_figwidth(15)    # Breite der Grafik

plt.bar(df1s['Unnamed: 0'], df1s['Durch-schnittlicher Mietpreis .2']) # Barplot Datensatz 1
plt.bar(df1s['Unnamed: 0'], df1s['Durch-schnittlicher Mietpreis .6'], bottom=df1s['Durch-schnittlicher Mietpreis .2']) # Barplot Datensatz 2

plt.xlabel('Kanton') # Beschriftung x-Achse
plt.ylabel('Durchschnittlicher Mietpreis [CHF]')  # Beschriftung y-Achse
plt.legend(['2-Zimmer', '6-Zimmer']) # Datensätze beschriften 
plt.xticks(rotation=90) # Labels um 90 Grad drehen

plt.title("Visualisierung 2: Vergleich Mietpreise nach Wohnungsgrösse und Kanton") # Titel der Grafik

plt.show()


# #### Visualisierungen 3: Vergleich Mietpreise nach Kanton und Wohnungsgrösse, Darstellung nebeneinander
# 
# Die Darstellung der Datensätze nebeneinander ist übersichtlicher. Allerding muss der Abstand der Datensätze bestimmt werden.

# In[17]:


# Berechnen des Abstands zum Visualisieren der Datensätze
indices = range(len(df1s['Durch-schnittlicher Mietpreis .2'])) # Indices für jeden Eintrag zum bestimmen der Position auf der x-Achse
width = np.min(np.diff(indices))/3. # Breite berechnen

plt.figure().set_figheight(5)   # Höhe der Grafik
plt.figure().set_figwidth(15)    # Breite der Grafik

plt.bar(indices-width/2, df1s['Durch-schnittlicher Mietpreis .2'],width,color='b',label='-Ymin') # Barplot Datensatz 1; x-Postionen Indices-Breite
plt.bar(indices+width/2, df1s['Durch-schnittlicher Mietpreis .6'],width,color='r',label='Ymax') # Barplot Datensatz 2; x-Postionen Indices+Breite

plt.xticks(indices, df1s['Unnamed: 0'], rotation='vertical') # Beschriftung Datenpunkte nach Kantonen

plt.xlabel('Kanton') # Beschriftung x-Achse
plt.ylabel('Durchschnittlicher Mietpreis [CHF]')  # Beschriftung y-Achse
plt.legend(['2-Zimmer', '6-Zimmer']) # Datensätze beschriften 

plt.title("Visualisierung 3: Mietpreise nach Wohnungsgrösse und Kanton; Darstellung nebeneinander") # Titel der Grafik

plt.savefig('Histogram_2b.png', bbox_inches='tight') # Grafik als .png speichern
plt.show()


# ## Visualisierung der Daten mit Matplotlib: Tortdendiagramm
# 
# Visualisierung der Mietpreise in der Schweiz als Tortendiagramm. Diese Darstellung ist weniger geeignet, wird aber zum Vergleich hier auch noch gezeigt. Der Eintrag zum Durschnittlichen Mietpreis in der gesamten Schweiz wird hier weggelassen, weil er in dieser Darstellung weniger sinnvoll ist. 

# #### Information aus dem Dataframe bekommen und Datenpunkte weglassen

# In[18]:


# Informationen zum Kanton sind im df2_a verfügbar
df1s['Unnamed: 0']


# In[19]:


# Den ersten Datenpunkt (Schweiz) weglassen (alle anderen auswählen)
df1s['Durch-schnittlicher Mietpreis '][1:]


# #### Tortendiagramm: Mietpreise anteilig nach Kantonen

# In[20]:


fig = plt.figure(figsize=(22,22)) # Grösse der Grafik
ax = fig.add_axes((0,0,.5,1)) # Achsen definieren

ax.set_title('Visualisierung 4: Mietpreise anteilig nach Kantonen', 
             bbox={'facecolor':'0.8', 'pad':3}, fontsize=20) # Titel

#Plotten der Mietpreise ohne Vergleichswert Schweiz (Zeile 0 wird weggellasen, auswählen der Zeilen > 0 mit [1:])
ax.pie(df1s['Durch-schnittlicher Mietpreis '][1:], labels=df1s['Unnamed: 0'][1:], autopct='%1.1f%%')

plt.show()


# ## Links zu weiteren Tutorials
# 
# In diesem Notebook werden nur wenige Optionen der Datenvisualisierung gezeigt. Viele weitere Optionen sind verfügbar, einige sind in den folgenden Links erklärt:
# 
#    [SimplyLearn: Data Visualization in Python](https://www.simplilearn.com/tutorials/python-tutorial/data-visualization-in-python)
#     
#    [W3Schools: Matplotlib Tutorial](https://www.w3schools.com/python/matplotlib_intro.asp)

# In[ ]:




