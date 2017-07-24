#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 20 10:58:30 2017

@author: sgmap, clementschaff
"""

import os
from os.path import join
import PyPDF2

def pdf_to_text(path_data_recues):
    for filename in os.listdir(path_data_recues):
        if filename.endswith('.pdf'):
            pdfFileObj = open(join(path_data_recues, filename), 'rb')
            pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
            all_text = ''
            for num_page in range(pdfReader.numPages):
                pageObj = pdfReader.getPage(num_page)
                text = pageObj.extractText()
                all_text += text + '\n saut de ligne \n'
            with open(join(path_data_recues, filename[:-4] + '.txt'), 'w',
                      encoding='utf8') as f:
                f.write(all_text)
            pdfFileObj.close()



def jurinet_2015_prudhom():
    '''
    load initial jurinet dump
    '''
    from jurinet.appariement.jurinet_data import load_jurinet
    jurinet = load_jurinet()
    # on ne retrouve pas le fichiers de l'échantillon (probablement parce qu'ils
    # sont trop vieux, et qu'on a jurinet 2015 seulement)

    # on isole tout de même les textes de jurisprudence
    XML = jurinet.TEXTE_ARRET
    cond = XML.str.contains("prud'hom") | XML.str.contains("Prud'hom") | XML.str.contains("PRUD'")
    # 2635 dossiers
    return jurinet[cond]

