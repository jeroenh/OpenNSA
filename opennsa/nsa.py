"""
Core abstractions used in OpenNSA.

In design pattern terms, these would be Data Transfer Objects (DTOs).
Though some of them do actually have some functionality methods.

Author: Henrik Thostrup Jensen <htj@nordu.net>
Copyright: NORDUnet (2011)
"""


import urlparse

from opennsa import error



STP_PREFIX = 'urn:ogf:network:stp:'
NSA_PREFIX = 'urn:ogf:network:nsa:'

LOG_SYSTEM = 'opennsa.nsa'



class STP: # Service Termination Point

    def __init__(self, network, endpoint):
        assert type(network) is str, 'Invalid network type provided for STP initialization'
        assert type(endpoint) is str, 'Invalid endpoint type provided for STP initialization'
        self.network = network
        self.endpoint = endpoint


    def urn(self):
        return STP_PREFIX + self.network + ':' + self.endpoint


    def __eq__(self, other):
        if not isinstance(other, STP):
            return False
        return self.network == other.network and self.endpoint == other.endpoint


    def __str__(self):
        return '<STP %s:%s>' % (self.network, self.endpoint)



class Link: # intra network link

    def __init__(self, network, source, dest):
        self.network = network
        self.source = source
        self.dest = dest


    def sourceSTP(self):
        return STP(self.network, self.source)


    def destSTP(self):
        return STP(self.network, self.dest)


    def __eq__(self, other):
        if not isinstance(other, Link):
            return False
        return self.network == other.network and self.source == other.source and self.dest == other.dest


    def __str__(self):
        return '<Link %s::%s=%s>' % (self.network, self.source, self.dest)




class Path:
    """
    Represent a path from a source and destitionation STP, with the endpoint pairs between them.
    """
    def __init__(self, network_links):
        self.network_links = network_links


    def links(self):
        return self.network_links


    def sourceEndpoint(self):
        return self.network_links[0].sourceSTP()


    def destEndpoint(self):
        return self.network_links[-1].destSTP()


    def __str__(self):
        return '<Path: ' + ' '.join( [ str(nl) for nl in self.network_links ] ) + '>'



class NetworkEndpoint(STP):

    def __init__(self, network, endpoint, nrm_port=None, dest_stp=None, max_capacity=None, available_capacity=None):
        STP.__init__(self, network, endpoint)
        if nrm_port is not None:
            assert type(nrm_port) is str, 'Invalid nrm_port type provided for NetworkEndpoint initialization'
        self.nrm_port = nrm_port
        self.dest_stp = dest_stp
        self.max_capacity = max_capacity
        self.available_capacity = available_capacity


    def nrmPort(self):
        assert self.nrm_port is not None, 'No NRM port defined for NetworkEndpoint %s' % str(self)
        return self.nrm_port


    def __str__(self):
        return '<NetworkEndpoint %s:%s-%s#%s>' % (self.network, self.endpoint, self.dest_stp, self.nrm_port)



class NetworkServiceAgent:

    def __init__(self, identity, endpoint): #, service_attributes=None):
        assert type(identity) is str, 'NSA identity type must be string (type: %s, value %s)' % (type(identity), identity)
        assert type(endpoint) is str, 'NSA endpoint type must be string (type: %s, value %s)' % (type(endpoint), endpoint)
        self.identity = identity
        self.endpoint = endpoint.strip()


    def getHostPort(self):
        url = urlparse.urlparse(self.endpoint)
        host, port = url.netloc.split(':',2)
        port = int(port)
        return host, port


    def url(self):
        return self.endpoint


    def urn(self):
        return NSA_PREFIX + self.identity


    def __str__(self):
        return '<NetworkServiceAgent %s>' % self.identity



class Network:

    def __init__(self, name, nsa):
        self.name = name
        self.nsa = nsa
        self.endpoints = []


    def addEndpoint(self, endpoint):
        self.endpoints.append(endpoint)


    def getEndpoint(self, endpoint_name):
        for ep in self.endpoints:
            if ep.endpoint == endpoint_name:
                return ep

        raise error.TopologyError('No such endpoint (%s)' % (endpoint_name))


    def __str__(self):
        return '<Network %s,%i>' % (self.name, len(self.endpoints))



class BandwidthParameters:

    def __init__(self, desired=None, minimum=None, maximum=None):
        self.desired = desired
        self.minimum = minimum
        self.maximum = maximum



class ServiceParameters:

    def __init__(self, start_time, end_time, source_stp, dest_stp, stps=None, directionality='Bidirectional', bandwidth=None):

        # should probably make path object sometime..

        # schedule
        self.start_time = start_time
        self.end_time   = end_time
        # path
        self.source_stp = source_stp
        self.dest_stp   = dest_stp
        self.stps       = stps
        assert directionality in ('Unidirectional', 'Bidirectional')
        self.directionality = directionality

        self.bandwidth = bandwidth or BandwidthParameters()


    def subConnectionClone(self, source_stp, dest_stp):
        return ServiceParameters(self.start_time, self.end_time, source_stp, dest_stp, None, self.directionality, self.bandwidth)


    def protoSP(self):
        return { 'start_time' : self.start_time,
                 'end_time'   : self.end_time,
                 'source_stp' : self.source_stp.urn(),
                 'dest_stp'   : self.dest_stp.urn(),
                 'stps'       : self.stps        }


    def __str__(self):
        return '<ServiceParameters %s>' % str(self.protoSP())

