#!/usr/bin/env python
# coding: utf-8

# # Datenvisualisierung mit Python/Matplotlib: Grundlagen
# 
# Grundlagen der Datenvisualisierung mit Matplotlib: Einfache Visualisierung von Funktionen und Daten.
# 
# Die benötigten Pythonmodule **NumPy** und **MatPlotLib** sind in den meisten Installation schon dabei; für Teil 2 dieses Notebooks muss **SciPy** dazu installiert werden. Installieren von SciPy mit Anaconda (im Anaconda Prompt (Windows) oder Terminal (Linux oder MacOS):
# 
#     conda install scipy
# 

# ## 1. Visualisierung einfacher Funktionen

# #### Module für Teil 1 importieren
# 
# Für Teil 1 werden NumPy und MatPlotLib benötigt.

# In[1]:


#NumPy importieren
import numpy as np


# In[2]:


# MatPlotLib importieren
import matplotlib.pyplot as plt


# #### Daten einer einfachen Funktion generieren

# In[3]:


# Definition der Punkte auf der x-Achse:
start = 0 # Anfangspunkt
end = 10 # Endpunkt
interval = 0.2 # Abstand der Punkte


# In[4]:


# Generieren der Punkte auf der x-Achse mit numpy.arange
x = np.arange(start, end, interval)
print("Datenpunkte auf der x-Achse:\n", x)


# In[5]:


# Funktionswerte (y-Werte) berechnen (sin(x))
y1 = np.sin(x)
print("Funktionswerte auf der y-Achse:\n", y1)


# #### Einfache Funktion plotten
# 
# Auftragen der Funktionswerte auf der y-Achse gegen die Datenpunkte auf der x-Achse

# In[6]:


plt.title("Einfache Visualisierung einer Funktion") # Titel des Plots
plt.xlabel('x') # Beschriftung der x-Achse
plt.ylabel('y') # Beschriftung der y-Achse
plt.plot(x,y1) # Funktion plotten: x, y1
plt.show


# #### Mehrere Funktionen plotten und labeln
# 
# Bei mehreren Datensätzen in einem Plot sollten die einzelnen Sets beschriftet sein.

# In[7]:


# y-Werte der Funktionen generieren
y2 = np.cos(x)
y3 = np.sin(x)*0.3


# In[8]:


plt.title("Einfache Visualisierung mehrerer Funktion") # Titel des Plots
plt.xlabel('x') # Beschriftung der x-Achse
plt.ylabel('y') # Beschriftung der y-Achse
plt.plot(x,y1) # Funktion plotten: x, y1
plt.plot(x,y2) # Funktion plotten: x, y2
plt.plot(x,y3) # Funktion plotten: x, y3
plt.legend(['cos(x)', 'sin(x)', 'sin(x)*0.3']) # Beschriftung der Datensätze
plt.show


# ## 2. Eigene Daten generieren: Brownsche Bewegung in einer Dimension
# 
# Die Brownsche Bewegung ist eine sehr einfache Diffusionsbewegung, die experimentell beobachtet werden kann. Mathematisch entspricht sie einer kummulativen Summe von normalverteilten Zufallszahlen.
# 
# Brownsche Bewegung: Erklärung bei Wolfram Alpha: 
# https://www.wolframalpha.com/input?i=Brownian+motion
# 
# Link zum SciPy Cookbook:
# https://scipy-cookbook.readthedocs.io/items/BrownianMotion.html
# 
# Von SciPy wird die Funktion scipy.stats.norm() benötigt: https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.norm.html
# Damit können normalverteilte Zufallszahlen generiert werden.

# In[9]:


# Scipy: benötigte Funktionen importieren
from scipy.stats import norm


# #### Einfache Berechnung der Brownschen Bewegung

# In[10]:


# Parameter definieren
delta = 0.25 # Paramenter für die Geschwindigkeit der Brownschen Bewegung 
dt = 0.1 # Zeitschritt
x = 0.0 # Ansfangsbedingung (Anfangsposition)
n = 60 # Anzahl Schritte


# In[11]:


# Berechnen der Brownschen Bewegung über n Schritte im Zeitabstand dt
traj = [] # Leere Liste für Trajektoriendaten
zeit = [] # Leere Liste für Zeitpunkte
# Daten generieren
for k in range(n):  # Loop über n Schritte
    tn = k*dt # Berechnung des Zeitpunkts
    x = x + norm.rvs(scale=delta**2*dt) # Berechnung der neuen Position mit scipy.stats.norm; scale: Standardabweichung
    traj.append(x) # Speichern der neuen Position
    zeit.append(tn) # Zeitpunkt speichern
print(traj)


# #### Daten visualisieren

# In[12]:


plt.title("Brownsche Bewegung in 1D") # Titel des Plots
plt.xlabel('Zeit [arbitrary units]') # Beschriftung der x-Achse
plt.ylabel('Position [arbitrary units]') # Beschriftung der y-Achse
plt.plot(traj, 'o:b') # Funktion plotten: Trajektoriendaten gegen Zeit
plt.savefig('Brownsche_Bewegung_1D.png')
plt.show


# In[ ]:




