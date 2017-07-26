# -*- coding: utf-8 -*-
"""
Created on Mon Jul 24 18:51:25 2017

@author: clementschaff
"""

import os
import nltk
import pandas as pd

from prudhomme.load_data import read_raw_csv, preproccess_data, filter_juridiction, filter_texte_arret
from prudhomme.process_decisions import ie_preprocess_col
from prudhomme.utils import export_decision
###################################
# define various paths
###################################

project_path = os.getcwd()
data_path = os.path.join(project_path, 'data')
data_file = os.path.join(data_path, 'jurinet.csv')
stanford_postagger_path = project_path  + "\\stanford-postagger-full-2017-06-09"

java_path = "C:/Program Files (x86)/Java/jre1.8.0_131/bin/java.exe"
nltk.internals.config_java(java_path, options = "-mx1000m", verbose =False)
os.environ['JAVAHOME'] = java_path

###################################
# load jurinet_data and preprocess
###################################

jurinet_dict = read_raw_csv(data_file)
jurinet_df = preproccess_data(jurinet_dict)

# filter decisions 
base = filter_juridiction(jurinet_df, "CA")
base = filter_texte_arret(base, "prud'h")
base = filter_texte_arret(base, "licenciement")

base.JURIDICTION.value_counts()
 
base = ie_preprocess_col(base)

base.TEXT_TOKEN[0][2]

for i in range(10):
    export_decision(base, i)

########################################
# work on legifrance database
########################################

import pickle, bs4

with open(os.path.join(data_path, 'data.pkl'), 'rb') as f:
    legifrance = pickle.load(f)

TEXTE_ARRET = pd.Series([bs4.BeautifulSoup(d, "html5lib").text for d in legifrance])
ID_DECISION = range(len(TEXTE_ARRET))
base = pd.DataFrame({"ID_DECISION":ID_DECISION,"TEXTE_ARRET":TEXTE_ARRET})
base = filter_texte_arret(base, "prud'h")
base = filter_texte_arret(base, "sans cause réelle et sérieuse")

base_scrs = base

#
## work on the first example
#doc = soup_juris[0].text
#processed_doc = ie_preprocessing(doc)
#for sent in processed_doc:
#    print(sent)
#    print("\n")
#

###################################
# load jurinet_data and preprocess
###################################

