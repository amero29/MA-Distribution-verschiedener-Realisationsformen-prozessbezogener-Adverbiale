# -*- coding: utf-8 -*-
"""
Created on Mon Jul 26 11:52:02 2021

@author: ameli
"""
''' Die hinsichtlich der semantischen Klasse annotierten verbalen Köpfe der 
prozessbezogenen Typen werden grafisch dargestellt.
Input: .xlsx-Datei, jeder Prozesstyp hat ein eigenes Arbeitsblatt
Output: Grafik 1: Verben nach Frequenz gewichtet.
        Grafik 2: Verben einfach gewertet.'''

####### Benötigte Packete ############
import pandas as pd
import os
import matplotlib.pyplot as plt
import matplotlib 

######################################
########## Parameter für #############
########## Grafik Ausgabe ############
######################################


matplotlib.use("pgf")
matplotlib.rcParams.update({
    "pgf.texsystem": "pdflatex",
    'font.family': 'serif',
    'text.usetex': True,
    'pgf.rcfonts': False,
})
plt.style.use('ggplot')

################ feststehende Variablen ##############
dict_heads ={}
dict_heads2 ={}


######################################
################# Pfad ###############
######################################
os.chdir(r"..\Datensätze\annotiert\verbaleKöpfe")
dirPath = r"..\verbaleKöpfe"
df_agens = pd.read_excel('Heads_Typen_aktuell.xlsx', sheet_name='agens')[:40]
df_rein = pd.read_excel('Heads_Typen_aktuell.xlsx', sheet_name='rein')[:40]
df_methode = pd.read_excel('Heads_Typen_aktuell.xlsx', sheet_name='methode')[:40]
df_degree = pd.read_excel('Heads_Typen_aktuell.xlsx', sheet_name='degree')[:40]
df_frequenz = pd.read_excel('Heads_Typen_aktuell.xlsx', sheet_name='frequenz')[:40]

def auswertung(df,name):
    dict_heads[name] = {}
    for index,row in df.iterrows():
        if row['ambig'] == 'yes':
            for element in row['SemanticNet Function'].split(';'):
                if element in dict_heads[name]:
                    dict_heads[name][element] += row['Vorkommen']
                else: dict_heads[name][element] = row['Vorkommen']
        else:
            if row['SemanticNet Function'] in dict_heads[name]:
                dict_heads[name][row['SemanticNet Function']] += row['Vorkommen']
            else: dict_heads[name][row['SemanticNet Function']] = row['Vorkommen']
    return()

def auswertung2(df,name):
    dict_heads2[name] = {}
    for index,row in df.iterrows():
        if row['ambig'] == 'yes':
            for element in row['SemanticNet Function'].split(';'):
                if element in dict_heads2[name]:
                    dict_heads2[name][element] += 1
                else: dict_heads2[name][element] = 1
        else:
            if row['SemanticNet Function'] in dict_heads2[name]:
                dict_heads2[name][row['SemanticNet Function']] += 1
            else: dict_heads2[name][row['SemanticNet Function']] = 1
    return()

auswertung(df_agens,'agensorientiert')
auswertung(df_degree,'Gradadv.')
auswertung(df_frequenz,'prozz. Freq.')
auswertung(df_methode,'methodenorientiert')
auswertung(df_rein,'reines ADV')

auswertung2(df_agens,'agens')
auswertung2(df_degree,'degree')
auswertung2(df_frequenz,'frequenz')
auswertung2(df_methode,'methode')
auswertung2(df_rein,'rein')

df_heads = pd.DataFrame.from_dict(dict_heads)
# Matrix transponieren
df_heads_T = df_heads.T
# Balkendiagramm ausgeben
df_heads.plot.bar(rot=90)
fig_1 = df_heads_norm = df_heads_T.div(df_heads_T.sum(1),axis=0)
fig_1 = plt.gcf()
fig_1.subplots_adjust(bottom=0.38)
fig_1.set_size_inches(w=6, h=4.5) 
plt.savefig('AuswertungHeadsTypen.pgf')

df_heads2 = pd.DataFrame.from_dict(dict_heads2)
# Matrix transponieren
df_heads2_T = df_heads2.T
# Balkendiagramm ausgeben
df_heads2.plot.bar(rot=90)
fig_1 = df_heads2_norm = df_heads2_T.div(df_heads2_T.sum(1),axis=0)
fig_1 = plt.gcf()
fig_1.subplots_adjust(bottom=0.38)
fig_1.set_size_inches(w=6, h=4.5) 
plt.savefig('AuswertungHeadsTypeneinfach.pgf')
