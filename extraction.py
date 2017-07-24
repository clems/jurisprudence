# -*- coding: utf-8 -*-
"""
Created on Mon Jun 26 12:03:53 2017

@author: AE
"""

import pandas as pd
path_data_recues = 'D:\data\prudhommes'

def _extract_brut_from_row(mot, row):
    temp = row['text'][row['idx'] + len(mot) :row['idx'] + 50]
    temp = temp.lstrip()
    if temp[:2] == 'ES':
        temp = temp[2:]
    if temp[:1] == 'E':
        temp = temp[1:]
    temp = temp.lstrip()
    if temp[:1] == ':':
        temp = temp[1:]        
    temp = temp.lstrip()
    return temp

def extract_apres_mot(mot, serie):
    ''' index est là lorsque le mot apparait plusieurs fois '''
    serie_lower = serie.str.lower()

    result_index = serie_lower.str.find(mot.lower())
    tab = pd.DataFrame({'text': serie, 'idx':result_index})
        
    extract_brut = tab.apply(lambda x: _extract_brut_from_row(mot, x), axis=1)

    # pour appelant
    
    stop_words = [',', '.', '\n', ':', '\(', '\)', 'à', ';', 'comme']
    extract = extract_brut
    for words in stop_words:
        extract = extract.str.split(words).str[0]

    return extract


select_from_jurinet = [
            'NUM_DECISION', 'NUMPOURVOI', 'ID_DOCUMENT',
            'JURIDICTION', 'ID_CHAMBRE', 'CHAMBRE', 'CAT_PUB', 'CHAMBRE',
            'ID_SOLUTION', 'SOLUTION', 'DT_DECISION',

            'COMPOSITION',
            'PRESIDENT', 'CONSRAP', 'AVOCAT', 'AVOG',
            ]

def csv_from_jurinet(jurinet):
    output = jurinet.copy()
    del output['TEXTE_ARRET']

    output.drop(['DT_MODIF', 'DT_CREATION',
                 'CLEF_ARRET',
                 ], axis=1, inplace=True)

    return output.loc[:, select_from_jurinet]


def exploitation(jurinet):
    output = jurinet.copy()
    text = output['TEXTE_ARRET']
    del output['TEXTE_ARRET']

    output = output.loc[:, select_from_jurinet]

    words = ['société', 'appelant', 'qualité de', 'salaire de']
    for word in words:
        output[word] = extract_apres_mot(word, text)
        
    return output


if __name__ == '__main__':
    from load import jurinet_2015_prudhom
#    jurinet = jurinet_2015_prudhom()

    tt = exploitation(jurinet)
#    tt = csv_from_jurinet(jurinet)
#    tt.to_csv(join(path_data_recues, 'generees.csv'), index=False)