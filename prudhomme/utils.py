# -*- coding: utf-8 -*-
"""
Created on Tue Jul 25 20:26:56 2017

@author: cleme
"""


## there is still a problem with newlines
def export_decision(df, idx):
    with open("data/export/decision{}.txt".format(idx), "wb") as f:
        f.write(df.TEXTE_ARRET[idx].encode('utf-8'))
#        f.write(df.TEXTE_ARRET[idx])
        f.close()

