import pandas as pd 

# data = pd.read_csv('question-pattern.csv')

# data = data.sort_values(by='q_pattern')
# data.to_csv('question-pattern.csv', index=False)

PREFIX = '''
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> 
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
PREFIX dbo: <http://dbpedia.org/ontology/> 
PREFIX dct: <http://purl.org/dc/terms/> 
PREFIX owl: <http://www.w3.org/2002/07/owl#> 
PREFIX wd: <https://www.wikidata.org/wiki/> 
PREFIX lexid-s: <https://w3id.org/lex-id/schema/> 
PREFIX lexid: <https://w3id.org/lex-id/data/> 
'''

Q_1_1 = '''
SELECT distinct (coalesce(?label, ?ans) as ?answer)
WHERE {
    ?LegalDocument a lexid-s:LegalDocument ;
        lexid-s:hasEnactionOfficial ?ans ;
        rdfs:label "legal_title"^^xsd:string .
    OPTIONAL { ?ans rdfs:label ?label .}
}
'''
Q_1_2 = '''
SELECT distinct ?answer
WHERE {
    ?LegalDocument a lexid-s:LegalDocument ;
        lexid-s:hasPromulgationDate ?answer ;
        rdfs:label "legal_title"^^xsd:string .
}
'''
Q_1_3 = '''
SELECT distinct ?answer
WHERE {
    ?LegalDocument a lexid-s:LegalDocument ;
        lexid-s:hasEnactionDate ?answer ;
        rdfs:label "legal_title"^^xsd:string .
}
'''
Q_1_4 = '''
SELECT distinct ?answer
WHERE {
    ?LegalDocument a lexid-s:LegalDocument ;
        lexid-s:considers ?answer ;
        rdfs:label "legal_title"^^xsd:string .
}
'''
Q_2_1 = '''
SELECT distinct (coalesce(?label , ?ans) as ?answer)
WHERE {
    ?LegalDocument a lexid-s:LegalDocument ;
    lexid-s:hasLegalBasis ?ans ;
    rdfs:label "legal_title"^^xsd:string .
    ?ans a lexid-s:LegalDocument .
    OPTIONAL {
    ?ans rdfs:label ?label .
    }
}
'''
Q_2_2 = '''
SELECT distinct (coalesce(?label , ?ans) as ?answer)
WHERE {
    ?LegalDocument a lexid-s:LegalDocument ;
    lexid-s:hasLegalBasis
    | lexid-s:implements
    | lexid-s:amends
    | lexid-s:repeals ?ans ;
    rdfs:label "legal_title"^^xsd:string .
    ?ans a lexid-s:LegalDocument .
    OPTIONAL {
    ?ans rdfs:label ?label .
    }
}
'''
Q_2_3 = '''
SELECT distinct (coalesce(?label , ?ans) as ?answer)
WHERE {
    ?LegalDocument a lexid-s:LegalDocument ;
    lexid-s:amends ?ans ;
    rdfs:label "legal_title"^^xsd:string .
    ?ans a lexid-s:LegalDocument .
    OPTIONAL {
    ?ans rdfs:label ?label .
    }
}
'''
Q_2_4 = '''
SELECT distinct (coalesce(?label , ?ans) as ?answer)
WHERE {
    ?LegalDocument a lexid-s:LegalDocument ;
    lexid-s:repeals ?ans ;
    rdfs:label "legal_title"^^xsd:string .
    ?ans a lexid-s:LegalDocument .
    OPTIONAL {
    ?ans rdfs:label ?label .
    }
}
'''
Q_3_1 = '''
SELECT distinct (concat(?contentLabel, ": ", ?contentName) as ?answer)
WHERE {
    ?LegalDocument a lexid-s:LegalDocument ;
    lexid-s:hasContent ?topLevelContent ;
    rdfs:label "legal_title"^^xsd:string .
    ?topLevelContent lexid-s:hasPart* ?content .
    ?content a lexid-s:Chapter ;
    rdfs:label ?contentLabel ;
    lexid-s:name ?contentName .
}
'''
Q_3_2 = '''
SELECT (count(?article) as ?answer)
WHERE {
    ?LegalDocument a lexid-s:LegalDocument ;
    lexid-s:hasContent ?topLevelContent ;
    rdfs:label "legal_title"^^xsd:string .
    ?topLevelContent lexid-s:hasPart* ?article .
    ?article a lexid-s:Article .
}
'''
Q_4_1 = '''
SELECT distinct (concat(coalesce(?sectionName, ""), " ", ?ans) as ?answer)
WHERE {
    ?LegalDocument a lexid-s:LegalDocument ;
    lexid-s:hasContent ?topLevelContent ;
    rdfs:label "legal_title"^^xsd:string .
    ?topLevelContent lexid-s:hasPart* ?article .
    ?article a lexid-s:Article ;
    rdfs:label "pasal"^^xsd:string .
    {
        {
            ?article lexid-s:hasPart ?section .
            ?section a lexid-s:Section ;
            lexid-s:name ?sectionName ;
            dct:description ?ans .
        }
        UNION
        {
            ?article dct:description ?ans .
        }
    }
}
'''
Q_4_2 = '''
SELECT distinct ?answer
WHERE {
    ?LegalDocument a lexid-s:LegalDocument ;
    lexid-s:hasContent ?topLevelContent ;
    rdfs:label "legal_title"^^xsd:string .
    ?topLevelContent lexid-s:hasPart* ?article .
    ?article a lexid-s:Article ;
    rdfs:label "pasal"^^xsd:string .
    ?article lexid-s:hasPart ?section .
    ?section a lexid-s:Section ;
    rdfs:label "ayat"^^xsd:string ;
    dct:description ?answer .
}
'''
Q_5_1 = '''
SELECT distinct (lcase(group_concat(distinct ?value; separator = "\\n")) as ?answer)
WHERE
{
  {
    SELECT distinct ?year ?number ?article
    (lcase(concat(?larticle, " ", coalesce(?lsection, ""))) as ?lcontent) ?value
    {
        ?document a lexid-s:LegalDocument;
            rdfs:label "legal_title"^^xsd:string .
        ?document (lexid-s:hasContent|lexid-s:hasPart)* ?parent .
        ?document lexid-s:amendedBy ?amendment .
        ?amendment lexid-s:hasContent ?articleI ;
        lexid-s:regulationYear ?year ;
        lexid-s:regulationNumber ?number .
        ?articleI lexid-s:modifies ?modification .
        ?modification lexid-s:hasModificationTarget ?parent ;
        lexid-s:hasModificationContent ?content .
        ?content lexid-s:hasPart* ?article .      
        ?article a lexid-s:Article ;
            rdfs:label ?larticle .
        {
          {
            ?article lexid-s:hasPart ?section .
            ?section a lexid-s:Section ;
            rdfs:label ?lsection ;
            dct:description ?value .
          }
          UNION
          {
            ?article dct:description ?value .
          }
        }
    }
  }
  FILTER regex(str(?lcontent), "pasal ayat", "i")
}
GROUP BY ?year ?number ?article
ORDER BY desc(?year) desc(?number)
LIMIT 1
'''
Q_5_2 = '''
SELECT distinct ?answer
WHERE {
  ?legalDocument a lexid-s:LegalDocument;
  	rdfs:label "legal_title"^^xsd:string;
    lexid-s:amendedBy ?amend .
  ?amend (lexid-s:hasPart|lexid-s:hasContent)* ?child .
  ?child lexid-s:deletes ?deleted .
  ?deleted rdf:type lexid-s:Article ;
           rdfs:label ?answer .               
}
'''
Q_5_3 = '''
SELECT distinct ?answer
WHERE {
  ?legalDocument a lexid-s:LegalDocument;
  	rdfs:label "legal_title"^^xsd:string;
    lexid-s:amendedBy ?amend .
  ?amend (lexid-s:hasPart|lexid-s:hasContent)* ?child .
  ?child lexid-s:adds ?added .
  ?added lexid-s:hasAdditionContent ?addedContent .
  ?addedContent rdf:type lexid-s:Article;
                rdfs:label ?answer         
}
'''
Q_5_4 = '''
SELECT (IF(count(distinct ?amend) > 0, "Ya", "Tidak") as ?answer) 
WHERE {
  {
    ?LegalDocument a lexid-s:LegalDocument ;
  		rdfs:label "legal_title"^^xsd:string ;
    lexid-s:amendedBy ?amend 
  }
  UNION
  {
    ?amend a lexid-s:LegalDocument ;
    	lexid-s:amends ?amended .
    ?amended a lexid-s:LegalDocument ;
    	rdfs:label "legal_title"^^xsd:string ;
  }
}
'''
Q_5_5 = '''
SELECT (IF(count(distinct ?document) > 0, "Tidak", "Ya") as ?answer) 
WHERE {
  {
    ?LegalDocument a lexid-s:LegalDocument ;
  		rdfs:label "legal_title"^^xsd:string ;
    lexid-s:repealedBy ?document 
  }
  UNION
  {
    ?document a lexid-s:LegalDocument ;
    	lexid-s:repeals ?repealed .
    ?repealed a lexid-s:LegalDocument ;
    	rdfs:label "legal_title"^^xsd:string ;
  }
}
'''
templates = {
    0: '',
    1: Q_1_1,
    2: Q_1_2,
    3: Q_1_3,
    4: Q_1_4,
    5: Q_2_1,
    6: Q_2_2,
    7: Q_2_3,
    8: Q_2_4,
    9: Q_3_1,
    10: Q_3_2,
    11: Q_4_1,
    12: Q_4_2,
    13: Q_5_1,
    14: Q_5_2,
    15: Q_5_3,
    16: Q_5_4,
    17: Q_5_5
}

# data = pd.read_csv('question-pattern.csv')
# query_template = []
# for q_index in data['query_index']:
#     query_template.append(PREFIX+templates[int(q_index)])
# print(len(query_template))
# data['query_template'] = query_template
# data.to_csv('question-sparql-template.csv', index=False)
    

data = pd.read_csv('question-sparql-template.csv')
print(data[data['q_pattern'] == 'Apa pertimbangan dalam membuat legal_title?']['query_template'][0])