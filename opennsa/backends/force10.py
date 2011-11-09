"""
NRM backend for Force10 switche

Authors: Ralph Koning <R.Koning@uva.nl>
         Henrik Thostrup Jensen <htj@nordu.net>
Copyright: NORDUnet (2011)
"""

import datetime
import os

from twisted.python import log
from twisted.internet import reactor as ti_reactor
from twisted.internet import defer as ti_defer
from twisted.internet import task as ti_task

from zope.interface import implements

from opennsa import nsa, error, state as state, interface as nsainterface
from opennsa.backends.common.calendar import ReservationCalendar
from opennsa.backends.sshexpect import SSHExpect
from opennsa.backends.f10_settings import *
from ConfigParser import ConfigParser


#   seems to be bug in calendar function..
#
#    # port temporal availability


def deferTaskFailed(err):
    if err.check(ti_defer.CancelledError):
        pass # this just means that the ti_task was cancelled
    else:
        log.err(err)

class Force10Proxy:
    """ This class keeps track of the force10 connection itself.

        This class uses the SSHExpect library to maintain a ssh
        connection to the Force10 switch. And exposes a basic
        set of functionality we need to implement the higher
        level functions."""

    def __init__(self):
        try:
            cfg = ConfigParser()
            cfg.read("%s/.opennsa-force10.cfg" % os.getenv("HOME"))
            self.user = cfg.get("force10", "username")
            self.pwd = cfg.get("force10", "password")
            self.host = cfg.get("force10", "hostname")
            self.ports = cfg.get("force10", "ports").lower().split(",")
            self.name = cfg.get("force10", "name")
            self.vlans = cfg.get("force10", "vlans").split(",")
        except Exception as e:
            raise e
            print "config not found"
            #from config file
            self.user=""
            self.pwd=""
            self.host=""
            self.ports=[]
            self.vlans=[]
            self.name="Force10"
        print self.name
        print self.vlans
        print self.ports
        self.cli=SSHExpect()
        self.cli.shellcmd=""
        self._switchPrompt()

    def _switchPrompt(self, style="default", vid="99999"):
        prompts = { "default" : "%s#" % self.name,
                    "conf"    : "%s\(conf\)#" % self.name,
                    "vlan"    : "%s\(conf-if-vl-%s\)#" % (self.name, vid),
                  }
        self.cli.prompt=prompts[style]

    def connect(self):
        """Establishes the ssh session to the Force10 switch"""
        s=self.cli
        s.connect(self.user, self.pwd, self.host, "-1 -t")
        s.waitPrompt()
        s.sendline("terminal length 0")
        s.waitPrompt()

    def disconnect(self):
        """Closes the ssh session to the Force10 switch"""
        s=self.cli
        s.logout()

    def release(self, vid):
        """Releases the connection specified identified by 'vid'

        On the switch we use vlans to create point-to-point connections,
        this means that vlans are unique for a connection on the f10.
        """
        if vid not in self.vlans:
            raise error.InvalidRequestError('Specified vlan not in the allowed vlans list')
        s=self.cli
        s.sendline("configure")
        self._switchPrompt("conf")
        s.waitPrompt()
        s.sendline("no interface vlan %s" % vid)
        s.sendline("end")
        self._switchPrompt()

    def provision(self, vid, src, dst, desc):
        """Provisions connections to force10

        It basically creates a vlan and adds two tagged ports in to create
        the connection.
        """
        if vid not in self.vlans:
            raise error.InvalidRequestError('Specified vlan not in the allowed vlans list')
        if src not in self.ports:
            raise error.InvalidRequestError('Source port not in the allowed ports list')
        if dst not in self.ports:
            raise error.InvalidRequestError('Destination port not in the allowed ports list')
        s=self.cli
        self._switchPrompt("conf")
        s.sendline("configure")
        s.waitPrompt()
        s.sendline("interface vlan %s" % vid)
        self._switchPrompt("vlan", vid)
        s.waitPrompt()
        s.sendline("name %s" % desc)
        s.sendline("description %s" % desc)
        s.sendline("no shut")
        s.sendline("tagged %s" % src)
        s.sendline("tagged %s" % dst)
        s.waitPrompt()
        s.sendline("end")
        self._switchPrompt("conf")

class Force10Backend:
    """The NSIBackendInterface for a Force10 switch""" 

    implements(nsainterface.NSIBackendInterface)

    def __init__(self, network_name=None):
        self.network_name = network_name
        self.connections = []
        self.cli = Force10Proxy()
        self.cli.connect()
        self.cal=ReservationCalendar()

    def createConnection(self, source_port, dest_port, service_parameters):
        """ Creates a connection object for the given ports and make sure 
            we can keep track of them
        """
        try:
            self._reserve(source_port, dest_port, service_parameters.start_time, service_parameters.end_time)
        except Exception as e: 
            raise e
        else:
            ac = Force10Connection(self.cli, source_port, dest_port, service_parameters, self.network_name, self.cal)
            self.connections.append(ac)
            return ac
        return None

    def _reserve (self, source_port, dest_port, res_start, res_end):
        """ Creates a reservation in the calendar, after making sure if the
            timeslot is available.
        """
        if res_start in [ None, '' ] or res_end in [ None, '' ]:
            raise error.InvalidRequestError('Reservation must specify start and end time (was either None or '')')
        try:
            self.cal.checkReservation(source_port, res_start, res_end)
        except error.InvalidRequestError as e:
            raise e
            return ti_defer.fail(error.ReserveError(e.message))
        else:
            self.cal.addConnection(source_port, res_start, res_end)
        try:
            self.cal.checkReservation(dest_port, res_start, res_end)
        except error.InvalidRequestError as e:
            raise e
            return ti_defer.fail(error.ReserveError(e.message))
        else:
            self.cal.addConnection(dest_port, res_start, res_end)

class Force10Connection:
    """ A Force10 connection Object, this keeps track of a single
        connection on the Force10
    """

    def __init__(self, cli, source_port, dest_port, service_parameters, network_name, calendar):
        self.source_port = source_port
        self.dest_port  = dest_port
        self.service_parameters = service_parameters
        self.network_name = network_name
        self.cal = calendar
        self.cli=cli
        self.state = state.ConnectionState()
        self.auto_transition_deferred = None

    def stps(self):
        """ This lists the avaliable STPs"""
        return nsa.STP(self.network_name, self.source_port), nsa.STP(self.network_name, self.dest_port)

    def deSchedule(self):
        """ This removes a previously scheduled function call from self.auto_transition_deferred """

        if self.auto_transition_deferred:
            log.msg('Cancelling automatic state transition.  CID %s' % id(self), system='Force10Backend Network %s' % self.network_name)
            self.auto_transition_deferred.cancel()
            self.auto_transition_deferred = None

    def _parse_port_urn(self, urn):
        """  This parses the urn and translates it into something 
             understandable by the Force10

             urn:ogf:network:uvalight.nl:force10:gi0-0:1780
             ^^^^^^^^^^^^^^^ ^^^^^^^^^^^ ^^^^^^^ ^^^^^ ^^^^
                  prefix        domain     host  port  vlan
        """
        parts = urn.split(":")
        if (len(parts) < 7) or (":".join(parts[0:3]) != "urn:ogf:network"):
            raise error.InvalidRequestError('urn %s is not correctly formatted' % dest_port)
        parts = parts[3:]
        portname=parts[2].split("-")
        return { "hostname" : ".".join([parts[1],parts[0]]), 
                 "vlan"     : ""+parts[3] , 
                 "port"     : "%s %s" % (portname[0], "/".join(portname[1:]))
               }

    def reserve(self):
        """This should make a reservation but force10 doesn't do
           reservations. So it basically does nothing. """
        log.msg('RESERVE. CID: %s, Ports: %s -> %s' % (id(self), self.source_port, self.dest_port), system='Force10Backend Network %s' % self.network_name)
        try:
            self.state.switchState(state.RESERVING)
            self.state.switchState(state.RESERVED)
        except error.StateTransitionError:
            return ti_defer.fail(error.ReserveError('Cannot reserve connection in state %s' % self.state()))
        # This should be removed, I scheduled some automatic provisioning for testing.
        ti_task.deferLater(ti_reactor, 5, self.provision)
        return ti_defer.succeed(self)

    def provision(self):
        """ This function handles the provisioning """

        def _total_seconds(td):
            """ total_seconds() is only available from python 2.7 so we use this """
            delta_seconds = (td.microseconds + (td.seconds + td.days * 24 * 3600) * 10**6) / 10**6.0
            delta_seconds = max(delta_seconds, 0) # if we dt_now during calculation
            return delta_seconds

        def doProvision():
            log.msg('PROVISION. CID: %s' % id(self), system='Force10Backend Network %s' % self.network_name)
            self.deSchedule()
            try:
                self.state.switchState(state.PROVISIONING)
                src=self._parse_port_urn(self.source_port)
                dst=self._parse_port_urn(self.dest_port)
                self.cli.release(src['vlan'])
                self.cli.provision(src['vlan'], src['port'], dst['port'], "autogole opennsa")
            except error.StateTransitionError:
                return ti_defer.fail(error.ProvisionError('Cannot provision connection in state %s' % self.state()))
            stop_delta_seconds = _total_seconds(self.service_parameters.end_time - datetime.datetime.utcnow())
            self.auto_transition_deferred = ti_task.deferLater(ti_reactor, stop_delta_seconds, self.release)
            self.auto_transition_deferred.addErrback(deferTaskFailed)
            self.state.switchState(state.PROVISIONED)

        src=self._parse_port_urn(self.source_port)
        dst=self._parse_port_urn(self.dest_port)
        if src['hostname'] != dst['hostname']: 
            raise error.InvalidRequestError('src and dest hostname are different while controlling single device ')
        if src['vlan'] != dst['vlan']: 
            raise error.InvalidRequestError('src and dest vlan are different and switch doesn not support retagging')
        dt_now = datetime.datetime.utcnow()

        if self.service_parameters.end_time <= dt_now:
            return ti_defer.fail(error.ProvisionError('Cannot provision connection after end time (end time: %s, current time: %s).' % (self.service_parameters.end_time, dt_now)))
        else:
            start_delta_seconds = _total_seconds(self.service_parameters.start_time - dt_now)
            self.auto_transition_deferred = ti_task.deferLater(ti_reactor, start_delta_seconds, doProvision)
            self.auto_transition_deferred.addErrback(deferTaskFailed)
            self.state.switchState(state.AUTO_PROVISION)
            log.msg('Connection %s scheduled for auto-provision in %i seconds ' % (id(self), start_delta_seconds), system='Force10Backend Network %s' % self.network_name)

        return ti_defer.succeed(self)

    def release(self):
        """Releases connection (on switch) but keeps the reservation"""
        log.msg('RELEASE. CID: %s' % id(self), system='Force10Backend Network %s' % self.network_name)
        self.deSchedule()
        try:
            self.state.switchState(state.RELEASING)
            src=self._parse_port_urn(self.source_port)
            dst=self._parse_port_urn(self.dest_port)
            self.cli.release(src['vlan'])
        except error.StateTransitionError, e:
            log.msg('Release error: ' + str(e), system='Force10Backend Network %s' % self.network_name)
            return ti_defer.fail(e)
        self.state.switchState(state.SCHEDULED)
        # This should be removed, I scheduled some automatic termination for testing.
        ti_task.deferLater(ti_reactor, 5, self.terminate)
        return ti_defer.succeed(self)

    def terminate(self):
        """Releases connection (on switch) and its reservation"""
        log.msg('TERMINATE. CID : %s' % id(self), system='Force10Backend Network %s' % self.network_name)
        self.state.switchState(state.TERMINATING)
        src=self._parse_port_urn(self.source_port)
        self.cli.release(src['vlan'])
        self.deSchedule()
        self.cal.removeConnection(self.source_port, self.service_parameters.start_time, self.service_parameters.end_time)
        self.cal.removeConnection(self.dest_port, self.service_parameters.start_time, self.service_parameters.end_time)
        self.state.switchState(state.TERMINATED)
        return ti_defer.succeed(self)

    def query(self, query_filter):
        pass
