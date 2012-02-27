
TEST_TOPOLOGY = """<?xml version="1.0"?>
<rdf:RDF xmlns="http://www.glif.is/working-groups/tech/dtox#"
     xml:base="http://www.glif.is/working-groups/tech/dtox"
     xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"
     xmlns:owl="http://www.w3.org/2002/07/owl#"
     xmlns:xsd="http://www.w3.org/2001/XMLSchema#"
     xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
     xmlns:dtox="http://www.glif.is/working-groups/tech/dtox#">

    <owl:Ontology rdf:about="http://www.glif.is/working-groups/tech/dtox"/>

    <!-- urn:ogf:network:stp:Aruba:A1 -->
    <owl:NamedIndividual rdf:about="urn:ogf:network:stp:Aruba:A1">
        <rdf:type rdf:resource="http://www.glif.is/working-groups/tech/dtox#STP"/>
        <rdfs:comment xml:lang="en">Position : [347,559]</rdfs:comment>
        <connectedTo rdf:resource="urn:ogf:network:stp:Dominica:D4"/>
        <dtox:mapsTo>Aruba_A1</dtox:mapsTo>
    </owl:NamedIndividual>


    <!-- urn:ogf:network:stp:Aruba:A2 -->
    <owl:NamedIndividual rdf:about="urn:ogf:network:stp:Aruba:A2">
        <rdf:type rdf:resource="http://www.glif.is/working-groups/tech/dtox#STP"/>
        <rdfs:comment xml:lang="en">Position : [601,561]</rdfs:comment>
        <dtox:mapsTo>Aruba_A2</dtox:mapsTo>
    </owl:NamedIndividual>


    <!-- urn:ogf:network:stp:Aruba:A3 -->
    <owl:NamedIndividual rdf:about="urn:ogf:network:stp:Aruba:A3">
        <rdf:type rdf:resource="http://www.glif.is/working-groups/tech/dtox#STP"/>
        <rdfs:comment xml:lang="en">Position : [864,558]</rdfs:comment>
        <dtox:mapsTo>Aruba_A4</dtox:mapsTo>
    </owl:NamedIndividual>


    <!-- urn:ogf:network:stp:Aruba:A4 -->
    <owl:NamedIndividual rdf:about="urn:ogf:network:stp:Aruba:A4">
        <rdf:type rdf:resource="http://www.glif.is/working-groups/tech/dtox#STP"/>
        <rdfs:comment xml:lang="en">Position : [1123,557]</rdfs:comment>
        <connectedTo rdf:resource="urn:ogf:network:stp:Bonaire:B1"/>
        <dtox:mapsTo>Aruba_A4</dtox:mapsTo>
    </owl:NamedIndividual>


    <!-- urn:ogf:network:nsnetwork:Aruba -->
    <owl:NamedIndividual rdf:about="urn:ogf:network:nsnetwork:Aruba">
        <rdf:type rdf:resource="http://www.glif.is/working-groups/tech/dtox#NSNetwork"/>
        <rdfs:label xml:lang="en">Aruba</rdfs:label>
        <rdfs:comment xml:lang="en">Position : [696,135]</rdfs:comment>
        <hasSTP rdf:resource="urn:ogf:network:stp:Aruba:A1"/>
        <hasSTP rdf:resource="urn:ogf:network:stp:Aruba:A2"/>
        <hasSTP rdf:resource="urn:ogf:network:stp:Aruba:A3"/>
        <hasSTP rdf:resource="urn:ogf:network:stp:Aruba:A4"/>
        <managedBy rdf:resource="urn:ogf:network:nsa:Aruba"/>
    </owl:NamedIndividual>


    <!-- urn:ogf:network:nsa:Aruba -->
    <owl:NamedIndividual rdf:about="urn:ogf:network:nsa:Aruba">
        <rdf:type rdf:resource="http://www.glif.is/working-groups/tech/dtox#NSA"/>
        <managing rdf:resource="urn:ogf:network:nsnetwork:Aruba" />
        <adminContact rdf:datatype="http://www.w3.org/2001/XMLSchema#string">Aruba network</adminContact>
        <csProviderEndpoint rdf:datatype="http://www.w3.org/2001/XMLSchema#string">http://localhost:9080/NSI/services/ConnectionService</csProviderEndpoint>
        <rdfs:comment xml:lang="en">Position : [93,237]</rdfs:comment>
    </owl:NamedIndividual>


    <!-- urn:ogf:network:stp:Bonaire:B1 -->
    <owl:NamedIndividual rdf:about="urn:ogf:network:stp:Bonaire:B1">
        <rdf:type rdf:resource="http://www.glif.is/working-groups/tech/dtox#STP"/>
        <rdfs:comment xml:lang="en">Position : [1826,468]</rdfs:comment>
        <connectedTo rdf:resource="urn:ogf:network:stp:Aruba:A4"/>
        <dtox:mapsTo>Bonaire_B1</dtox:mapsTo>
    </owl:NamedIndividual>


    <!-- urn:ogf:network:stp:Bonaire:B2 -->
    <owl:NamedIndividual rdf:about="urn:ogf:network:stp:Bonaire:B2">
        <rdf:type rdf:resource="http://www.glif.is/working-groups/tech/dtox#STP"/>
        <rdfs:comment xml:lang="en">Position : [2077,466]</rdfs:comment>
        <dtox:mapsTo>Bonaire_B2</dtox:mapsTo>
    </owl:NamedIndividual>


    <!-- urn:ogf:network:stp:Bonaire:B3 -->
    <owl:NamedIndividual rdf:about="urn:ogf:network:stp:Bonaire:B3">
        <rdf:type rdf:resource="http://www.glif.is/working-groups/tech/dtox#STP"/>
        <rdfs:comment xml:lang="en">Position : [2333,466]</rdfs:comment>
        <dtox:mapsTo>Bonaire_B3</dtox:mapsTo>
    </owl:NamedIndividual>


    <!-- urn:ogf:network:stp:Bonaire:B4 -->
    <owl:NamedIndividual rdf:about="urn:ogf:network:stp:Bonaire:B4">
        <rdf:type rdf:resource="http://www.glif.is/working-groups/tech/dtox#STP"/>
        <rdfs:comment xml:lang="en">Position : [2592,466]</rdfs:comment>
        <connectedTo rdf:resource="urn:ogf:network:stp:Curacao:C1"/>
        <dtox:mapsTo>Bonaire_B4</dtox:mapsTo>
    </owl:NamedIndividual>


    <!-- urn:ogf:network:nsnetwork:Bonaire -->
    <owl:NamedIndividual rdf:about="urn:ogf:network:nsnetwork:Bonaire">
        <rdf:type rdf:resource="http://www.glif.is/working-groups/tech/dtox#NSNetwork"/>
        <rdfs:label xml:lang="en">Bonaire</rdfs:label>
        <rdfs:comment xml:lang="en">Position : [2178,58]</rdfs:comment>
        <hasSTP rdf:resource="urn:ogf:network:stp:Bonaire:B1"/>
        <hasSTP rdf:resource="urn:ogf:network:stp:Bonaire:B2"/>
        <hasSTP rdf:resource="urn:ogf:network:stp:Bonaire:B3"/>
        <hasSTP rdf:resource="urn:ogf:network:stp:Bonaire:B4"/>
        <managedBy rdf:resource="urn:ogf:network:nsa:Bonaire"/>
    </owl:NamedIndividual>


    <!-- urn:ogf:network:nsa:Bonaire-->
    <owl:NamedIndividual rdf:about="urn:ogf:network:nsa:Bonaire">
        <rdf:type rdf:resource="http://www.glif.is/working-groups/tech/dtox#NSA"/>
        <rdfs:label xml:lang="en">SURFnet OpenDRAC - The NSI Edition</rdfs:label>
        <managing rdf:resource="urn:ogf:network:nsnetwork:Bonaire" />
        <adminContact rdf:datatype="http://www.w3.org/2001/XMLSchema#string">Bonaire Network</adminContact>
        <csProviderEndpoint rdf:datatype="http://www.w3.org/2001/XMLSchema#string">http://localhost:9081/NSI/services/ConnectionService</csProviderEndpoint>
        <rdfs:comment xml:lang="en">Position : [1586,174]</rdfs:comment>
    </owl:NamedIndividual>


    <!-- urn:ogf:network:stp:Curacao:C1 -->
    <owl:NamedIndividual rdf:about="urn:ogf:network:stp:Curacao:C1">
        <rdf:type rdf:resource="http://www.glif.is/working-groups/tech/dtox#STP"/>
        <rdfs:comment xml:lang="en">Position : [3463,454]</rdfs:comment>
        <connectedTo rdf:resource="urn:ogf:network:stp:Bonaire:B4"/>
        <dtox:mapsTo>Curacao_C1</dtox:mapsTo>
    </owl:NamedIndividual>


    <!-- urn:ogf:network:stp:Curacao:C2 -->
    <owl:NamedIndividual rdf:about="urn:ogf:network:stp:Curacao:C2">
        <rdf:type rdf:resource="http://www.glif.is/working-groups/tech/dtox#STP"/>
        <rdfs:comment xml:lang="en">Position : [3725,455]</rdfs:comment>
        <dtox:mapsTo>Curacao_C2</dtox:mapsTo>
    </owl:NamedIndividual>


    <!-- urn:ogf:network:stp:Curacao:C3 -->
    <owl:NamedIndividual rdf:about="urn:ogf:network:stp:Curacao:C3">
        <rdf:type rdf:resource="http://www.glif.is/working-groups/tech/dtox#STP"/>
        <rdfs:comment xml:lang="en">Position : [3981,458]</rdfs:comment>
        <dtox:mapsTo>Curacao_C3</dtox:mapsTo>
    </owl:NamedIndividual>


    <!-- urn:ogf:network:stp:Curacao:C4 -->
    <owl:NamedIndividual rdf:about="urn:ogf:network:stp:Curacao:C4">
        <rdf:type rdf:resource="http://www.glif.is/working-groups/tech/dtox#STP"/>
        <rdfs:comment xml:lang="en">Position : [4239,458]</rdfs:comment>
        <connectedTo rdf:resource="urn:ogf:network:stp:Dominica:D1"/>
        <dtox:mapsTo>Curacao_C4</dtox:mapsTo>
    </owl:NamedIndividual>


    <!-- urn:ogf:network:nsnetwork:Curacao -->
    <owl:NamedIndividual rdf:about="urn:ogf:network:nsnetwork:Curacao">
        <rdf:type rdf:resource="http://www.glif.is/working-groups/tech/dtox#NSNetwork"/>
        <rdfs:label xml:lang="en">Curacao</rdfs:label>
        <rdfs:comment xml:lang="en">Position : [3690,102]</rdfs:comment>
        <hasSTP rdf:resource="urn:ogf:network:stp:Curacao:C1"/>
        <hasSTP rdf:resource="urn:ogf:network:stp:Curacao:C2"/>
        <hasSTP rdf:resource="urn:ogf:network:stp:Curacao:C3"/>
        <hasSTP rdf:resource="urn:ogf:network:stp:Curacao:C4"/>
        <managedBy rdf:resource="urn:ogf:network:nsa:Curacao"/>
    </owl:NamedIndividual>


    <!-- urn:ogf:network:nsa:Curacao -->
    <owl:NamedIndividual rdf:about="urn:ogf:network:nsa:Curacao">
        <rdf:type rdf:resource="http://www.glif.is/working-groups/tech/dtox#NSA"/>
        <managing rdf:resource="urn:ogf:network:nsnetwork:Curacao" />
        <adminContact rdf:datatype="http://www.w3.org/2001/XMLSchema#string">1.	Curacao Admin Contact</adminContact>
        <csProviderEndpoint rdf:datatype="http://www.w3.org/2001/XMLSchema#string">http://localhost:9082/NSI/services/ConnectionService</csProviderEndpoint>
        <rdfs:comment xml:lang="en">Position : [3138,173]</rdfs:comment>
    </owl:NamedIndividual>


    <!-- urn:ogf:network:stp:Dominica:D1 -->
    <owl:NamedIndividual rdf:about="urn:ogf:network:stp:Dominica:D1">
        <rdf:type rdf:resource="http://www.glif.is/working-groups/tech/dtox#STP"/>
        <rdfs:comment xml:lang="en">Position : [3348,1237]</rdfs:comment>
        <connectedTo rdf:resource="urn:ogf:network:stp:Curacao:C4"/>
    </owl:NamedIndividual>


    <!-- urn:ogf:network:stp:Dominica:D2 -->
    <owl:NamedIndividual rdf:about="urn:ogf:network:stp:Dominica:D2">
        <rdf:type rdf:resource="http://www.glif.is/working-groups/tech/dtox#STP"/>
        <rdfs:comment xml:lang="en">Position : [3601,1237]</rdfs:comment>
    </owl:NamedIndividual>


    <!-- urn:ogf:network:stp:Dominica:D3 -->
    <owl:NamedIndividual rdf:about="urn:ogf:network:stp:Dominica:D3">
        <rdf:type rdf:resource="http://www.glif.is/working-groups/tech/dtox#STP"/>
        <rdfs:comment xml:lang="en">Position : [3862,1237]</rdfs:comment>
    </owl:NamedIndividual>


    <!-- urn:ogf:network:stp:Dominica:D4 -->
    <owl:NamedIndividual rdf:about="urn:ogf:network:stp:Dominica:D4">
        <rdf:type rdf:resource="http://www.glif.is/working-groups/tech/dtox#STP"/>
        <rdfs:comment xml:lang="en">Position : [4125,1233]</rdfs:comment>
        <connectedTo rdf:resource="urn:ogf:network:stp:Aruba:A1"/>
    </owl:NamedIndividual>


    <!-- urn:ogf:network:nsa:Dominica -->
    <owl:NamedIndividual rdf:about="urn:ogf:network:nsnetwork:Dominica">
        <rdf:type rdf:resource="http://www.glif.is/working-groups/tech/dtox#NSNetwork"/>
        <rdfs:label xml:lang="en">Dominica</rdfs:label>
        <rdfs:comment xml:lang="en">Position : [3522,838]</rdfs:comment>
        <hasSTP rdf:resource="urn:ogf:network:stp:Dominica:D1"/>
        <hasSTP rdf:resource="urn:ogf:network:stp:Dominica:D2"/>
        <hasSTP rdf:resource="urn:ogf:network:stp:Dominica:D3"/>
        <hasSTP rdf:resource="urn:ogf:network:stp:Dominica:D4"/>
        <managedBy rdf:resource="urn:ogf:network:nsa:Dominica"/>
    </owl:NamedIndividual>


    <!-- urn:ogf:network:nsa:Dominica-->
    <owl:NamedIndividual rdf:about="urn:ogf:network:nsa:Dominica">
        <rdf:type rdf:resource="http://www.glif.is/working-groups/tech/dtox#NSA"/>
        <managing rdf:resource="urn:ogf:network:nsnetwork:Dominica" />
        <csProviderEndpoint rdf:datatype="http://www.w3.org/2001/XMLSchema#string">http://localhost:9083/NSI/services/ConnectionService</csProviderEndpoint>
        <adminContact rdf:datatype="http://www.w3.org/2001/XMLSchema#string">Dominica Network</adminContact>
        <rdfs:comment xml:lang="en">Position : [3099,915]</rdfs:comment>
    </owl:NamedIndividual>

</rdf:RDF>
"""

