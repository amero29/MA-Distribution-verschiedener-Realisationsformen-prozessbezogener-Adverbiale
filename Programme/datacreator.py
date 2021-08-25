# -*- coding: utf-8 -*-
"""
Created on Sun Aug 22 11:52:48 2021

@author: ameli
"""
'''Aus den NZZ-Basisdaten werden Datensätze mit allen Vorkommen des gegebenen 
Tokens generiert, Metadaten eingeschlossen.
Input: Geparste NZZ-Datensätze als .csv-Datei
Outpus: Datensatz mit allen Vorkommen des Tokens als .csv-Datei'''
import pandas as pd
import csv
import os

################## manuell zu modifizierende Variablen ###########################
adverbial = 'schlecht'
outputname = 'schlecht.csv'

'''Pfad zu den NZZ-Gesamtdatensätzen als .csv-Datei, jeder Monat ist eine eigene Datei
Es handelt sich um absolute Pfade, bitte manuell anpassen!'''
os.chdir(r"C:\Users\ameli\Documents\Uni\Masterarbeit\Daten\Basisdaten\alle Jahre")
dirPath = r"C:\Users\ameli\Documents\Uni\Masterarbeit\Daten\Basisdaten\alle Jahre"
result = next(os.walk(dirPath))[2]

################## feste Variablen
dict_data={}
sentence=""
conll =[]
ID = 0
match = 'NO'
adverbial = 'schlecht'
idnzz=""
synt = "LEER"
head="LEER"
t_id =0

#############################################
###################FUNKTIONEN################
#############################################
'''Alle Sätze, die das entsprechende Token enthalten werden in einem Dictionary
(dict_data) mit allen relevanten Werten gespeichert'''
def vorhanden(gesamt,adv,syn_f,kopf,ges_tag,kopf_id):
    if adv in gesamt:
        for element in conll:
            if adv in element[0].split("\t"):
                token_id = element[0].split("\t")[0]
                syn_f = element[0].split("\t")[4]
                kopf_id = 0
                kopf = "No Head"
                kopf_function = "No Head"
                kopf_info = "No Head"
                try:
                    kopf_id = int(element[0].split("\t")[6])
                # Dem Token ist kein Head zugeordnet
                except:
                    kopf_id = "No Head"
                for token in ges_tag:
                    if type(token[0])==str:
                        token_list = token[0].split("\t")
                    else:
                        token_list = token[0]
                    #fehlerhafte Zeile
                    if token_list[0] in [' \n', ' "1']:
                        pass
                    #fehlerhafte Zeile
                    elif "\nNZZ" in token_list[0]:
                        pass
                    elif int(token_list[0])==kopf_id:
                        if len(token_list) < 3:
                            kopf = "No Head"
                            kopf_function = "No Head"
                        else:
                            # unflektierte Form des Kopfes
                            kopf = token_list[2]
                            kopf_info = token_list[5]
                            kopf_function = token_list[3]
                dict_data[ID]=[idnzz,sentence,syn_f,kopf,kopf_id,kopf_info,kopf_function,token_id]
                return()
        


######TU DIES FüR ALLE FILES DES ORDNERS#######
for datei in result:
    with open(datei, encoding='utf-8') as csvdatei:
        csv_reader_object = csv.reader(csvdatei)
        for row in csv_reader_object:
            if row ==[]:
                vorhanden(sentence.split(),adverbial,synt,head,conll,t_id)
                sentence = ""
                conll=[]
                idnzz=""
                match = 'NO'
                synt = "LEER"
                head="LEER"
                t_id=0
                
            else:
                if len(row)==1:
                    if "NZZ_" in str(row):
                        row = str(row).split(";")
                        idnzz = row[0][2:]
                        conll.append(row[1].split("\\t"))
                        if len(conll[0])>1:
                            sentence = sentence + str(conll[0][1])
                            if str(conll[0][1]) == adverbial:
                                match = str(conll[0][1])
                            if "nNZZ" in idnzz:
                                idnzz = idnzz[3:]
                            ID+=1
                        ##sortiert Zeilenumbrüche aus
                        else: 
                            pass
                    else:
                        conll_new = row[0].split("\\t")
                        #print(conll_new)
                        conll.append(row)
                        token = conll_new[0].split()
                        #print(conll_new[0].split())
                        if len(token)>=1:
                            sentence = sentence +" "+ token[1]
                            if token[1]==adverbial:
                                match = token[1]
                else: 
                    conll.append(row)
                    if len(row)==5:
                        sentence = sentence + " ,"
                    elif len(row) > 0:
                        sentence = sentence + " "+row[1].split()[0]
                    else:
                        pass
                    
                            
                    
                    
                    
            
###################################################
############ Dictionary in Data-Frame #############
###################################################           
df_adv = pd.DataFrame.from_dict(dict_data, orient='index', columns=["ID-NZZ","sentence","Funktion-Hit","Head", "ID-Head","Meta-Kopf","Function-Head","ID-Token"])


##################################################
######## Ausgabe der Adverbialtabelle ############
##################################################
'''absoluten Pfad manuell anpassen'''
os.chdir(r"C:\Users\ameli\Desktop\Masterarbeit")
dirPath = r"C:\Users\ameli\Desktop\Masterarbeit"
df_adv.to_csv(outputname, index=False)
