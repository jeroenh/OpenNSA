"""
OpenNSA RDF topology database and parser.

Author: Jeroen van der Ham <vdham@uva.nl

Copyright: University of Amsterdam (2012)
"""

import rdflib
import os.path

from opennsa import nsardf as nsa
from opennsa import  error
from opennsa.topology import dijkstra


OWL_NS = rdflib.namespace.Namespace("http://www.w3.org/2002/07/owl#")
RDF_NS = rdflib.namespace.Namespace('http://www.w3.org/1999/02/22-rdf-syntax-ns#')
DTOX_NS = rdflib.namespace.Namespace('http://www.glif.is/working-groups/tech/dtox#')


# TODO make configurable
RDFDB = "/Users/jeroen/Projects/OpenNSA-UvA/opennsa/rdfdb"

class Topology(object):
    """
    TopologyRDF is an RDF-db based substitute for the regular Topology object.
    Basically it provides a way for the legacy OpenNSA to interact with an RDF db.
    """
    def __init__(self, graph):
        super(Topology, self).__init__()
        self.graph = graph
    
    def addNetwork(self,network):
        # Network has already been parsed into the DB, no need to add.
        pass
    def getNetwork(self,network_name):
        if not network_name.startswith("urn:ogf:network:nsnetwork:"):
            networkURI = rdflib.URIRef("urn:ogf:network:nsnetwork:"+network_name)
        else:
            networkURI = network_name
        if (networkURI,RDF_NS.type,DTOX_NS.NSNetwork) in self.graph:
            return nsa.Network(networkURI,self.graph)
        else:
            raise error.TopologyError('No network named %s (%s)' % (network_name,networkURI))
    def getEndpoint(self, network, endpoint):
        """docstring for getEndpoint"""
        network = self.getNetwork(network)
        return network.getEndpoint(endpoint)
    def getEndpoint1(self, endpoint):
        endpoint = rdflib.URIRef(endpoint)
        if (endpoint, RDF_NS.type, DTOX_NS.STP) in self.graph:
            network = self.graph.value(predicate=DTOX_NS.hasSTP, object=endpoint)
            return self.getEndpoint(network,endpoint)
        else:
            raise Exception("Unknown Endpoint %s" % endpoint)
        
        
    def convertSDPRouteToLinks(self, source_ep,dest_ep,route):
        """docstring for convertSDPRouteToLinks"""
        raise NotImplementedError("Topology.convertSDPRouteToLinks is not implemented")
    def findPath(self, source_stp, dest_stp, bandwidth=None):
        d = dijkstra.Dijkstra(self.graph)
        return d.findShortestPath(str(source_stp.uri), str(dest_stp.uri), bandwidth)
    def findPaths(self, source_stp, dest_stp, bandwidth=None):
        d = dijkstra.Dijkstra(self.graph)
        return d.findShortestPaths(str(source_stp.uri), str(dest_stp.uri), bandwidth)
    # def _pruneMismatchedPorts(self, network_paths):
    #         """docstring for _pruneMismatchedPorts"""
    #     pass
    # def findPathEndpoints(self, source_stp, dest_stp, visited_networks=None):
    #     """docstring for findPathEndpoints"""
    #    pass
    # def filterBandwidth(self, paths_sdps, bandwidths):
    #     """docstring for filterBandwidth"""
    #     pass
    def __str__(self):
        return '\n'.join( [ str(n) for n in self.networks ] )
        
            

def parseGOLETopology(topology_source,identifier="opennsa",reload_source=False):
    def stripURNPrefix(text):
        URN_PREFIX = 'urn:ogf:network:'
        assert text.startswith(URN_PREFIX)
        return text.split(':')[-1]

    OWL_NS = rdflib.namespace.Namespace("http://www.w3.org/2002/07/owl#")
    RDF_NS = rdflib.namespace.Namespace('http://www.w3.org/1999/02/22-rdf-syntax-ns#')
    DTOX_NS = rdflib.namespace.Namespace('http://www.glif.is/working-groups/tech/dtox#')

    graph = rdflib.Graph(store="Sleepycat",identifier=identifier)
    # TODO: Change this to some configurable option.
    graph.open(RDFDB)
    if reload_source:
        try:
            if os.path.isfile(topology_source) or topology_source.startswith("http:"):
                graph.parse(topology_source)
            else:
                graph.parse(data=topology_source)
        except Exception as e:
            raise error.TopologyError('Invalid topology source: %s' % e)

    topo = Topology(graph)

    # Objects are created on the fly.
    
    # for nsnetwork in graph.subjects(RDF_NS['type'],DTOX_NS['NSNetwork']):
    #         # Setup the base network object, with NSA
    #         nsaId = graph.value(subject=nsnetwork, predicate=DTOX_NS['managedBy'])
    #         network_nsa_ep = graph.value(subject=nsaId, predicate=DTOX_NS['csProviderEndpoint'])
    #         network_nsa = NetworkServiceAgent(nsaId, graph)
    #         network = Network(nsnetwork, graph)
    # 
    #         # Add all the STPs and connections to the network
    #         for stp in graph.objects(nsnetwork, DTOX_NS['hasSTP']):
    #             # stp_name = stripURNPrefix(str(stp))
    #             dest_stp = graph.value(subject=stp, predicate=DTOX_NS['connectedTo'])
    #             # If there is a destination, add that, otherwise the value stays None.
    #             if dest_stp:
    #                 dest_network = graph.value(predicate=DTOX_NS['hasSTP'], object=dest_stp)
    #                 dest_stp = STP(dest_dest_stp, graph, dest_network)
    #             ep = NetworkEndpoint(stp, graph, network)
    #             network.addEndpoint(ep)
    # 
    #         topo.addNetwork(network)

    return topo
