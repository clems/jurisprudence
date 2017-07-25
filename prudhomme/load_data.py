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
    print("the dict has {} entries".format(len(jurinet_dict)))
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




def filter_prudhomme(jurinet_df):
    ''' filter decisions with the word "prud'hom" in text'''
    initial_len = len(jurinet_df)
    text = jurinet_df.TEXTE_ARRET
    cond = (text.str.lower()).str.contains("prud'hom")
    out = jurinet_df[cond]
    final_len = len(out)
    print("there was {} entries in the table. There is now {} entries".format(initial_len, final_len ))
    return out


def filter_ccass(jurinet_df):
    ''' filter decision of the Cour de cassation'''
    initial_len = len(jurinet_df)
    juri = jurinet_df.JURIDICTION
    cond = (juri == 'cour de cassation')
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
