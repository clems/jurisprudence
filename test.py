# -*- coding: utf-8 -*-
"""
Created on Mon Jul 24 18:51:25 2017

@author: clementschaff
"""

import os
import pandas as pd

from prudhomme.load_data import read_raw_csv, preproccess_data, filter_ccass, filter_prudhomme, filter_cdappel


project_path = os.getcwd()
data_file = os.path.join(project_path, 'data', 'jurinet.csv')

jurinet_dict = read_raw_csv(data_file, nrows = 1000)

# convert the dict into a dataframe
jurinet_df = preproccess_data(jurinet_dict)


prudh = filter_prudhomme(jurinet_df)
ccass = filter_ccass(jurinet_df)
appel = filter_cdappel(jurinet_df)



