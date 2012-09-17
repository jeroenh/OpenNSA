"""
OpenNSA RDF Shortestpath finder based on Dijkstra

Author: Jeroen van der Ham <vdham@uva.nl

Copyright: University of Amsterdam (2012)
"""
import heapq
import rdflib

DTOX_NS = rdflib.namespace.Namespace('http://www.glif.is/working-groups/tech/dtox#')

# To Infinity and Beyond!
# (Actually can't think of another way to define infinity on a computer.)
infinity = "infinity"

class Dijkstra(object):
    def __init__(self, graph):
        self.graph = graph

    def getNeighbors(self, cp, path=None):
        network = self.graph.value(predicate=DTOX_NS.hasSTP,object=rdflib.URIRef(cp))
        if len(path)>1 and self.graph.value(predicate=DTOX_NS.hasSTP,object=rdflib.URIRef(path[-2]))==network:
            # we're coming from the domain, going to outside, so only return connectedTo
            conn = self.graph.value(subject=rdflib.URIRef(cp),predicate=DTOX_NS.connectedTo)
            if conn:
                return [str(conn)]
            else:
                return []
        # We're looking for intra-domain path:
        stps = set(str(x) for x in self.graph.objects(subject=network,predicate=DTOX_NS.hasSTP))
        # We're not a neighbor of ourselves
        stps.remove(str(cp))
        return stps
    def findShortestPath(self, src=None, dst=None, bandwidth=None):
        q = [(0, src, ())]
        visited = set()
        while q:
            (cost, v1, path) = heapq.heappop(q)
            if v1 not in visited:
                visited.add(v1)
                path += (v1,)
                if v1 == dst:
                    return list(path)
                for v2 in self.getNeighbors(v1):
                    if v2 not in visited:
                        m = self.getMetric(v1,v2,bandwidth)
                        if not m == infinity:
                            heapq.heappush(q, (cost+m, v2, path))
        return None
    def findShortestPaths(self, src=None, dst=None, bandwidth=None):
        q = [(0, src, ())]
        visited = set()
        results = set()
        while q:
            (cost, v1, path) = heapq.heappop(q)
            path += (v1,)
            if v1 == dst:
                results.add(path)
                continue
            if v1 not in visited:
                visited.add(v1)
                for v2 in self.getNeighbors(v1,path):
                    if v2 not in visited:
                        m = self.getMetric(v1,v2,bandwidth)
                        if not m == infinity:
                            heapq.heappush(q, (cost+m, v2, path))
        return results
    def getMetric(self, source, target, bandwidth=None):
        # TODO: All kinds of funky metric magic possibly taking bandwidth into account
        # Possible to return "infinity" if you have no bandwidth for example.
        return 1