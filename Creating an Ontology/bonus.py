import logging
import rdflib
from rdflib import Graph, URIRef
from SPARQLWrapper import SPARQLWrapper, RDF
from rdflib.plugins.memory import IOMemory

# configuring logging
logging.basicConfig()
 
# configuring the end-point and constructing query
sparql = SPARQLWrapper("http://data.linkedmdb.org/sparql")
construct_query="""
      PREFIX ma: <http://www.semanticweb.org/ontologies/2018/Ontology1.owl#>
      PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>        
      PREFIX movie: <http://data.linkedmdb.org/resource/movie/>
      PREFIX rdfs:<http://www.w3.org/2000/01/rdf-schema#>
      PREFIX dc: <http://purl.org/dc/terms/>
      prefix owl: <http://www.w3.org/2002/07/owl#>
      
      CONSTRUCT {
      ?country rdf:type ma:Country .
      ?country ma:countryName ?name .
      ?country ma:capital ?capital.
      ?country ma:population ?population.
      ?country ma:currency ?currency .
      ?country ma:totalArea ?area .
      ?country ma:continent ?continent .
      }
       WHERE{
       ?country rdf:type movie:country .
       OPTIONAL {?country movie:country_name ?name }
       OPTIONAL {?country movie:country_capital ?capital }
       OPTIONAL {?country movie:country_population ?population }
       OPTIONAL {?country movie:country_currency ?currency}
       OPTIONAL {?country movie:country_areaInSqKm ?area}
       OPTIONAL {?country movie:country_continent ?continent}
       }
       LIMIT 246
       """

sparql.setQuery(construct_query)
sparql.setReturnFormat(RDF)

# creating the RDF store and graph
memory_store=IOMemory()
graph_id=URIRef('http://www.semanticweb.org/store/movie')
g = Graph(store=memory_store, identifier=graph_id)
rdflib.plugin.register('sparql', rdflib.query.Processor, 'rdfextras.sparql.processor', 'Processor')
rdflib.plugin.register('sparql', rdflib.query.Result, 'rdfextras.sparql.query', 'SPARQLQueryResult')

# merging results and saving the store 
g = sparql.query().convert()
g.parse("Ontology2.owl")
g.serialize("Ontology3.owl", "xml")
