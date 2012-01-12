"""
OpenNSA RDF Shortestpath finder based on Dijkstra

Author: Jeroen van der Ham <vdham@uva.nl

Copyright: University of Amsterdam (2012)
"""
import heapq
import rdflib

DTOX_NS = rdflib.namespace.Namespace('http://www.glif.is/working-groups/tech/dtox#')

class Dijkstra(object):
    def __init__(self, graph):
        self.graph = graph

    def getNeighbors(self, cp):
        network = self.graph.value(predicate=DTOX_NS.hasSTP,object=cp.uri)
        stps = [str(x) for x in self.graph.objects(subject=network,predicate=DTOX_NSA.hasSTP)]
        connected = str(self.graph.value(subject=cp.uri,predicate=DTOX_NS.connectedTo))
        stps.append(connected)
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
                    print list(path)
                    return list(path)
                for v2 in self.getNeighbors(v1):
                    if v2 not in visited:
                        m = self.getMetric(v1,v2,bandwidth)
                        if not m == infinity:
                            heapq.heappush(q, (cost+m, v2, path))
        return None
