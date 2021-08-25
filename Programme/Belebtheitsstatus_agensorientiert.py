# -*- coding: utf-8 -*-
"""
Created on Mon Feb 15 15:42:26 2021

@author: ameli
"""

import pandas as pd
import os
import matplotlib.pyplot as plt
import matplotlib

########### feststehende Variablen ##############
dict_anim = {}
########### Benötigte Pakete ####################
agens =['anim','inanim','anim_like','unknown','else','ambiguous','coc']
sonstiges_list = []
## Festlegen Output (.pgf), Parameter und Grafikstyle (ggplot)
matplotlib.use("pgf")
matplotlib.rcParams.update({
    "pgf.texsystem": "pdflatex",
    'font.family': 'serif',
    'text.usetex': True,
    'pgf.rcfonts': False,
})
plt.style.use('ggplot')

##################################################
################# Funktionen #####################
##################################################
def belebtheit(datensatz):
    werte ={'anim':0,'inanim':0,'anim_like':0,'unknown':0,'else':0,'ambiguous':0,'coc':0}
    for index, row in datensatz.iterrows(): 
        if row['Status']=='done':
            if row['Agens'] == 'anim':
                werte['anim'] +=1
            elif row['Agens'] == 'inanim':
                werte['inanim'] +=1
            elif row['Agens'] == 'anim_like':
                werte['anim_like'] +=1
            elif row['Agens'] == 'unknown':
                werte['unknown'] +=1
            elif row['Agens'] == 'ambiguous':
                werte['unknown'] +=1
            elif row['Agens'] == 'clash of coordination':
                werte['coc'] +=1
            else: print(row['Agens'])
    return(werte)

os.chdir(r"..\Datensätze\annotiert\Adverbiale\agens")
dirPath = r"..\agens"
result = next(os.walk(dirPath))[2]

for element in result:
    name = element.split('_')[0]
    data = pd.read_csv(element, sep=';')
    dict_anim[name] = belebtheit(data)
 
    
##################################
########## Grafiken ##############
##################################
os.chdir(r".\Grafiken")
dirPath = r".\Grafiken"   
df_bd_agens = pd.DataFrame.from_dict(dict_anim)
# Matrix transponieren
df_bd_agens_T = df_bd_agens.T
# Balkendiagramm ausgeben
df_bd_agens_T.plot.bar(rot=30).legend(loc='center left',bbox_to_anchor=(1.0, 0.5))
# Normalisieren
fig_1 = df_bd_agens_norm = df_bd_agens_T.div(df_bd_agens_T.sum(1),axis=0)
fig_1 = plt.gcf()
fig_1.subplots_adjust(bottom=0.25,right=0.75)
fig_1.set_size_inches(w=5, h=3) 
plt.savefig('AGENS.pgf')
#gestapeltes Balkendiagramm
fig = df_bd_agens_norm.plot.barh(stacked=True).legend(loc='center left',bbox_to_anchor=(1.0, 0.5))
fig = plt.gcf()
fig.subplots_adjust(right=0.75,left=0.15)
fig.set_size_inches(w=5, h=2) 
plt.savefig('agensverteilung.pgf')


