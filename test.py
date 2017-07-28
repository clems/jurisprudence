# -*- coding: utf-8 -*-
"""
Created on Mon Jul 24 18:51:25 2017

@author: clementschaff
"""

import os
import nltk
import pandas as pd

from prudhomme.load_data import filter_texte_arret
from prudhomme.process_decisions import tokenize_sent, preprocess_texte_arret, convert_nltk_text
from prudhomme.utils import export_decision

###################################
# define various paths
###################################

project_path = os.getcwd()
data_path = os.path.join(project_path, 'data')
data_file = os.path.join(data_path, 'jurinet.csv')
stanford_postagger_path = project_path  + "\\stanford-postagger-full-2017-06-09"

java_path = "C:\Program Files (x86)\Java/jre1.8.0_131/bin/java.exe"
nltk.internals.config_java(java_path, options = "-mx1000m", verbose =False)
os.environ['JAVAHOME'] = java_path

####################################
## load jurinet_data and preprocess
####################################
#from prudhomme.load_data import read_raw_csv, preproccess_data, filter_juridiction, filter_texte_arret
# from prudhomme.utils import export_decision
#
#jurinet_dict = read_raw_csv(data_file)
#jurinet_df = preproccess_data(jurinet_dict)
#
## filter decisions 
#base = filter_juridiction(jurinet_df, "CA")
#base = filter_texte_arret(base, "prud'h")
#base = filter_texte_arret(base, "licenciement")
#
#base.JURIDICTION.value_counts()
# 
#base = ie_preprocess_col(base)
#
#base.TEXT_TOKEN[0][2]
#
#for i in range(10):
#    export_decision(base, i)
#
########################################
# work on legifrance database
########################################

import pickle, bs4, re

with open(os.path.join(data_path, 'data.pkl'), 'rb') as f:
    legifrance = pickle.load(f)

TEXTE_ARRET = pd.Series([bs4.BeautifulSoup(d, "html5lib").get_text() for d in legifrance])
ID_DECISION = range(len(TEXTE_ARRET))

base = pd.DataFrame({"TEXTE_ARRET":TEXTE_ARRET, "ID_DECISION": ID_DECISION})
base_2 = filter_texte_arret(base, "prud'h")

base_scrs = filter_texte_arret(base_2, u"sans cause réelle et sérieuse")
base_scrs['TEXTE_ARRET'] = preprocess_texte_arret(base_scrs.TEXTE_ARRET)
base_scrs = base_scrs.assign(SENTENCES = tokenize_sent(base_scrs.TEXTE_ARRET))
base_scrs = base_scrs.assign(TEXT = convert_nltk_text(base_scrs.TEXTE_ARRET))

export_decision(base_scrs, 0)
doc = base_scrs.TEXTE_ARRET[0]
text = base_scrs.TEXT[0]
words = [w.lower() for w in text]


patterns = [(r'[0-9]+\.?[0-9]+(?= €)', 'AMT'), (r'.*', 'NN')]
amounts_tagger = nltk.RegexpTagger(patterns)
amounts_tagger.tag(['la','somme','de','1554.62 € uros'])

for sentence in base_scrs.SENTENCES[0]:
    for sent_part in sentence.split('\n'):
#        re.search("sans cause réelle et sérieuse", sent_part):
        montants = re.findall(u'[0-9]+\.?[0-9]+(?= €)', sent_part)
        if len(montants)>0:
            words = nltk.word_tokenize(sent_part)
            print(montants)
            print('\n\n')
            print(sent_part)
            input()
        
def indeminite_features(word):
    features = {}
    features['is_ammount'] = None
    
    
from nltk.corpus import brown
brown_sents = brown.sents(categories = "news")
print(brown_sents[3])
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
