#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 20 10:58:30 2017

@author: sgmap, clementschaff
"""

from xml.etree import ElementTree as ET
import pandas as pd

def read_raw_csv(file_path, nrows=None):
    ''' read the raw jurinet.csv file and return the parsed the content of the 
    XML column in a dict. main key is "ID_DOCUMENT"
    '''
    jurinet = pd.read_csv(file_path, encoding='utf8', nrows = nrows)
    jurinet_dict = {}
    for idx, row in jurinet.iterrows():
        row_dict = {}
        # parse the XML attribute of the row        
        try:
            root = ET.fromstring(row.XML[:])
        except:
            continue
        # store it in a dict
        for child in root:
            row_dict[child.tag] = child.text
        # store this dict in the main dict
        jurinet_dict[row_dict['ID_DOCUMENT']] = row_dict.copy()
    print("csv file had {} entries, the dict has {} entries".format(len(jurinet), len(jurinet_dict)))
    return jurinet_dict

def preproccess_data(jurinet_dict):
    jurinet_df = pd.DataFrame.from_dict(jurinet_dict, orient= 'index')
    initial_len = len(jurinet_df)
    # drop NA
    jurinet_df.dropna(axis = 0, how= "any", subset = ['JURIDICTION'], inplace = True)
    # lower JURIDICTION
    jurinet_df.JURIDICTION = jurinet_df.JURIDICTION.str.lower()

    final_len = len(jurinet_df)    
    print("there was {} entries in the table. There is now {} entries".format(initial_len, final_len ))
    return jurinet_df

def filter_texte_arret(dataframe, word):
    ''' filter decisions with the word "word" in text'''
    initial_len = len(dataframe)
    text = dataframe.TEXTE_ARRET
    cond = (text.str.lower()).str.contains(word.lower())
    out = dataframe[cond]
    final_len = len(out)
    print("there was {} entries in the table. There is now {} entries".format(initial_len, final_len ))
    return out


def filter_juridiction(jurinet_df, juridiction):
    ''' filter decision of a specific juridication
    juridiction may be "CCASS" for Cour de cassation, "CA" for Cour d'appel, None'''
    if juridiction not in ("CCASS", "CA"):
        raise "juridiction should be CCASS or CA"
    initial_len = len(jurinet_df)
    juri = jurinet_df.JURIDICTION
    if juridiction == "CCASS":
        cond = (juri == 'cour de cassation')
    elif juridiction == "CA":
        cond = juri.str.contains("cour d'appel")
    out = jurinet_df[cond]
    final_len = len(out)
    print("there was {} entries in the table. There is now {} entries".format(initial_len, final_len ))
    return out

def filter_cdappel(jurinet_df):
    ''' filter decision of the Cour de cassation'''
    initial_len = len(jurinet_df)
    juri = jurinet_df.JURIDICTION
    cond = juri.str.contains("cour d'appel")
    out = jurinet_df[cond]
    final_len = len(out)
    print("there was {} entries in the table. There is now {} entries".format(initial_len, final_len ))
    return out

