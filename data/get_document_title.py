from SPARQLWrapper import SPARQLWrapper, JSON

endpoint_url = 'http://localhost:9999/blazegraph/sparql'

sparql = SPARQLWrapper(endpoint_url)
sparql.setReturnFormat(JSON)

sparql.setQuery('''
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> 
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
PREFIX dbo: <http://dbpedia.org/ontology/> 
PREFIX dct: <http://purl.org/dc/terms/> 
PREFIX owl: <http://www.w3.org/2002/07/owl#> 
PREFIX wd: <https://www.wikidata.org/wiki/> 
PREFIX lexid-s: <https://w3id.org/lex-id/schema/> 
PREFIX lexid: <https://w3id.org/lex-id/data/> 

SELECT distinct (str(?lDocument) as ?ans)
WHERE {
  ?legalDocument a lexid-s:LegalDocument ;
                   rdfs:label ?lDocument .
}
''')
answers = []
try:
    ret = sparql.queryAndConvert()
    # print(ret)
    with open("unique-document-title.txt", 'w') as f:
      for r in ret["results"]["bindings"]:
          answers.append(r['ans']['value'])
          f.write(r['ans']['value']+'\n')

except Exception as e:
    print(e)
print(len(answers))