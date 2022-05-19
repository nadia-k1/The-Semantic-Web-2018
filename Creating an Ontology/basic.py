import logging
import rdflib
from rdflib.graph import Graph, URIRef
from SPARQLWrapper import SPARQLWrapper, RDF
from rdflib.plugins.memory import IOMemory

# configuring logging
logging.basicConfig()
 
# configuring the end-point and constructing query
sparql = SPARQLWrapper("http://dbpedia.org/sparql")
construct_query="""
      PREFIX ma: <http://www.semanticweb.org/ontologies/2018/Ontology1.owl#>
      PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>        
      PREFIX foaf: <http://xmlns.com/foaf/0.1/>
      PREFIX dbpedia-owl: <http://dbpedia.org/ontology/>
      PREFIX dbpprop: <http://dbpedia.org/property/>
      
      CONSTRUCT {
      ?film rdf:type ma:Movie .
      ?film ma:movieName ?name .
      ?film ma:movieAbstract ?abstract .
      ?film ma:runtime ?runtime . 
      ?film ma:hasLanguage ?language .
      	?language rdf:type ma:Language .
      ?film ma:hasActor ?actor .
      	?actor rdf:type ma:Actor .
      ?film ma:musicBy ?musicComposer .
      	?musicComposer rdf:type ma:MusicComposer .
      ?film ma:directedBy ?director .
      	?director rdf:type ma:Director .
      ?film ma:producedBy ?producer .
      	?producer rdf:type ma:Producer .
      ?film ma:filmedIn ?country .
      	?country rdf:type ma:Country .
      ?film ma:writtenBy ?screenwriter .
      	?screenwriter rdf:type ma:Writer .
      }
       WHERE{
       ?film rdf:type dbpedia-owl:Film .
       ?film foaf:name ?name .
       OPTIONAL {?film dbpedia-owl:abstract ?abstract} 
       OPTIONAL {?film dbpprop:runtime ?runtime}
       OPTIONAL {?film dbpedia-owl:language ?language}
       OPTIONAL {?film dbpedia-owl:starring ?actor} 
       OPTIONAL {?film dbpedia-owl:musicComposer ?musicComposer} 
       OPTIONAL {?film dbpedia-owl:director ?director}
       OPTIONAL {?film dbpedia-owl:producer ?producer}
       OPTIONAL {?film dbpedia-owl:country ?country}
       OPTIONAL {?film dbpedia-owl:writer ?screenwriter}
       FILTER (LANG(?name)="en")
       FILTER (LANG(?abstract)="en")
	   }
	   LIMIT 100000
	   """
sparql.setQuery(construct_query)
sparql.setReturnFormat(RDF)

# creating the RDF store and graph
memory_store=IOMemory()
graph_id=URIRef("http://www.semanticweb.org/store/movie")
g = Graph(store=memory_store, identifier=graph_id)
rdflib.plugin.register('sparql', rdflib.query.Processor, 'rdfextras.sparql.processor', 'Processor')
rdflib.plugin.register('sparql', rdflib.query.Result, 'rdfextras.sparql.query', 'SPARQLQueryResult')

# merging results and saving the store
g = sparql.query().convert()
g.parse("Ontology1.owl")
g.serialize("Ontology2.owl", "xml")
