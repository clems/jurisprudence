# -*- coding: utf-8 -*-
"""
Created on Fri Jul 21 12:17:46 2017

@author: clementschaff
"""

#################################################################
# process jurisprudence
#################################################################

import nltk, re
from nltk.tag.stanford import StanfordPOSTagger

def pos_tag(to_tag, stanford_postagger_path):
    '''tag the tokens with part of speech; to_tag is the tags; model_path is the 
    file path to the stanford POS tagger model; and jar_path to the Stanford POS 
    tagger jar file'''
    pos_tagger = StanfordPOSTagger(stanford_postagger_path +"\\models\\french.tagger",
                                   stanford_postagger_path +"\\stanford-postagger.jar",
                                   encoding='utf8') #create an object of class POSTagger that is encoded in UTF-8
    tags = pos_tagger.tag(to_tag) #run the tagging algorithm on the tokenized raw text
    return tags

def clean_text(doc):
    # remove decimal thousands separator '. ' from text
    doc = re.sub(r'\. [0-9]{3}(?![0-9])',lambda m: m.group(0)[-3:], doc)
    # replace decimal separator ', ' by '.'
    doc = re.sub(r'[0-9]\, [0-9]{2}(?![0-9])',lambda m: m.group(0)[0] + '.' + m.group(0)[-2:], doc)
    # clean law references such as 'L. 202' => 'L202' to make it easier to find sentences
    doc = re.sub(r'([ \(])L. [0-9]',lambda m: m.group(0)[0] + 'L' + m.group(0)[-1], doc)
    return doc


def preprocess_texte_arret(TEXTE_ARRET):
    ''' tokenize and tag sentences in document'''
    TEXTE_ARRET_CLEAN = TEXTE_ARRET.apply(clean_text)
    return TEXTE_ARRET_CLEAN

# sentences = [pos_tag(sent, stanford_postagger_path) for sent in sentences]

def tokenize_sent(TEXTE_ARRET):
    ''' tokenize TEXTE_ARRET into sentences '''
    extra_abreviations = ['l'] # add that to deal with "L. " (law references) 
    french_tok = nltk.data.load('tokenizers/punkt/french.pickle')
    french_tok._params.abbrev_types.update(extra_abreviations)
    lambda_tok = lambda doc: french_tok.tokenize(doc)
    return TEXTE_ARRET.apply(lambda_tok)

def tokenize_words(SENTENCES):
    ''' tokenize SENTENCES into words '''
    lambda_word = lambda sentences: [nltk.word_tokenize(sent) for sent in sentences]
    return SENTENCES.apply(lambda_word)

def convert_nltk_text(TEXTE_ARRET):
    ''' tokenize TEXTE_ARRET into nltk.Text '''
    lambda_word = lambda texte: nltk.Text(nltk.word_tokenize(texte))
    return TEXTE_ARRET.apply(lambda_word)

#entities = nltk.chunk.ne_chunk(tags)
#
#from nltk.corpus import ieer
#docs = ieer.parsed_docs(d)
#tree = docs[1].text
#print(tree)
#
#import re
#
#
#
#
#from nltk.corpus import ieer
#docs = ieer.parsed_docs(d)
#print(docs[1].text)
#
