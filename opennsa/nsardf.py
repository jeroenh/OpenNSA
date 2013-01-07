"""
Core abstractions used in OpenNSA - RDF DB Variant.

In design pattern terms, these would be Data Transfer Objects (DTOs).
Though some of them do actually have some functionality methods.

Author: Jeroen van der Ham <vdham@uva.nl>
Copyright: University of Amsterdam (2012)
"""
import rdflib
# Constants for parsing GOLE topology format
OWL_NS = rdflib.namespace.Namespace("http://www.w3.org/2002/07/owl#")
RDF_NS = rdflib.namespace.Namespace('http://www.w3.org/1999/02/22-rdf-syntax-ns#')
DTOX_NS = rdflib.namespace.Namespace('http://www.glif.is/working-groups/tech/dtox#')


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
class BandwidthParameters:

    def __init__(self, desired=None, minimum=None, maximum=None):
        self.desired = desired
        self.minimum = minimum
        self.maximum = maximum
