# -*- coding: utf-8 -*-
"""
Created on Fri Jul 21 12:17:46 2017

@author: cleme
"""

#################################################################
# process jurisprudence
#################################################################

import pickle, bs4, nltk, os, re
from nltk.tag.stanford import StanfordPOSTagger

java_path = "C:/Program Files (x86)/Java/jre1.8.0_131/bin/java.exe"
nltk.internals.config_java(java_path, options = "-mx1000m", verbose =False)
os.environ['JAVAHOME'] = java_path

root_path = "C:\\Users\\cleme\\Documents\\jurisprudence"
stanford_postagger_path = root_path + "\\stanford-postagger-full-2017-06-09"

def pos_tag(to_tag, model_path = stanford_postagger_path  +"\\models\\french.tagger",
            jar_path = stanford_postagger_path +"\\stanford-postagger.jar"):
    '''tag the tokens with part of speech; to_tag is the tags; model_path is the 
    file path to the stanford POS tagger model; and jar_path to the Stanford POS 
    tagger jar file'''
    pos_tagger = StanfordPOSTagger(model_path,jar_path,encoding='utf8') #create an object of class POSTagger that is encoded in UTF-8
    tags = pos_tagger.tag(to_tag) #run the tagging algorithm on the tokenized raw text
    return tags

def rep_thousand_sep(match):
    return match.group(0)[-3:]

def rmv_thousand_sep(doc):
    return re.sub(r'\. [0-9]{3}(?![0-9])', rep_thousand_sep, doc)


def ie_preprocessing(doc):
    ''' tokenize and tag sentences in document'''
    doc_clean = rmv_thousand_sep(doc)
    sentences = nltk.sent_tokenize(doc_clean)
    sentences = [nltk.word_tokenize(sent) for sent in sentences]
    sentences = [pos_tag(sent) for sent in sentences]
    return sentences



with open('data.pkl', 'rb') as f:
    juris = pickle.load(f)
    
soup_juris = [bs4.BeautifulSoup(d, "html5lib") for d in juris]

# work on the first example
doc = soup_juris[0].text
processed_doc = ie_preprocessing(doc)
for sent in processed_doc:
    print(sent)
    print("\n")


entities = nltk.chunk.ne_chunk(tags)

from nltk.corpus import ieer
docs = ieer.parsed_docs(d)
tree = docs[1].text
print(tree)

import re




from nltk.corpus import ieer
docs = ieer.parsed_docs(d)
print(docs[1].text)

#####################################################################
### tests
#####################################################################


import unittest

class TestJuris(unittest.TestCase):
    
    def test_rep_thousand_sep(self):
        self.assertEqual(rep_thousand_sep(".430"), "430"))
        
        