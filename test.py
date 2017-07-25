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
data_file = os.path.join(project_path, 'data', 'jurinet.csv')
stanford_postagger_path = project_path  + "\\stanford-postagger-full-2017-06-09"

java_path = "C:/Program Files (x86)/Java/jre1.8.0_131/bin/java.exe"
nltk.internals.config_java(java_path, options = "-mx1000m", verbose =False)
os.environ['JAVAHOME'] = java_path

###################################
# load data and preprocess
###################################
jurinet = pd.read_csv(data_file, encoding='utf8')


jurinet_dict = read_raw_csv(data_file)
jurinet_df = preproccess_data(jurinet_dict)

# filter decisions 
base = filter_juridiction(jurinet_df, "CA")
base = filter_texte_arret(base, "prud'h")
base = filter_texte_arret(base, "licenciement")
 
base = ie_preprocess_col(base)

export_decision(appel_prudhomme, 2)


