#!/usr/bin/env python
# coding: utf-8

# # Beispiel Stromproduktion 3: Scatterplot, Regression, Korrelation
# 
# ### Datenvisualisierung mit Python/Matplotlib

# ### Datenbeispiel: Stromproduktion in der Schweiz
# 
# Datenquelle: Bundesamt für Energie
# Webseite: https://opendata.swiss/dataset/energiedashboard-ch-stromproduktion-swissgrid
# 
# Zeitpunkt der Abrfrage: 15.07.2026
# 
# Format: CSV (.csv)

# ## 1. Einlesen und Organisation der Daten
# 
# Zum importieren von CSV-Files kann das Modul Pandas verwendet werden.
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


# #### Erste Seite des Excel-Files lesen und anzeigen

# In[2]:


# CSV-file lesen
df = pd.read_csv('ogd104_stromproduktion_swissgrid.csv')


# In[3]:


# Eingelesene Daten anzeigen
df


# #### Struktur der Dataframes
# 
# Datenstruktur: Dictionnary; die Spalten des CSV-files sind über Keys() zugänglich

# In[4]:


# Verfügbare Keys anzeigen lassen
df.keys()


# In[5]:


# Eine bestimmte Spalte auswählen
df['Energietraeger']


# #### Daten neu ordnen: Datensatz in verschiedene Zeitreihen nach Energieträger gruppieren
# 
# Im Inputfile sind alle Energieerzeugungsdaten in der zweiten Spalte gespeichert, der jeweilige Energieträger ist jeweils in der ersten Spalte angegeben. Zur Visualisierung müssen die Daten nach Energieträger gruppiert werden.

# In[6]:


# Liste der verschiedenen Energieträger erstellen
Energiearten = []
for en in df['Energietraeger']:
      if not en in Energiearten:
          Energiearten.append(en);

print('Liste der Energieträger: \n', Energiearten)


# In[7]:


# Einen bestimmten Energieträger auswählen und in neuem Dataframe speichern
df_fluss = df.loc[df['Energietraeger'] == 'Flusskraft']
df_kern = df.loc[df['Energietraeger'] == 'Kernkraft']
df_speicher = df.loc[df['Energietraeger'] == 'Speicherkraft']
df_therm = df.loc[df['Energietraeger'] == 'Thermische']
df_photo = df.loc[df['Energietraeger'] == 'Photovoltaik']
df_wind = df.loc[df['Energietraeger'] == 'Wind']
print('Anzahl Datenpunkte pro Energieträger:\n')
print('\tFlusskraft:\t', len(df_fluss))
print('\tKernkraft:\t', len(df_kern))
print('\tSpeicherkraft:\t', len(df_speicher))
print('\tThermische:\t', len(df_therm))
print('\tPhotovoltaik:\t', len(df_photo))
print('\tWind:\t\t', len(df_wind))


# ## 2. Vergleich der  Stromerzeugung verschiedener Energieträger

# #### Notwendige Module importieren

# In[8]:


# Matplotlib zum erstellen der Grafiken
import matplotlib.pyplot as plt


# #### Zeitreihen für alle Energieträger plotten
# 
# Für einen allgemeinen Überblick wird zuerst die Stromproduktion aller Energieträger in einzelnen Subplots visualisiert.

# In[9]:


plt.rcParams.update({'font.size': 14}) # Schriftgrösse definieren

# Matplotlib subplots
f, axs = plt.subplots(6,1, figsize=(15, 20)) # Definieren der Subplots

# Subplot Stromproduktion aus Flusskraft
plt.subplot(6, 1, 1)
plt.plot(df_fluss['Datum'],df_fluss['Produktion_GWh']) 
plt.xticks(df_fluss['Datum'][0::500])
plt.legend(['Flusskraft'])

# Subplot Stromproduktion aus Kernkraft
plt.subplot(6, 1, 2)
plt.plot(df_kern['Datum'],df_kern['Produktion_GWh'])
plt.xticks(df_kern['Datum'][0::500])
plt.legend(['Kernkraft'])

# Subplot Stromproduktion aus Speicherkraftwerke
plt.subplot(6, 1, 3)
plt.plot(df_speicher['Datum'],df_speicher['Produktion_GWh'])
plt.xticks(df_speicher['Datum'][0::500])
plt.legend(['Speicherkraft'])

# Subplot Stromproduktion thermische Kraftwerke
plt.subplot(6, 1, 4)
plt.plot(df_therm['Datum'],df_therm['Produktion_GWh'])
plt.xticks(df_therm['Datum'][0::500])
plt.legend(['Thermische'])
plt.ylabel('Stromproduktion [GWh]')

# Subplot Stromproduktion aus Photovoltaik
plt.subplot(6, 1, 5)
plt.plot(df_photo['Datum'],df_photo['Produktion_GWh'])
plt.xticks(df_photo['Datum'][0::500])
plt.legend(['Photovoltaik'])

# Subplot Stromproduktion aus Windkraft
plt.subplot(6, 1, 6)
plt.plot(df_wind['Datum'],df_wind['Produktion_GWh'])
plt.xticks(df_wind['Datum'][0::500])
plt.legend(['Wind'])
plt.xlabel('Datum')

plt.show()


# ## 3. Vergleich zweier Energieträger: Scatterplot, lineare Regression und Korrelationkoeffizient
# 
# Die Korrelation zweier Zeitreihen kann visualisiert werden, indem man die Zeitreihen in einem Scatterplot gegeneinander aufträgt. Beispiel hier: Stromproduktion aus Flusskraft gegen Stromproduktion aus Photovoltaik. Als erstes visulalisieren wir beide Zeitreihen im gleichen Plot.

# In[10]:


## Matplotlib subplots
f, axs = plt.subplots(1,1, figsize=(12, 8))

lx1 = '2015-01-01' # unteres Limit x-Achse
lx2 = '2026-07-01' # oberes Limit y-Achse
ly1 = -2.0   # unteres Limit y-Achse
ly2 = 110.0 # oberes Limit y-Achse

plt.subplot(1, 1, 1)
plt.plot(df_fluss['Datum'],df_fluss['Produktion_GWh'])
plt.plot(df_photo['Datum'],df_photo['Produktion_GWh'])
plt.xticks(df_fluss['Datum'][0::550])
plt.xlim(lx1,lx2)
plt.ylim(ly1,ly2)
plt.legend(['Flusskraft','Photovoltaik']) # Beschriftung der Datensätze
plt.ylabel('Stromproduktion [GWh]')
plt.xlabel('Datum')

plt.show()


# ### Scatterplot zur Datenvisualisierung
# 
# Die Stromproduktion aus beiden Quellen wird gegeneinander aufgetragen. Dazu werden Zeitreihen gleicher Länge benötigt, wie sie in diesem Datensatz vorliegen. Bei Zeitreihen ungleicher Länge muss zuerst ein Ausschnitt gleicher Länge gewählt und als neue Zeitreihe gespeichert werden.

# In[11]:


plt.figure().set_figheight(5)
plt.figure().set_figwidth(10)
plt.scatter(df_fluss['Produktion_GWh'], df_photo['Produktion_GWh'], s=10, alpha=0.6, edgecolors="k") # Scatterplot Flusskrft gegen Photovoltaik
plt.xlabel('Flusskraft Stromproduktion [GWh]') # Beschriftung x-Achse
plt.ylabel('Photovoltaik Stromproduktion [GWh]') # Beschriftung y-Achse
plt.show()


# ### Lineare Regression
# 
# Die Korrelation der beiden Datensätze kann anhand der linearen Regression visualisiert werden. Zur Berechnung der Regression wird die Funktion numpy.polyfit() verwendet:
# 
# https://numpy.org/doc/stable/reference/generated/numpy.polyfit.html

# In[12]:


# Numpy importieren
import numpy as np


# Linearen Regression mit least squares mit np.polyfit() Das Resultat ist die Steigung (b) und Achsenabschitt (a) der Regressionslinie. Der Grad des Polynoms wird über deg=1 (linear) festgelegt.

# In[13]:


# Fitten der linearen Regression mit least squares with np.polyfit
b, a = np.polyfit(df_fluss['Produktion_GWh'], df_photo['Produktion_GWh'], deg=1)
print('b = ', b, '\ta =', a)


# In[14]:


plt.figure().set_figheight(5) # Breite
plt.figure().set_figwidth(10) # Höhe
plt.scatter(df_fluss['Produktion_GWh'], df_photo['Produktion_GWh'], s=10, alpha=0.6, edgecolors="k") # Scatterplot Flusskrft gegen Photovoltaik

# Sequenz der Zahlen von 10 bis 105 generieren (für Darstellung)
xseq = np.linspace(10, 105, num=100)

# Regressionslinie plotten
plt.plot(xseq, a + b * xseq, color="r", lw=2.0);

plt.xlabel('Flusskraft Stromproduktion [GWh]')  # Beschriftung x-Achse
plt.ylabel('Photovoltaik Stromproduktion [GWh]')  # Beschriftung y-Achse

plt.legend(['Datenpunkte','Lineare Regression']) # Beschriftung Daten
plt.show()


# ### Korrelationskoeffizient berechnen mit Numpy
# 
# Als Mass für die Korrelation von Datensätzen kann der Korrelationskoeffizient berechnet werden.
# 
#      1: maximale korrelation der Daten
#      0: keine Korrelation
#     -1: negative Korrelation
# 
# Die Korrelation kann mit numpy.corrcoef() berechnet werden. Berechnet wird dabei jeweils eine Korrelationsmatrix. Bei zwei Datensätzen als input sind die Diagonalelemente (0,0) und (1,1) jeweils 1, da sie der Korrelation der Datenätze mit sich selber entsprechen. Die Elemente (0,1) und (1,0) entsprechen der Korrelation der Datensätze miteinander.
# 
# https://numpy.org/doc/stable/reference/generated/numpy.corrcoef.html

# In[15]:


# Korrelationsmatrix berechnen
r = np.corrcoef(df_fluss['Produktion_GWh'], df_photo['Produktion_GWh'])

# Nicht-diagonale Elemente der Korrelationsmatrix ausgeben
print("Korrelationskoeffizient = ", r[0,1]) 


# In[ ]:




