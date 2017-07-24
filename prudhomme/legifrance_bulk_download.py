# -*- coding: utf-8 -*-
"""
Created on Fri Jul 21 12:16:42 2017

@author: Clement Schaff
"""

#################################################################
# load jurisprudence from legifrance
#################################################################

import requests, bs4, pickle

def legifrance_request(legifranceUrl = 'https://www.legifrance.gouv.fr/rechExpJuriJudi.do'):
    ''' Make a search on legifrance web site '''
    _legifrance_request_params = {"champNumeroAffaire":None, 
                          "champDateDecision1J":None, 
                          "champDateDecision1M":None,   
                          "champDateDecision1A":None,
                          "champNatureDecision":None,
                          "champNumeroBulletin":None,   
                          "champAnnee":None,
                          "champFormation":None,
                          "champDecisionAttaquee":None,
                          "champLieuDecisionAttaquee":None,
                          "champDecisionAttaqueeDateJ":None,
                          "champDecisionAttaqueeDateM":None,
                          "champDecisionAttaqueeDateA":None,
                          "checkboxRechercheDecisionCourDAppel":"on",
                          "champSiegeCour":None,
                          "champJuridiction":None,
                          "champLieu":None,
                          "rechDepth":"1",
                          "rechSaufDepth":"0",
                          "rechFT1":"licenciement",
                          "rechFT1Cible":"TIntegral",
                          "rechFTOp1":"AND",
                          "rechFT2":None,
                          "rechFT2Cible":"TIntegral",
                          "rechFTOp2":"AND",
                          "rechFT3":None,
                          "rechFT3Cible":"TIntegral",
                          "rechFTOp3":"AND",
                          "rechFT4":None,
                          "rechFT4Cible":"TIntegral",
                          "rechFTSauf":None,
                          "rechFTSaufCible":"TIntegral",
                          "idNomenclature":None,
                          "bouton":"Rechercher"}
    
    return requests.get(legifranceUrl, params = _legifrance_request_params ) #res1

def append_jurisprudence_url(request, decision_url):
    ''' Get all decision url on a single page of results from a legifrance 
    search'''
    jurisResult = bs4.BeautifulSoup(request.text)
    for result in jurisResult.select("li.resultat1"):
        decision_url.append([link.get('href') for link in result.select('a')])
    for result in jurisResult.select("li.resultat2"):
        decision_url.append([link.get('href') for link in result.select('a')])

def get_decision_url(n_pages = 601, 
                     legifranceUrl = 'https://www.legifrance.gouv.fr/rechExpJuriJudi.do'):
    ''' Get all decision url on a legifrance search. A call to legifrance_request()
    should be done first'''
    decision_url = []
    for i in range(1,n_pages):
        res = requests.get(legifranceUrl, params = {"reprise":"true","page":str(i)})
        append_jurisprudence_url(res, decision_url)
    return decision_url

def get_decision_html(decision_url):
    ''' create a list of decision html content from a list of decision URL'''
    decisions = []
    for decisionLink in decision_url:
        res = requests.get('https://www.legifrance.gouv.fr' + decisionLink[0])
        decision = bs4.BeautifulSoup(res.text)
        decisions.append(str(decision.select("div.data")[0]))
    return decisions

def save_file(file = 'data.pkl', decisions):
    with open('data.pkl', 'wb') as f:
        pickle.dump(decisions, f)

if __name__ == __main__:
    ''' function should be called in this order'''
    legifrance_request()
    decision_url = get_decision_url()
    decisions = get_decision_html(decision_url)
    