from twisted.trial import unittest

from opennsa import topologyrdf as topology


TEST_TOPOLOGY_GOLE="../AutoGOLE-Topo-2012-02-11.owl"

# class GenericTopologyTest:
# 
#     def testParseAndFindPath(self):
# 
#         for ts in TEST_PATHS:
#             source_stp = nsa.STP(ts['source_network'], ts['source_endpoint'])
#             dest_stp   = nsa.STP(ts['dest_network'], ts['dest_endpoint'])
# 
#             paths = self.topo.findPaths(source_stp, dest_stp, ts.get('bandwidth'))
#             for path in paths:
#                 self.assertEquals(ts['source_network'],  path.source_stp.network)
#                 self.assertEquals(ts['source_endpoint'], path.source_stp.endpoint)
#                 self.assertEquals(ts['dest_network'],    path.dest_stp.network)
#                 self.assertEquals(ts['dest_endpoint'],   path.dest_stp.endpoint)
# 
#             leps = [ path.endpoint_pairs for path in paths ]
# 
#             self.assertEquals(len(leps), len(ts['paths']), 'Unexpected number of paths')
#             for p in ts['paths']:
#                 self.assertIn(p, leps)
# 


class GOLETopologyTest(unittest.TestCase):

    def setUp(self):
        self.topo = topology.parseGOLETopology(TEST_TOPOLOGY_GOLE)



