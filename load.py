#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 20 10:58:30 2017

@author: sgmap
"""

import os
import re
import pandas as pd

from os.path import join

#######################
### Aproche via jurinet
#######################

### On a ici que les décisions d'appel...

# from jurinet.appariement.jurinet_data import load_jurinet
#tab = load_jurinet()
#contient_prud = tab.XML.str.contains("prud'hom")
## attention avec prud'homm parde ce que l'adjectif n'a qu'un m
#print(contient_prud.value_counts())
#
#l_un_pas_l_autre = tab.XML.str.contains("prud'homm")
#print(l_un_pas_l_autre.value_counts())
#
#prud = tab[(contient_prud) & (~l_un_pas_l_autre)]
#print(prud.XML.iloc[23])


#######################
### Aproche via dila data
#######################

# On ne trouve rien
#from appariement.dila_data import get_dila_text_by_numero, get_dila_text_infos
#infos_juritext = get_dila_text_infos()
#get_dila_text_by_numero("07/1064", infos_juritext)
#
#
#liste_prudhomme = []
#liste_path = []
#counter = 0
#for titre in infos_juritext['TITRE'].keys():
#    if "PRUD" in titre or "Prud" in titre or "prud" in titre:
#        liste_prudhomme.append(counter)
#        print(titre)
#    counter += 1


#######################
### Aproche a la mano
#######################

#mots_cles = ["jugement", "entre", "procédure", "EXPOSE DU LITIGE",
#             "EN DROIT", "PAR CES MOTIFS", "MOTIVATION"]
#
## NOTE : deux type, référé et jugement
#        
#path = "D:\data\jurinet\prudhomme"
#for file in os.listdir(path):
#    if file != "README.txt":
#        print("*****", file)
#        with open(join(path, file), encoding='utf8') as f:
#            text = f.read()
#        for mot_cle in mots_cles:
#            if (mot_cle.upper() in text or 
#                mot_cle.lower() in text or 
#                mot_cle.capitalize() in text or
#                ' '.join(mot_cle.upper()) in text
#                ):
#                print(mot_cle, "ok")
#            else:
#                print(mot_cle, "not_ok")



path_data_recues = '/home/sgmap/data/prudhomme'
path_data_recues = 'D:\data\prudhommes'

def pdf_to_text():
    import PyPDF2
    for filename in os.listdir(path_data_recues):
        if filename.endswith('.pdf'):
            pdfFileObj = open(join(path_data_recues, filename), 'rb')
            pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
            all_text = ''
            for num_page in range(pdfReader.numPages):
                pageObj = pdfReader.getPage(num_page)
                text = pageObj.extractText()
                all_text += text + '\n saut de ligne \n'
            with open(join(path_data_recues, filename[:-4] + '.txt'), 'w',
                      encoding='utf8') as f:
                f.write(all_text)
            pdfFileObj.close()



def jurinet_2015_prudhom():
    from jurinet.appariement.jurinet_data import load_jurinet
    jurinet = load_jurinet()
    # on ne retrouve pas le fichiers de l'échantillon (probablement parce qu'ils
    # sont trop vieux, et qu'on a jurinet 2015 seulement)

    # on isole tout de même les textes de jurisprudence
    XML = jurinet.TEXTE_ARRET
    cond = XML.str.contains("prud'hom") | XML.str.contains("Prud'hom") | XML.str.contains("PRUD'")
    # 2635 dossiers
    return jurinet[cond]