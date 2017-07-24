# -*- coding: utf-8 -*-
"""
Created on Fri Jul 21 12:16:42 2017

@author: Clement Schaff
"""

#################################################################
# load jurisprudence from legifrance
#################################################################

import requests, bs4

legifranceRequest1 = {"champNumeroAffaire":None, 
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



legifranceUrl = 'https://www.legifrance.gouv.fr/rechExpJuriJudi.do'
res1 = requests.get(legifranceUrl, params = legifranceRequest1)

def append_jurisprudence_url(request, decisionLinks):
    jurisResult = bs4.BeautifulSoup(request.text)
    for result in jurisResult.select("li.resultat1"):
        decisionLinks.append([link.get('href') for link in result.select('a')])
    for result in jurisResult.select("li.resultat2"):
        decisionLinks.append([link.get('href') for link in result.select('a')])

decisionLinks = []
for i in range(1,601):
    res = requests.get(legifranceUrl, params = {"reprise":"true","page":str(i)})
    append_jurisprudence_url(res, decisionLinks)

print(len(decisionLinks))

decisionList = []
for decisionLink in decisionLinks:
    res = requests.get('https://www.legifrance.gouv.fr' + decisionLink[0])
    decision = bs4.BeautifulSoup(res.text)
    decisionList.append(str(decision.select("div.data")[0]))
    
len(decisionList)

import pickle
with open('data.pkl', 'wb') as f:
    pickle.dump(decisionList, f)

