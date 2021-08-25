# -*- coding: utf-8 -*-
"""
Created on Sat Aug 21 11:42:19 2021

@author: ameli
"""


'''Programm zur Erstellung der normalisierten und nicht normalisierten Balkendiagramme
der Verteilung der syntaktischen Funktionen für die einzelnen prozessbezogenen Adverbialtypen 
+ normalisierte Gesamtübersicht
Input: Die mit datacreator.py erstellten Gesamtdatensätze zu den einzelnen Token
Output: Die Grafiken als .pfg-Datei zur Einbindung in Latex'''


import pandas as pd
import os
import matplotlib.pyplot as plt
import matplotlib

## Festlegen Output (.pgf), Parameter und Grafikstyle (ggplot)
matplotlib.use("pgf")
matplotlib.rcParams.update({
    "pgf.texsystem": "pdflatex",
    'font.family': 'serif',
    'text.usetex': True,
    'pgf.rcfonts': False,
})
plt.style.use('ggplot')


###############################################
################ Variablen ####################
###############################################
'''Definieren der syntaktischen Kategorien nach STTS-Tags und spezifischen Lexemen'''

praedikativ = ['sein', 'werden', 'erscheinen', 'heißen', 'bleiben', 'scheinen']
adverbial = ['VMFIN','VAFIN','VVFIN','VAIMP','VVIMP','VVINF','VAINF','VMINF',
             'VVIZU','VVPP','VMPP','VAPP']
attributiv = ['NN','NE','PPER','PRF','PPOSAT','PPOSS','PDAT','PDS','PIAT','PDAT'
              ,'PIS','PRELAT','PRELS','PWAT','PWS','PWAV']
modifikator = ['ADJA','ADJD','CARD','PAV','ADV','APPR','APPRART','APPO','APZR']

dict_funct = {'rein':{},'agens':{},'degree':{},'methode':{},'frequenz':{}}
dict_sonst = {}
##################################################
################# Funktionen #####################
##################################################

'''Für den gegebenen Datensatz werden die syntaktischen Realisierungen ausgezählt 
und in einem Dictionary (werte) zurückgegeben'''
def synt_funktion(datensatz):
    werte = {"attributiv":0, "prädikativ":0, "adverbial": 0, "modifikator": 0, "sonstiges": 0}
    for index, row in datensatz.iterrows():
        if row['Head'] in praedikativ:
            werte["prädikativ"]+=1
        elif row['Function-Head'] in adverbial:
            werte["adverbial"]+=1
        elif row['Function-Head'] in modifikator:
            werte["modifikator"]+=1
        elif row['Function-Head'] in attributiv:
            werte["attributiv"]+=1
        else:
            werte["sonstiges"] += 1
            # Erstellen eines Dictionaries zur Auswertung der 'Sonstigen'
            if row['Function-Head'] in dict_sonst.keys():
                dict_sonst[row['Function-Head']]+=1
            else: 
                dict_sonst[row['Function-Head']]=1
    return(werte)

#################################################
############## reine Adverbiale #################
#################################################
os.chdir(r"..\Datensätze\gesamt\Adverbiale\rein")
dirPath = r"..\rein"
result = next(os.walk(dirPath))[2]
for element in result:
    name = element.split('.')[0]
    data = pd.read_csv(element, sep=';',dtype={'ID-Head':'str'})
    dict_funct['rein'][name]=synt_funktion(data)

df_rein = pd.DataFrame.from_dict(dict_funct['rein'])
################################################
####### Agensorientierte Adverbiale ############
################################################    
os.chdir(r"..\agens")
dirPath = r"..\agens"
result = next(os.walk(dirPath))[2]

for element in result:
    name = element.split('.')[0]
    data = pd.read_csv(element, sep=';',dtype={'ID-Head':'str'})
    dict_funct['agens'][name]=synt_funktion(data)

df_agens = pd.DataFrame.from_dict(dict_funct['agens'])
df_gesamt = df_rein.join(df_agens)
################################################
############### Gradadverbiale #################
################################################    
os.chdir(r"..\degree")
dirPath = r"..\degree"
result = next(os.walk(dirPath))[2]

for element in result:
    name = element.split('.')[0]
    data = pd.read_csv(element, sep=';',dtype={'ID-Head':'str'})
    dict_funct['degree'][name]=synt_funktion(data)
 
df_degree = pd.DataFrame.from_dict(dict_funct['degree'])
df_gesamt = df_gesamt.join(df_degree)
################################################
###### Methodenorientierte Adverbiale ##########
################################################  
os.chdir(r"..\method")
dirPath = r"..\method"
result = next(os.walk(dirPath))[2]

for element in result:
    name = element.split('.')[0]
    data = pd.read_csv(element, sep=';',dtype={'ID-Head':'str'})
    dict_funct['methode'][name]=synt_funktion(data)

df_methode = pd.DataFrame.from_dict(dict_funct['methode'])
df_gesamt = df_gesamt.join(df_methode)
################################################
######## Prozessbezogene Frequenzen ############
################################################  
os.chdir(r"..\frequency")
dirPath = r"..\frequency"
result = next(os.walk(dirPath))[2]

for element in result:
    name = element.split('.')[0]
    data = pd.read_csv(element, sep=';',dtype={'ID-Head':'str'})
    dict_funct['frequenz'][name]=synt_funktion(data)

df_frequenz = pd.DataFrame.from_dict(dict_funct['frequenz'])
df_gesamt = df_gesamt.join(df_frequenz)

################################################
##### Erstellen und Ausgeben der Grafiken ######
################################################
os.chdir(r"..")
dirPath = r"."
################################################
############## Gesamtübersicht #################
################################################
df_gesamt_T=df_gesamt.T.sort_values(by='adverbial', ascending=True)
fig_gesamt = df_gesamt_norm = df_gesamt_T.div(df_gesamt_T.sum(1),axis=0)
fig_gesamt  = df_gesamt_norm.plot.barh(stacked=True).legend(loc='center left',bbox_to_anchor=(1.0, 0.5))
fig_gesamt  = plt.gcf()
fig_gesamt .subplots_adjust(right=0.75,left=0.2)
fig_gesamt .set_size_inches(w=5, h=3.5) 
plt.savefig('GESAMT.pgf')
plt.close()
#################################################
############## reine Adverbiale #################
#################################################
# Matrix transponieren
df_rein_T = df_rein.T.sort_values(by='adverbial', ascending=False)
df_rein_T2 = df_rein.T.sort_values(by='adverbial', ascending=True)
# Balkendiagramm ausgeben
df_rein_T.plot.bar(rot=30)
fig_rein_1 = df_rein_1 = df_rein_T.div(df_rein_T.sum(1),axis=0)
fig_rein_1 = plt.gcf()
fig_rein_1.subplots_adjust(left = 0.15, bottom=0.25)
fig_rein_1.set_size_inches(w=5, h=3) 
plt.savefig('REIN.pgf')
#normalisiertes, gestapeltes Balkendiagramm
fig_rein_2 = df_rein_norm2 = df_rein_T2.div(df_rein_T2.sum(1),axis=0)
fig_rein_2 = df_rein_norm2.plot.barh(stacked=True).legend(loc='center left',bbox_to_anchor=(1.0, 0.5))
fig_rein_2 = plt.gcf()
fig_rein_2.subplots_adjust(right=0.75,left=0.2)
fig_rein_2.set_size_inches(w=5, h=2) 
plt.savefig('REIN_NORM.pgf')
plt.close()
################################################
####### Agensorientierte Adverbiale ############
################################################ 
# Matrix transponieren
df_agens_T = df_agens.T.sort_values(by='adverbial', ascending=False)
df_agens_T2 = df_agens.T.sort_values(by='adverbial', ascending=True)
# Balkendiagramm ausgeben
df_agens_T.plot.bar(rot=30)
fig_agens_1 = df_agens_1 = df_agens_T.div(df_agens_T.sum(1),axis=0)
fig_agens_1 = plt.gcf()
fig_agens_1.subplots_adjust(bottom=0.25)
fig_agens_1.set_size_inches(w=5, h=3) 
plt.savefig('AGENS.pgf')
#gestapeltes, normalisiertes Balkendiagramm
fig_agens_2 = df_agens_norm2 = df_agens_T2.div(df_agens_T2.sum(1),axis=0)
fig_agens_2 = df_agens_norm2.plot.barh(stacked=True).legend(loc='center left',bbox_to_anchor=(1.0, 0.5))
fig_agens_2 = plt.gcf()
fig_agens_2.subplots_adjust(right=0.75,left=0.15)
fig_agens_2.set_size_inches(w=5, h=2) 
plt.savefig('AGENS_NORM.pgf')
plt.close()
################################################
############### Gradadverbiale #################
################################################
# Matrix transponieren
df_degree_T = df_degree.T.sort_values(by='adverbial', ascending=False)
df_degree_T2 = df_degree.T.sort_values(by='adverbial', ascending=True)
# Balkendiagramm ausgeben
df_degree_T.plot.bar(rot=30)
fig_degree_1 = df_degree_1 = df_degree_T.div(df_degree_T.sum(1),axis=0)
fig_degree_1 = plt.gcf()
fig_degree_1.subplots_adjust(left = 0.15, bottom=0.25)
fig_degree_1.set_size_inches(w=5, h=3) 
plt.savefig('DEGREE.pgf')
#gestapeltes, normalisiertes Balkendiagramm
fig_degree_2 = df_degree_norm2 = df_degree_T2.div(df_degree_T2.sum(1),axis=0)
fig_degree_2 = df_degree_norm2.plot.barh(stacked=True).legend(loc='center left',bbox_to_anchor=(1.0, 0.5))
fig_degree_2 = plt.gcf()
fig_degree_2.subplots_adjust(right=0.75,left=0.2)
fig_degree_2.set_size_inches(w=5, h=3) 
plt.savefig('DEGREE_NORM.pgf')
plt.close()
################################################
###### Methodenorientierte Adverbiale ##########
################################################ 
# Matrix transponieren
df_methode_T = df_methode.T.sort_values(by='adverbial', ascending=False)
df_methode_T2 = df_methode.T.sort_values(by='adverbial', ascending=True)
# Balkendiagramm ausgeben
df_methode_T.plot.bar(rot=30)
fig_methode_1 = df_methode_norm = df_methode_T.div(df_methode_T.sum(1),axis=0)
fig_methode_1 = plt.gcf()
fig_methode_1.subplots_adjust(left = 0.15, bottom=0.25)
fig_methode_1.set_size_inches(w=5, h=3) 
plt.savefig('METHODE.pgf')
#gestapelte, normalisiertes Balkendiagramm
fig_methode_2 = df_methode_norm2 = df_methode_T2.div(df_methode_T2.sum(1),axis=0)
fig_methode_2 = df_methode_norm2.plot.barh(stacked=True).legend(loc='center left',bbox_to_anchor=(1.0, 0.5))
fig_methode_2 = plt.gcf()
fig_methode_2.subplots_adjust(right=0.75,left=0.25) 
fig_methode_2.set_size_inches(w=5, h=2) 
plt.savefig('METHODE_NORM.pgf')
plt.close()

################################################
######## Prozessbezogene Frequenzen ############
################################################ 
# Matrix transponieren
df_frequenz_T2 = df_frequenz.T.sort_values(by='adverbial', ascending=True)
df_frequenz_T= df_frequenz.T.sort_values(by='adverbial', ascending=False)
# Balkendiagramm ausgeben
df_frequenz_T.plot.bar(rot=30).legend(loc='center left',bbox_to_anchor=(1.0, 0.5))
fig_frequenz_1 = df_frequenz_norm = df_frequenz_T.div(df_frequenz_T.sum(1),axis=0)
fig_frequenz_1  = plt.gcf()
fig_frequenz_1 .subplots_adjust(right = 0.75, bottom=0.25) 
fig_frequenz_1 .set_size_inches(w=5, h=2.5) 
plt.savefig('FREQUENZ.pgf')
#normalisiertes, gestapeltes Balkendiagramm
fig_frequenz_2 = df_frequenz_norm2 = df_frequenz_T2.div(df_frequenz_T2.sum(1),axis=0)
fig_frequenz_2  = df_frequenz_norm2.plot.barh(stacked=True).legend(loc='center left',bbox_to_anchor=(1.0, 0.5))
fig_frequenz_2  = plt.gcf()
fig_frequenz_2.subplots_adjust(right=0.75,left=0.21)
fig_frequenz_2.set_size_inches(w=5, h=2) 
plt.savefig('FREQUENZ_NORM.pgf')
plt.close()




















 