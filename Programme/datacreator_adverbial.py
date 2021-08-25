# -*- coding: utf-8 -*-
"""
Created on Mon Feb 15 15:42:26 2021

@author: ameli
"""
''' Das Programm erstellt Datensätze aller adverbialen Vorkommen aus den mit datacreator.py
erstellten gesamten Datensätzen
Input: Die entsprechende mit datacreator.py erstellte .csv-Datei mit allen Vorkommen
Output: Eine .csv-Datei mit allen adverbialen Vorkommen; Eine .csv-Datei mit einem zufälligen
Subsample von n=200 '''
import pandas as pd
import os

################## manuell zu modifizierende Variablen ###########################
inputdatei = 'anders.csv'
adverbial = 'anders'
output = 'anders_adverbial.csv'
output200 = 'anders_adverbial_200.csv'
################## feststehende Variablen #########################################
os.chdir(r"..\Datensätze\gesamt\Adverbiale\rein")
df = pd.read_csv(inputdatei , sep=';')
# verbale Köpfe nach dem STTS 
sttsverbal = ['VMFIN','VAFIN','VVFIN','VAIMP','VVIMP','VVINF','VAINF','VMINF','VVIZU','VVPP','VMPP','VAPP']

#############################################
################# FUNKTIONEN ################
#############################################
def vhead (data,head):
    #prädikative Vorkommen werden aussortiert
    exception = ['sein', 'werden', 'erscheinen', 'heißen', 'bleiben', 'scheinen', 'wirken']
    df_verb = pd.DataFrame()
    for index, row in df.iterrows():
        if row['Function-Head'] in head:
            #sortiert bestimmte Verben aus
            if row['Head'] in exception:
                pass
            elif row['Head'] == '--':
                pass
            #elif row['sentence'].split()[row['ID-Token']-2] == ',':
             #   pass
            else:
                df_verb = df_verb.append(row, ignore_index = True)
    return(df_verb)


#erstellt einen Dataframe mit allen adverbialen Vorkommen und sortiert Duplikate aus    
out = vhead(df,sttsverbal).drop_duplicates()
out200 = out.sample(n=200)

##################################################
######## Ausgabe der Adverbialtabellen############
##################################################
os.chdir(r"..\..\..\annotiert\Adverbiale\rein")
out.to_csv(output, index=False)
out200.to_csv(output200, index=False)