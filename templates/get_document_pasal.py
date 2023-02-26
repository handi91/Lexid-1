from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd
import re

endpoint_url = 'http://localhost:9999/blazegraph/sparql'

sparql = SPARQLWrapper(endpoint_url)
sparql.setReturnFormat(JSON)

# template = '''
# PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> 
# PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
# PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
# PREFIX dbo: <http://dbpedia.org/ontology/> 
# PREFIX dct: <http://purl.org/dc/terms/> 
# PREFIX owl: <http://www.w3.org/2002/07/owl#> 
# PREFIX wd: <https://www.wikidata.org/wiki/> 
# PREFIX lexid-s: <https://w3id.org/lex-id/schema/> 
# PREFIX lexid: <https://w3id.org/lex-id/data/> 

# SELECT distinct ?larticle
# WHERE {
#     ?LegalDocument a lexid-s:LegalDocument ;
#     lexid-s:hasContent ?topLevelContent .
#     ?topLevelContent lexid-s:hasPart* ?article .
#     ?article a lexid-s:Article ;
#     rdfs:label ?larticle .
# }
# ORDER BY ?larticle
# '''
# sparql.setQuery(template)
# ret = sparql.queryAndConvert()
# pasal_pasal = []
# print(len(ret["results"]["bindings"]))
# # print(ret["results"]["bindings"][0])
# for i in ret["results"]["bindings"]:
#     # print(i)
#     pasal = i['larticle']['value']
#     if re.match(r'^Pasal (\d+|[A-Z]+)$', pasal):
#         pasal_pasal.append(pasal)
#         continue
#     if re.match(r'^Pasal \d+[A-Z]$', pasal):
#         pasal_pasal.append(pasal)
# pasal_pasal.sort()
# print(len(pasal_pasal))
# data = pd.DataFrame({
#     "pasal": pasal_pasal
# })
# print(re.match(r'Pasal \d+[A-Z]', 'Pasal 18A'))
# data.to_csv('valid-pasal-label.csv', index=False)

# template2 = '''
# PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> 
# PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
# PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
# PREFIX dbo: <http://dbpedia.org/ontology/> 
# PREFIX dct: <http://purl.org/dc/terms/> 
# PREFIX owl: <http://www.w3.org/2002/07/owl#> 
# PREFIX wd: <https://www.wikidata.org/wiki/> 
# PREFIX lexid-s: <https://w3id.org/lex-id/schema/> 
# PREFIX lexid: <https://w3id.org/lex-id/data/> 

# SELECT distinct (concat(?larticle, " ", ?lsection) as ?answer) ?larticle ?lsection
# WHERE {
#     ?LegalDocument a lexid-s:LegalDocument ;
#     lexid-s:hasContent ?topLevelContent .
#     ?topLevelContent lexid-s:hasPart* ?article .
#     ?article a lexid-s:Article ;
#     rdfs:label ?larticle .
#     ?article lexid-s:hasPart ?section .
#     ?section a lexid-s:Section ;
#     rdfs:label ?lsection .
# }
# ORDER BY ?answer
# '''
# sparql.setQuery(template2)
# ret2 = sparql.queryAndConvert()
# pasal_with_ayat = []
# pasal2 = []
# ayat2 = []
# for j in ret2['results']['bindings']:
#     # print(j)
#     pasal_and_ayat = j['answer']['value']
#     pasal = j['larticle']['value']
#     ayat = j['lsection']['value']
#     if re.match(r'^Pasal (\d+|[A-Z]+)$', pasal) or re.match(r'^Pasal \d+[A-Z]$', pasal):
#         if re.match(r'^ayat \d+$', ayat):
#             pasal_with_ayat.append(pasal_and_ayat)
#             pasal2.append(pasal)
#             ayat2.append(ayat)
# print(len(pasal_with_ayat))
# data2 = pd.DataFrame({
#     "pasal_ayat": pasal_with_ayat,
#     "pasal": pasal2,
#     "ayat": ayat2
# })

# data2.to_csv('valid-pasal-with-ayat-label.csv', index=False)

data3 = pd.read_csv('valid-pasal-label.csv')
data3['pasal_ayat'] = data3['pasal']
data3['ayat'] = ['' for i in range(data3.shape[0])]

data4 = pd.read_csv('valid-pasal-with-ayat-label.csv')
data_concat = pd.concat([data3, data4])
data_concat = data_concat[['pasal_ayat', 'pasal', 'ayat']]
data_concat.to_csv('valid-pasal-optional-ayat-label.csv', index=False)
