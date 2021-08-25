# -*- coding: utf-8 -*-
"""
Created on Wed Jun  2 11:51:09 2021

@author: ameli
"""
'''Die annotierten Datensätze des Prozesstyps methodenorientiert werden hinsichtlich
der Token-Head-Distanz ausgewertet
Input: Die annotierten methodenorientierten Datensätze als .csv
Output: Grafik 1: Token-Head-Distanz aller Inputdatensätze unterschieden zwischen methode und Bereich
        Grafik 2: absolute Werte der Vorkommen methode und Bereich'''

########### Benötigte Pakete ####################
import pandas as pd
import os
import matplotlib.pyplot as plt
import matplotlib

######## feststehende Variablen #################
vorkommen_dict = {'politisch':{'Methode':0,'Bereich':0},'ökologisch':{'Methode':0,'Bereich':0},'wissenschaftlich':{'Methode':0,'Bereich':0}}
distance_dict = {}
## Festlegen Output (.pgf), Parameter und Grafikstyle (ggplot)
matplotlib.use("pgf")
matplotlib.rcParams.update({
    "pgf.texsystem": "pdflatex",
    'font.family': 'serif',
    'text.usetex': True,
    'pgf.rcfonts': False,
})
plt.style.use('ggplot')

##############################################################
######################## Funktionen ##########################
##############################################################
def distance(token,name):
    distanz_methode = []
    distanz_bereich = []
    for index,row in token.iterrows():
        if row['Status'] == 'done':
            if row['Unterkategorie']=='methodenorientiert':
                distanz_methode.append(abs(row['ID-Head']-row['ID-Token']))
                vorkommen_dict[name]['Methode']+=1
            elif row['Unterkategorie']=='Frameadverbial':
                distanz_bereich.append(abs(row['ID-Head']-row['ID-Token']))
                vorkommen_dict[name]['Bereich']+=1
    distanz_methode = sum(distanz_methode)/len(distanz_methode)
    distanz_bereich = sum(distanz_bereich)/len(distanz_bereich)
    return([distanz_methode, distanz_bereich])


#########################################################
############### Erstellen der Dictionarys ###############
#########################################################
os.chdir(r"..\Datensätze\annotiert\Adverbiale\methode")
dirPath = r"..\methode"
result = next(os.walk(dirPath))[2]
for element in result:
    name = element.split('_')[0]
    data = pd.read_csv(element, sep=';')
    distance_dict[name] = distance(data,name)

##################################
########## Grafiken ##############
##################################
df_distanz = pd.DataFrame.from_dict(distance_dict, orient='index', columns =['Methode','Bereich'])
df_distanz.sort_values('Methode').plot.bar(rot=30,color={'Methode':'green','Bereich':'orange'}).legend(loc='center left',bbox_to_anchor=(1.0, 0.5))

os.chdir(r".\Grafiken")
dirPath = r".\Grafiken"
# Normalisieren
fig_1 = df_distanz_norm = df_distanz.div(df_distanz.sum(1),axis=0)
fig_1 = plt.gcf()
fig_1.subplots_adjust(bottom=0.26,right = 0.7)
fig_1.set_size_inches(w=5, h=2.5) 
plt.savefig('THDMethode.pgf')

df_vorkommen = pd.DataFrame.from_dict(vorkommen_dict, orient='index', columns =['Methode','Bereich'])
df_vorkommen.sort_values('Methode').plot.bar(rot=30)
fig_2 = df_vorkommen_norm = df_vorkommen.div(df_vorkommen.sum(1),axis=0)
fig_2 = plt.gcf()
fig_2.subplots_adjust(bottom=0.26)
fig_2.set_size_inches(w=4, h=2.5)
plt.savefig('VorkommenMethode.pgf')
