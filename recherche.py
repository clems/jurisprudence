#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  4 00:30:37 2017

On a besoin de faire tourner la fonction pdf_to_text avant de faire tourner
ce programme. 

@author: sgmap
"""

import os
import re
from pprint import pprint
import pandas as pd

from os.path import join


###############################
### Étude des fichiers fournis
###############################

path_data_recues = 'D:\data\prudhommes'
#echantillon = pd.read_excel(join(path_data_recues, 'echantillonbaselicenciements.xlsx'))


def _test_jurinet(func, jurinet, nrows=0):
    ''' fait un test sur la base jurinet 
        Si nrows est différent de zéro, on fait tourner sur un sous-echantillon
        tiré aléatoirement de taille nrwos. Ce qui faicilite la lecture en 
        cas de printing
        '''
    assert isinstance(nrows, int)
    if nrows > 0:
        jurinet['TEXTE_ARRET'].sample(nrows).apply(func)
    else:
        jurinet['TEXTE_ARRET'].apply(func)


def _test_pdfs(func):
    result_text = []
    for filename in os.listdir(path_data_recues):
        if filename.endswith('.txt'):
            with open(join(path_data_recues, filename), 'r', encoding='utf8') as f:
                text = f.read()
                result_text.append(func(text))    


def _test(func, on='both', jurinet=None, nrows=0):
    """ Une routine pour tester des fonctions sur les textes passés ou
        bien sur la base jurinet
    """
    assert on in ['both', 'jurinet', 'pdf']

    if on in ['both', 'pdf']:
        result_text = _test_pdfs(func)

    if on in ['both', 'jurinet']:
        assert jurinet is not None
        result_on_jurinet= _test_jurinet(func, jurinet, nrows=nrows)

    if on == 'both':
        return result_text, result_on_jurinet
    if on == 'jurinet':
        return result_on_jurinet
    if on == 'pdf':
        return result_text
 
 
def _recherche(mot, text, option_mot_qui_suivent=0):
    text_lower = text.lower()
    if mot.lower() in text_lower:
        idx = text_lower.index(mot.lower())
        if option_mot_qui_suivent:
            if option_mot_qui_suivent > 0:
                return text[idx: idx + len(mot) + option_mot_qui_suivent]
            else:
                return text[idx - option_mot_qui_suivent : idx + len(mot)]
        else:
            return idx
    else:
        return False


def print_recherche(mot, text, option_mot_qui_suivent=0, verbose=True):
    result = _recherche(mot, text, option_mot_qui_suivent)
    if result and verbose:
        print('* ', result)
    else:
        print('pas trouvé')
    return result


def mots_qui_suivent(mot, text, index=0):
    ''' index est là lorsque le mot apparait plusieurs fois '''
    stop_words = [',', '.', '\n', ':', '\(', '\)', 'à', ';']
    result = _recherche(mot, text, 50)
    if result:
        for words in stop_words:
            result = result.split(words)[0]
    if result:
        print('* ', result)
    else:
        print('pas trouvé')        
    return result


def test_presence(mot, jurinet):
    result = jurinet['TEXTE_ARRET'].str.lower().str.count(mot.lower())
    vc = result[result > 0].value_counts()
    print('''
        Le mot \"{}\" est présent dans {} textes et absent dans {}.
        Lorqu'il est présent, il apparait entre {} et {} fois.
        
        Les principales fréquences sont les suivantes :
{}
    '''.format(mot, sum(result > 0), sum(result == 0),
               vc.index.min(), vc.index.max(),
               vc.head()
               ))

def non_present(mot, jurinet):
    result = jurinet['TEXTE_ARRET'].str.lower().str.count(mot.lower())
    return jurinet['TEXTE_ARRET'][result == 0]


if __name__ == '__main__':
    from load import jurinet_2015_prudhom
    jurinet = jurinet_2015_prudhom()
    tt = jurinet
    
    ## Composition
    
    # Président OK, le genre existe via Mme ou via Prénom
    # Pour les autres, on les a quand la cours de cassation juge
    # pas pour les autres
    
    # on regarde si on a bien un élément pour le président, l'avocat général et
    # le rapporteur
    president = tt['COMPOSITION'].str.lower().str.contains('président')
    president.fillna(False, inplace=True)
    president = president | tt['PRESIDENT'].notnull()
    # => Il en manque 2
    
    #TODO: regarder la recherche de avocat général, conseiller et autre dans le texte
    

    ### Société
    test_presence('société', jurinet)
    test_presence('SARL', jurinet)
    test_presence('société ano', jurinet)
    test = _test_jurinet(lambda x: print_recherche('société ', x, 50),
                         jurinet = jurinet, nrows=12)
    
    test_mots = _test_jurinet(lambda x: mots_qui_suivent('société', x), 
                     jurinet = jurinet, nrows=20)
    test = _test_jurinet(lambda x: x.count('socié'), jurinet = jurinet)
    

    # Appelant
    test_presence('appelant', jurinet)
    test = _test_jurinet(lambda x: print_recherche('appelant', x, 50), 
                     jurinet = jurinet, nrows=30)

    test_presence('le pourvoi formé par', jurinet)
    test = _test_jurinet(lambda x: print_recherche('le pourvoi formé par', x, 50), 
                     jurinet = jurinet, nrows=30)


    # profession
    mot = 'qualité de'
    test_presence(mot, jurinet)
    test_phrase = _test_jurinet(lambda x: print_recherche(mot, x, 50), 
                     jurinet = jurinet, nrows=20)
        
    test_mots = _test_jurinet(lambda x: mots_qui_suivent(mot, x), 
                     jurinet = jurinet, nrows=20)
    
    test_non_present = non_present(mot, jurinet)
#    print(test_non_present.iloc[0])
    mot = 'en tant que'
    
    
    # date, ancienneté
    mot = 'indeterminée à compter de' #contrat
    test_presence(mot, jurinet)
    test_phrase = _test_jurinet(lambda x: print_recherche(mot, x, 50), 
                     jurinet = jurinet, nrows=20)
        
    test_mots = _test_jurinet(lambda x: mots_qui_suivent(mot, x), 
                     jurinet = jurinet, nrows=20)
    
    test_non_present = non_present(mot, jurinet)
#    print(test_non_present.iloc[0])    

    mot = "ans d'ancienneté"
    ## remarque : 
#    M. SZPEKOWSKI a travaillé au sein de l'association ' Ecole Notre Dame de Bétharram' devenue
#    l'association l'OGEC ' le Beau Rameau' du 4 septembre 1989 (ou 1999, aucun contrat de travail
#    n'étant produit aux débats) au 18 juillet 2009, date de son licenciement pour motif économique, en
#    qualité de surveillant.

#    M. David BILY, agent EDF statutaire depuis 2002

    mot = 'durée indéterminée en date du'
    # mot = 'faible ancienneté'
    # mot = 'embauché le'

    test_presence(mot, jurinet)
    test_phrase = _test(lambda x: print_recherche(mot, x, 50), 
                     jurinet = jurinet, nrows=20)
        
    test_mots = _test_jurinet(lambda x: mots_qui_suivent(mot, x), 
                     jurinet = jurinet)
    test_non_present = non_present(mot, jurinet)
#    print(test_non_present.iloc[0])


    # salaire
    mot = 'salaire de'
    # salaire brut mensuel de 
    # salaire brut de 
    # coefficient hiérarchique
    test_presence(mot, jurinet)
    test_phrase = _test(lambda x: print_recherche(mot, x, 50), 
                     jurinet = jurinet, nrows=20)
        
    test_mots = _test_jurinet(lambda x: mots_qui_suivent(mot, x), 
                     jurinet = jurinet)
    test_non_present = non_present(mot, jurinet)
#    print(test_non_present.iloc[0])


    # sujets
    print(voir.iloc[0])
    test = _test(lambda x: print_recherche('handi', x, 14), jurinet = jurinet)
    test = _test(lambda x: x.count('handi'), jurinet = jurinet)


    # montants:
    




    def recherche_sur_les_textes(text, verbose=True):
         # avoir la ville (probablement facile dans jurinet via le XML)
        ville = _recherche("COUR D'APPEL", text, 15)
        if ville:
             ville = ville.replace('DE ','').replace("D'",''.replace("d'",'')).lstrip()
             if ville[:2] == 'DE':
                 ville = ville[2:] 
        if ville:
            ville = ville.replace('DE ','').replace("D'",''.replace("d'",'')).lstrip()
            if ville[:2] == 'DE':
                ville = ville[2:]
            ville = ''.join(re.findall('[A-Z]', ville))
    
        # licenciement économique
        print_recherche('temps partiel', text, 15)
        print_recherche('économi', text, 50)
        print_recherche('faute lourde', text, 50)
        print_recherche('santé', text, 15)
        print_recherche('handi', text, 15)



#
#
#####
### travail sur la date d'embauche
#    test = _test(lambda x: print_recherche('ancienneté', x, 14), on = 'pdf')
#    test = _test(lambda x: x.count('ancienneté'), on = 'pdf')
#


#plus_de_ans
#sachant que le salarié a plus de deux ans ancienneté, test sur durée.
#parfois on a la date d'embauche.
#
#et que l'enterprise à plus de 11 salarié.
#Nom de l'entreprise et SIRET
#
#
#Salaire du salarié avant le licenciement.
#
#Le salaire est le plus dur. Souvent le salaire brut d'embauche
#mais un salaire brut évalué regardé réumnération
#
#indemnité peut être noté en mois ou en euros
#
#proffesion :
#    les fonctions de
#
#temps partiel
#
#type licenciement
#    'économique ou non', 'difficulté'
#
#la colonne Q: chance de retrouver un emploi. Pas de manière automatique.
#
#Commune localisation de l'entreprise.
#Lieu de travail.
#
#
#Avoir des infos sur le prudhom d'origine
#
#AA protection syndicale
#
#Le plus Jury montant sans cause réélle et sérieuse et le plaignant.
#
#
#
