"""
OpenNSA RDF topology database and parser.

Author: Jeroen van der Ham <vdham@uva.nl

Copyright: University of Amsterdam (2012)
"""

import rdflib

from opennsa import nsa, error, dijkstra


# Constants for parsing GOLE topology format
OWL_NS = rdflib.namespace.Namespace("http://www.w3.org/2002/07/owl#")
RDF_NS = rdflib.namespace.Namespace('http://www.w3.org/1999/02/22-rdf-syntax-ns#')
DTOX_NS = rdflib.namespace.Namespace('http://www.glif.is/working-groups/tech/dtox#')

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
            return Network(networkURI,self.graph)
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
        """docstring for findPaths"""
        d = dijkstra.Dijkstra(self.graph)
        return d.findShortestPath(str(source_stp.uri), str(dest_stp.uri), bandwidth)
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
        
            
class RDFObject(object):
    """Baseclass for NSA RDF Objects"""
    def __init__(self, uri, graph):
        super(RDFObject, self).__init__()
        self.uri = uri
        self.graph = graph
    def urn(self):
        return self.uri
    def __str__(self):
        return '<RDFObject %s %s>' % (self.__class__.__name__, self.uri)

class Network(RDFObject):
    """Wrapper class for NSNetwork object"""
    def __init__(self, uri, graph):
        super(Network, self).__init__(uri, graph)
        label = self.graph.value(subject=self.uri,predicate=RDF_NS.label)
        if label:
            self.name = label
        else:
            # len("urn:ogf:network:nsnetwork:") = 26
            self.name = self.uri[26:]
        nsaID = self.graph.value(subject=uri, predicate=DTOX_NS.managedBy)
        self.nsa = NetworkServiceAgent(nsaID,self.graph)
    def addEndpoint(self,endpoint):
        raise NotImplementedError("Network.addEndpoint is not implemented")
    def getEndpoint(self, endpoint_name):
        if (self.uri, DTOX_NS.hasSTP, rdflib.URIRef(endpoint_name)) in self.graph:
            return NetworkEndpoint(endpoint_name, self.graph, self)
        else:
            raise Exception("Unknown Endpoint %s in Network %s" % (endpoint_name, self))

class NetworkServiceAgent(RDFObject):
    """Wrapper class for NetworkServiceAgent"""
    def __init__(self, uri, graph):
        super(NetworkServiceAgent, self).__init__(uri, graph)
        self.identity = self.uri[20:]
        # self.endpoint = graph.value(subject=uri, predicate=DTOX_NS.csProviderEndpoint)
    def getHostPort(self):
        raise NotImplementedError("NetworkServiceAgent.getHostPort is not implemented")
    def url(self):
        return str(self.graph.value(subject=self.uri, predicate=DTOX_NS.csProviderEndpoint))
        raise NotImplementedError("NetworkServiceAgent.url is not implemented")

class STP(RDFObject):
    """Wrapper class for STP"""
    def __init__(self, uri, graph, network):
    # def __init__(self, uri, graph, network, endpoint):
        super(STP, self).__init__(uri, graph)
        self.network = network.name
        # self.endpoint = endpoint
    def __eq__(self, other):
        if not isinstance(other, STP):
            return False
        return self.uri == other.uri

class NetworkEndpoint(STP):
    """Wrapper class for NetworkEndpoint"""
    def __init__(self, uri, graph, network):
        super(NetworkEndpoint, self).__init__(uri, graph, network)
        # def __init__(self, uri, graph, network, endpoint, nrm_port=None, dest_stp=None, max_capacity=None, available_capacity=None):
        # self.network = network.name
        # TODO
        self.endpoint = self.uri.split(":")[-1]
        # self.nrm_port = nrm_port
        # self.dest_stp = dest_stp
        # self.max_capacity = max_capacity
        # self.available_capacity = available_capacity
    def nrmPort(self):
        return self.uri.split(":")[-1]
        # return self.graph.value(subject=self.uri,predicate=DTOX_NS.mapsTo)
    # def __str__(self):
    #         return '<NetworkEndpoint %s:%s-%s#%s>' % (self.network, self.endpoint, self.dest_stp, self.nrm_port)

def parseGOLETopology(topology_source,reload_source=False):
    def stripURNPrefix(text):
        URN_PREFIX = 'urn:ogf:network:'
        assert text.startswith(URN_PREFIX)
        return text.split(':')[-1]

    OWL_NS = rdflib.namespace.Namespace("http://www.w3.org/2002/07/owl#")
    RDF_NS = rdflib.namespace.Namespace('http://www.w3.org/1999/02/22-rdf-syntax-ns#')
    DTOX_NS = rdflib.namespace.Namespace('http://www.glif.is/working-groups/tech/dtox#')

    graph = rdflib.Graph(store="Sleepycat")
    # TODO: Change this to some configurable option.
    graph.open("/Users/jeroen/Projects/OpenNSA-UvA/opennsa/rdfdb")
    if reload_source:
        try:
            graph.parse(topology_source)
        except:
            raise error.TopologyError('Invalid topology source')

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
