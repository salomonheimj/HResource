import requests as requests
import json as json
from requests.auth import HTTPBasicAuth

def cb_get_results(sintomas):
    url = 'https://gateway.watsonplatform.net/discovery/api/v1/environments/980ee167-f667-405b-a661-acf3a7d01dc4/collections/949ce21d-4000-4ac4-88d6-38484cccddde/query?version=2017-10-16&count=&offset=&aggregation=&filter=&passages=true&deduplicate=false&highlight=true&return=&natural_language_query='
    for i in range(len(sintomas)):
        url+= sintomas[i]+'%20'
    r=requests.get(url, auth=('788db5c8-5d33-4998-b0f8-af0ed1d02e1e','4PlZbmbrZ3PL'))
    print(str(r.status_code))
    #print(r.json())
    jso = (r.json())
    cantRes = jso['matching_results']
    resultados = jso['results']
    results =[]
    #results.append("Cantidad de resultados: " + str(cantRes))
    for i in range (len(resultados)):
        res = resultados[i]
        score = res['score']
        metaData = res['extracted_metadata']
        fileName = metaData['filename']
        fileName = fileName.replace('_', ' ')
        enr = res['enriched_text']
        sent = enr['sentiment']
        doc = sent['document']
        sentScore = doc['score']
        sentLabel = doc['label']
        objResultado = Resultado(score,fileName, sentScore, sentLabel,cantRes)
        results.append(objResultado)
    return results

class Resultado(object):
    mainScore=0
    textTittle=""
    sentScore =0
    sentLabel=""
    cantResults = 0
    def __init__(self, mainScore, textTittle, sentScore, sentLabel,cantResults):
        self.mainScore=mainScore
        self.textTittle=textTittle
        self.sentScore=sentScore
        self.sentLabel=sentLabel
        self.cantResults=cantResults
def cb_get_sintomas():
    sintomas = []
    return sintomas
