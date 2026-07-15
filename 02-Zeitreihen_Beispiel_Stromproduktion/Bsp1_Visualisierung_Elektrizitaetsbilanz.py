#!/usr/bin/env python
# coding: utf-8

# # Beispiel 1: Einfache Visualisierungen der Elektrizitaetsbilanz
# 
# ### Datenvisualisierung mit Python/Matplotlib

# ### Datenbeispiel: Stromproduktion in der Schweiz
# 
# Datenquelle: Bundesamt für Energie
# Webseite: https://opendata.swiss/de/dataset/schweizerische-elektrizitatsstatistik-schweizerische-elektrizitatsbilanz-monatswerte
# 
# Zeitpunkt der Abfrage: 15.07.2026
# 
# Format: CSV (.csv)

# ## 1. Einlesen und Organisation der Daten
# 
# Zum importieren von CSV-Files kann das Modul **Pandas** verwendet werden.
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


# #### Datenfile lesen und anzeigen
# 
# Pandas stellt Reader für verschiedene Formate zur Verfügung. Der entsprechende Reader read_csv() wird ausgewählt und bekommt als Parameter den Filenamen. Die Daten werden dann im Dataframe df gespeichert.

# In[2]:


# CSV-file lesen
df = pd.read_csv('ogd35_schweizerische_elektrizitaetsbilanz_monatswerte.csv')


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
df['Endverbrauch_GWh']


# In[6]:


# Jeden 12. Datenpunkt einer Spalte auswählen (jeweils erster Monat im Jahr)
df['Endverbrauch_GWh'][::12]


# ## 2. Visualisierung der Elektrizitätsbilanz
# 
# Die Zeitreihen von Erzeugung, Verbrauch u.s.w. in den verschiedenen Spalten können nun zusammen oder separat visualisiert werden.

# #### Notwendige Module importieren

# In[7]:


# Matplotlib zum Erstellen der Grafiken
import matplotlib.pyplot as plt


# ### Visualisierung 1: Eine Zeitreihe visualisieren
# 
# Die Stromproduktion jedes Energieträgers über die Zeit ist eine Zeitreihe. 

# In[8]:


# Visualisierung der des Endverbrauchs
plt.figure().set_figheight(5) # Höhe des Plots
plt.figure().set_figwidth(15) # Breite des Plots
plt.rcParams.update({'font.size': 14}) # Schriftgrösse definieren

plt.plot(df['Endverbrauch_GWh']) # Plotten der Stromproduktion nach Datum

plt.xlabel('Index der Datenpunkte') # Beschriftung x-Achse
plt.ylabel('Endverbrauch [GWh]') # Beschriftung y-Achse

plt.title("Endverbrauch") # Titel des Plots

plt.show()


# ### Visualisierung 2: Mehrere Zeitreihen visualisieren
# 
# Um mehrere Zeitreihen zu vergleichen müssen diese in einem Plot kombiniert werden.

# In[9]:


# Visualisierung von Einfuhr und Ausfuhr
plt.figure().set_figheight(5) # Höhe des Plots
plt.figure().set_figwidth(15) # Breite des Plots
plt.rcParams.update({'font.size': 14}) # Schriftgrösse definieren

plt.plot(df['Einfuhr_GWh']) # Plotten der Stromproduktion nach Datum
plt.plot(df['Ausfuhr_GWh']) # Plotten der Stromproduktion nach Datum

plt.xlabel('Index der Datenpunkte') # Beschriftung x-Achse
plt.ylabel('Einfuhr/Ausfuhr[GWh]') # Beschriftung y-Achse

plt.legend(['Einfuhr', 'Ausfuhr'])

plt.title("Stromeinfuhr und -ausfuhr") # Titel des Plots

plt.show()


# Visualisierung der Daten in mehreren Subplots: die einzelnen Datensätze sind so gut zu erkennen.

# ### Visualisierung 3: Endverbrauch gegen Jahr auftragen
# 
# Zur Vereinfachung wird dafür hier nur jeder 12. Datenpunkt verwendet, jeweils der erste Monat des Jahres.

# In[10]:


# Visualisierung der des Endverbrauchs
plt.figure().set_figheight(5) # Höhe des Plots
plt.figure().set_figwidth(15) # Breite des Plots
plt.rcParams.update({'font.size': 14}) # Schriftgrösse definieren

plt.plot(df['Jahr'][::12], df['Endverbrauch_GWh'][::12]) # Plotten der Stromproduktion nach Datum

plt.xlabel('Jahr') # Beschriftung x-Achse
plt.ylabel('Endverbrauch [GWh]') # Beschriftung y-Achse

plt.title("Endverbrauch im Januar nach Jahr") # Titel des Plots

plt.show()


# ### Visualisierung 4: Erzeugung, Einfuhr, Ausfuhr und Endverbrauch im Januar gegen Jahr auftragen
# 
# Zur Vereinfachung wird dafür hier nur jeder 12. Datenpunkt verwendet, jeweils der erste Monat des Jahres.

# In[11]:


# Visualisierung der des Endverbrauchs
plt.figure().set_figheight(5) # Höhe des Plots
plt.figure().set_figwidth(15) # Breite des Plots
plt.rcParams.update({'font.size': 14}) # Schriftgrösse definieren

plt.plot(df['Jahr'][::12], df['Erzeugung_netto_GWh'][::12]) # Plotten der Stromproduktion nach Datum
plt.plot(df['Jahr'][::12], df['Einfuhr_GWh'][::12]) # Plotten der Stromproduktion nach Datum
plt.plot(df['Jahr'][::12], df['Ausfuhr_GWh'][::12]) # Plotten der Stromproduktion nach Datum
plt.plot(df['Jahr'][::12], df['Endverbrauch_GWh'][::12]) # Plotten der Stromproduktion nach Datum

plt.xlabel('Jahr') # Beschriftung x-Achse
plt.ylabel('Endverbrauch [GWh]') # Beschriftung y-Achse

plt.legend(['netto Erzeugung', 'Einfuhr', 'Ausfuhr', 'Endverbrauch'])

plt.title("Erzeugung, Einfuhr, Ausfuhr und Endverbrauch im Januar") # Titel des Plots

plt.show()


# In[ ]:




