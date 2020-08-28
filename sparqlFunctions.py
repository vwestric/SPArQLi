#SPARQL Functions
#Family Places
#Find in which issuance which family members are mentioned 
#(as identified by the respective property), group by Families
def familyPlaces(g, id):
    #Libraries
    import rdflib

    #Variables
    output = []

    #SPARQL Query
    result = g.query("""
                        SELECT ?place ?long ?lat (count(?place) as ?count)
                        WHERE {
                            {
                                ?a P:P53 Q:%s .
                                ?a P:P1343 ?regest .
                                ?regest P:P291 ?place .
                                ?place GEO:long ?long .
                                ?place GEO:lat ?lat .
                            }
                            UNION
                            {
                                ?a P:P53 Q:%s .
                                ?a P:P1817 ?regest .
                                ?regest P:P291 ?place .
                                ?place GEO:long ?long .
                                ?place GEO:lat ?lat .
                            }
                        }
                        GROUP BY ?place
                        ORDER BY DESC(?count)
                        LIMIT 300
                      """ % (id, id)
                     )

    #Output
    for row in result:
        output.append([node.toPython() for node in row])

    return output

#Issuance Places
def issuancePlaces(g, dep):
    #Libraries
    import rdflib
    
    #Variables
    output = []
    
    #SPARQL Query
    result = g.query("""
                        SELECT ?place ?long ?lat (count(?place) as ?count)
                        WHERE {
                                ?a ?p ?regest .
                                ?regest P:P361 Q:%s .
                                ?regest P:P291 ?place .
                                ?place GEO:long ?long .
                                ?place GEO:lat ?lat .
                            }
                    GROUP BY ?place
                    ORDER BY DESC(?count)
                    LIMIT 500
                    """% (dep)
                    ) 
    
    #Output
    for row in result:
        output.append([node.toPython() for node in row])

    return output


#Find which entities recurr in all three registries (except issuance places)
def recurringEntities(g):
    #Libraries
    import rdflib

    #Variables
    output = []

    #SPARQL Query
    result = g.query("""
                        SELECT ?entity (count(?entity) as ?count)
                        WHERE {
                                ?entry OWL:sameAs ?entity .
                        }
                        GROUP BY ?entity
                        ORDER BY DESC(?count)
                      """
                     )    

    #Output
    for row in result:
        output.append([node.toPython() for node in row])
    
    return output

#Occupations or Positions Held by a Specific Family
def occupationByFamily(g, family):
    # Libraries
    import rdflib

    # Variables
    output = []

    # SPARQL Query
    result = g.query("""
                        SELECT ?occupation (count(?occupation) as ?count)
                        WHERE {
                                {
                                        ?entry P:P53 Q:%s .
                                        ?entry P:P106 ?occupation .
                                }
                                UNION 
                                {
                                        ?entry P:P53 Q:%s .
                                        ?entry P:P39 ?occupation .
                                }
                        }
                        GROUP BY ?occupation
                        ORDER BY DESC(?count)
                      """ % (family, family)
                     )

    # Output
    for row in result:
        output.append([node.toPython() for node in row])

    return output

#Find out if an Entity has corresponding Regests in an Department
def existsInDep(g, id, dep):
    # Libraries
    import rdflib

    # Variables
    output = []

    # SPARQL Query
    result = g.query("""
                            SELECT ?regest
                            WHERE {
                                    {
                                        ?entry OWL:sameAs Q:%s .
                                        ?entry ?property ?regest . 
                                        ?regest P:P361 Q:%s .
                                    }
                                    UNION
                                    {
                                        ?entry OWL:sameAs Q:%s .
                                        ?regest ?property ?entry . 
                                        ?regest P:P361 Q:%s .
                                    }
                            }
                          LIMIT 1
                          """ % (id, dep, id, dep)
                     )

    # Output
    for row in result:
        output.append([node.toPython() for node in row])

    if output:
        return True
    else:
        return False


#Get Entries corresponding to an Entity
def associatedEntries(g, id):
    # Libraries
    import rdflib

    # Variables
    output = []

    # SPARQL Query
    result = g.query("""
                            SELECT ?entry
                            WHERE {
                                    ?entry OWL:sameAs Q:%s .
                                }
                          """ % id
                     )

    # Output
    for row in result:
        output.append([node.toPython() for node in row])

    return output

def count(g, property):
    # Libraries
    import rdflib

    # Variables
    output = []

    # SPARQL Query
    result = g.query("""
                            SELECT ?object (count(?object) as ?count)
                            WHERE {
                                    ?entry P:%s ?object .
                                }
                            GROUP BY ?object
                            ORDER BY DESC(?count)
                    """ % property
                     )

    # Output
    for row in result:
        output.append([node.toPython() for node in row])

    return output

#Occupations by Place of Issuance
def occupationByIssuancePlaces(g, occupation):
    # Libraries
    import rdflib

    # Variables
    output = []

    # SPARQL Query
    result = g.query("""
                            SELECT ?entity ?long ?lat (count(?entity) as ?count)
                            WHERE {
                                    ?entry P:P106 Q:%s .
                                    ?a P:P1817 ?regest .
                                    ?regest P:P291 ?place .
                                    ?place OWL:sameAs ?entity .
                                    ?place GEO:long ?long .
                                    ?place GEO:lat ?lat .
                            }
                        GROUP BY ?entity
                        ORDER BY DESC(?count)
                        LIMIT 300
                        """ % occupation
                     )

    # Output
    for row in result:
        output.append([node.toPython() for node in row])

    return output