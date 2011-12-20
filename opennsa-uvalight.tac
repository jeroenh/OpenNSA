#!/usr/bin/env python # syntax highlightning

import os, sys,time

from twisted.python.log import ILogObserver
from twisted.application import internet, service

from opennsa import setup, logging
from opennsa.backends import force10


DEBUG = False

HOST = 'nsa.uvalight.nl'
PORT = 9080

TOPOFILE = 'SC2011-Topo-v5f.owl'

WSDL_DIR = os.path.join(os.getcwd(), 'wsdl')
NETWORK_NAME = 'uvalight.ets'

application = service.Application("OpenNSA")
application.setComponent(ILogObserver, logging.DebugLogObserver(sys.stdout, DEBUG).emit)
time.sleep(1)
backend = force10.Force10Backend(NETWORK_NAME)
factory = setup.createService(NETWORK_NAME, open(TOPOFILE), backend, HOST, PORT, WSDL_DIR)


internet.TCPServer(PORT, factory, interface='localhost').setServiceParent(application)
