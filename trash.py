# -*- coding: utf-8 -*-
"""
Created on Tue Jul 25 22:04:00 2017

@author: cleme
"""

part_separator = ['ENTRE :', 'ET :', "L'affaire a été appelée à l'audience publique", 'MOTIFS DE LA DÉCISION :', 'PAR CES MOTIFS', ]

# cut the decision in its main parts.
import re

def split_text_arret(text):
    remain = text
    [HEAD, remain] = re.split('ENTRE :', remain, maxsplit = 1)
    [PARTIE1, remain] = re.split('ET :\n', remain, maxsplit = 1)
    [PARTIE2, remain] = re.split("L'affaire a été appelée à l'audience publique", remain, maxsplit = 1)
    [ESPECE, remain] = re.split('MOTIFS DE LA DÉCISION :\n', remain, maxsplit = 1)
    [MOTIFS, DECISION] = re.split('PAR CES MOTIFS\n', remain, maxsplit = 1)

    