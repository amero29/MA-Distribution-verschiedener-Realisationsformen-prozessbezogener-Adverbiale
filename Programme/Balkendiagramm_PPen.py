# -*- coding: utf-8 -*-
"""
Created on Mon Jul 12 13:09:03 2021

@author: ameli
"""
'''
Aus den annotierten PP-Datensätzen werden die häufigsten Nomen und verbalen Köpfe 
als Latextabelle extrahiert, sowie Säulendiagramme der Adverbialtypen zu jeder PP erstellt.
Input: .csv-Dateien mit annotierten (Prozesstyp) Präpositionalphrasen
Output: .txt-Datein mit Latex Code für die je 7 häufigsten Verben und Nomen 
        .pgf-Datei mit den Grafiken zur Typenverteilung innerhalb der PPen'''
## Benötigte Pakete
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

############ feste Variablen ################
dict_PP = {}
dict_verbs = {}
dict_nouns = {}
##############################################################
######################## Funktionen ##########################
##############################################################
def prozesstypen(datensatz):
    verben = {}
    nomen = {}
    dict_out={'np':0, 'Sonstige':0, 'agens':0, 'rein':0, 'degree':0, 'methode':0}
    for index, row in datensatz.iterrows(): 
        ##### VERBEN#######
        if row['cor_conceptual_head_+1_lemma'] in verben:
            verben[row['cor_conceptual_head_+1_lemma']]+=1
        else: verben[row['cor_conceptual_head_+1_lemma']] =1
        ##### NOMEN #######
        if row['target_noun_lemma'] in nomen:
            nomen[row['target_noun_lemma']]+=1
        else: nomen[row['target_noun_lemma']] =1
        #####Typenverteilung ######
        if row['prozess']=='yes':
            if row['Typ'] in dict_out.keys():
                dict_out[row['Typ']]+=1
            else: 
                dict_out[row['Typ']]=1
        elif row['prozess']=='no':
            dict_out['np']+=1
        elif row['Status'] == 'not_of_interest':
            dict_out['Sonstige']+=1
        elif row['Status'] == 'problem':
            dict_out['Sonstige']+=1
    return(dict_out,verben,nomen)

#########################################################
############### Erstellen der Dictionarys ###############
#########################################################

os.chdir(r"..\Datensätze\annotiert\PPen")
dirPath = r"..\PPen"
result = next(os.walk(dirPath))[2]

for element in result:
    name = element.split('_')[0]
    data = pd.read_csv(element, sep=';')[0:100]
    dict_PP[name] = prozesstypen(data)[0]
    dict_verbs[name] = prozesstypen(data)[1]
    dict_nouns[name] = prozesstypen(data)[2]

#########################################################
################# Ausgabe der Tabellen ##################
#########################################################
os.chdir(r".\Auswertung")
dirPath = r"..\Auswertung"
####################### Verben ##########################
for pp in dict_verbs:
    df_verbs = pd.DataFrame()
    name = str(pp.split('_')[0]+'_verbs.txt')
    df_verbs = df_verbs.append(pd.DataFrame.from_dict(dict_verbs[pp].items()).sort_values([1],ascending = False)[:7])
    df_verbs.to_latex(name, index=False)

######################## Nomen ##########################
for pp in dict_nouns:
    df_nouns = pd.DataFrame()
    name = str(pp.split('_')[0]+'_nouns.txt')
    df_nouns = df_nouns.append(pd.DataFrame.from_dict(dict_nouns[pp].items()).sort_values([1],ascending = False)[:7])
    df_nouns.to_latex(name, index=False)
    
##################################
########## Grafiken ##############
##################################
df = pd.DataFrame.from_dict(dict_PP)
df_mit = df.drop(['in','ohne'],axis=1)
df_ohne = df.drop(['in','mit'],axis=1)
df_in = df.drop(['ohne','mit'],axis=1)
##################################
##### Subplots kombinieren########
##################################
colors = [['black','black','blue','blue','blue','blue']]
fig, (ax1, ax2, ax3) = plt.subplots(1,3)

df_mit.plot(ax=ax1, kind='bar', legend=False, rot=90, color=colors)
ax1.set_title('mit')
ax1.set_xlabel('n=100')

df_ohne.plot(ax=ax2, kind='bar',legend=False, rot=90, color=colors)
ax2.set_title('ohne')
ax2.set_xlabel('n=100')

df_in.plot(ax=ax3, kind='bar',legend=False, rot=90, color=colors)
ax3.set_title('in')
ax3.set_xlabel('n=40')

fig.subplots_adjust(bottom=0.2)

plt.savefig('prozesstypen_PPen.pgf')