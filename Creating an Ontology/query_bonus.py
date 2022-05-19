import logging
import rdflib

# configuring logging
logging.basicConfig()

# creating the graph
g=rdflib.Graph()
result=g.parse("Ontology3.owl", "xml")
print("graph has %s statements.\n" % len(g))

# Query to return 15 movies filmed in countries with population more than 100 million: FILTER (?population > 10000000)
# FILTER regex(str(?countryName_movie), str(?countryName_country)) combines movies and countries information. 
# Population information is from LinkedMDB.
# Not all information is in DBpedia and not in the format needed for my ontology, whereas movies information is from DBpedia only.
query1="""
PREFIX mc: <http://www.semanticweb.org/ontologies/2018/Ontology1.owl#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>  
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> 
SELECT DISTINCT ?movieName ?countryName_country ?population
WHERE { ?film rdf:type mc:Movie .
        ?film mc:movieName ?movieName .
        ?film mc:filmedIn ?countryName_movie .
		?country rdf:type mc:Country .
                ?country mc:countryName ?countryName_country .
                ?country mc:population ?population .
	FILTER regex(str(?countryName_movie), str(?countryName_country))
	FILTER (?population > 100000000)
        }LIMIT 15
        """

# querying and displaying the results
print ('{0:40s} {1:20s} {2:10s}'.format("Title","Filmed in","Population"))
print ('{0:40s} {1:20s} {2:10s}'.format("----------------------------------------","--------------------","------------------"))
for name,country,population in g.query(query1):
    print ('{0:40s} {1:20s} {2:10s}'.format(name,country,population))
    
print ("\n\n")

# Query	to return movies filmed in countries that have a capital "Canberra"
query2="""
PREFIX mc: <http://www.semanticweb.org/ontologies/2018/Ontology1.owl#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>  
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> 
SELECT DISTINCT ?movieName ?countryName_country ?capital
WHERE { ?film rdf:type mc:Movie .
        	?film mc:movieName ?movieName .
        	?film mc:filmedIn ?countryName_movie .
	?country rdf:type mc:Country .
                ?country mc:countryName ?countryName_country .
                ?country mc:capital ?capital .
        FILTER regex(str(?countryName_movie), str(?countryName_country))
	FILTER regex(str(?capital),"Canberra")
        }
        """
		
# querying and displaying the results
print ('{0:40s} {1:20s} {2:10s}'.format("Title","Filmed in","Capital"))
print ('{0:40s} {1:20s} {2:10s}'.format("----------------------------------------","--------------------","------------------"))
for name,country,capital in g.query(query2):
    print ('{0:40s} {1:20s} {2:10s}'.format(name,country,capital))

print ("\n\n")

# Query	to return movies filmed in countries that have a square kilometres area between 300000 and 400000	
query3="""
PREFIX mc: <http://www.semanticweb.org/ontologies/2018/Ontology1.owl#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>  
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> 
SELECT DISTINCT ?movieName ?countryName_country ?area
WHERE { ?film rdf:type mc:Movie .
        	?film mc:movieName ?movieName .
        	?film mc:filmedIn ?countryName_movie .
	?country rdf:type mc:Country .
        	?country mc:countryName ?countryName_country .
        	?country mc:totalArea ?area .
	FILTER regex(str(?countryName_movie), str(?countryName_country))
	FILTER (?area > 300000.0 && ?area < 400000.0)
        }
        """
# querying and displaying the results
print ('{0:40s} {1:20s} {2:10s}'.format("Title","Filmed in","Area(sqkm)"))
print ('{0:40s} {1:20s} {2:10s}'.format("----------------------------------------","--------------------","------------------"))
for name,country,area in g.query(query3):
    print ('{0:40s} {1:20s} {2:10s}'.format(name,country,area))

print ("\n\n")
	
# Query	to return movies filmed in South America continent with a population more than 200M
query4="""
PREFIX mc: <http://www.semanticweb.org/ontologies/2018/Ontology1.owl#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>  
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> 
SELECT DISTINCT ?movieName ?countryName_country ?countrycontinent ?population
WHERE { ?film rdf:type mc:Movie .
        	?film mc:movieName ?movieName .
        	?film mc:filmedIn ?countryName_movie .
	?country rdf:type mc:Country .
        	?country mc:countryName ?countryName_country .
        	?country mc:continent ?countrycontinent .
        	?country mc:population ?population .
	FILTER regex(str(?countryName_movie), str(?countryName_country))
	FILTER regex(str(?countrycontinent),"SA")
        FILTER (?population > 200000000)
        }
        """
# querying and displaying the results
print ('{0:30s} {1:10s} {2:20s} {3:10s}'.format("Title","Filmed in","Continent", "Population"))
print ('{0:30s} {1:10s} {2:20s} {3:10s}'.format("------------------------------","---------","--------------------","--------------------"))
for name,country,continent,population in g.query(query4):
    print ('{0:30s} {1:10s} {2:20s} {3:10s}'.format(name,country,continent,population))
