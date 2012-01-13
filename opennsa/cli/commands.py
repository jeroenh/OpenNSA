# cli commands

from twisted.python import log
from twisted.internet import defer

from opennsa import nsa



@defer.inlineCallbacks
def reserve(client, client_nsa, provider_nsa, source_stp, dest_stp, start_time, end_time, bandwidth, connection_id, global_id):

    source_network, source_port = source_stp.split(':',1)
    dest_network,   dest_port   = dest_stp.split(':', 1)

    r_source_stp = "urn:ogf:network:stp:" + source_stp
    r_dest_stp = "urn:ogf:network:stp:" + dest_stp
    
    bwp = nsa.BandwidthParameters(bandwidth)
    service_params  = nsa.ServiceParameters(start_time, end_time, r_source_stp, r_dest_stp, bandwidth=bwp)

    log.msg("Connection ID: %s" % connection_id)
    log.msg("Global ID: %s" % global_id)

    _ = yield client.reserve(client_nsa, provider_nsa, None, global_id, 'Test Connection', connection_id, service_params)
    print "Reservation created at %s Connection ID: %s" % (provider_nsa, connection_id)


@defer.inlineCallbacks
def provision(client, client_nsa, provider_nsa, connection_id):

    _ = yield client.provision(client_nsa, provider_nsa, None, connection_id)
    log.msg('Connection %s provisioned' % connection_id)


@defer.inlineCallbacks
def release(client, client_nsa, provider_nsa, connection_id):

    _ = yield client.release(client_nsa, provider_nsa, None, connection_id)
    log.msg('Connection %s released' % connection_id)


@defer.inlineCallbacks
def terminate(client, client_nsa, provider_nsa, connection_id):

    _ = yield client.terminate(client_nsa, provider_nsa, None, connection_id)
    log.msg('Connection %s terminated' % connection_id)


@defer.inlineCallbacks
def querysummary(client, client_nsa, provider_nsa, connection_ids, global_reservation_ids):

    qc = yield client.query(client_nsa, provider_nsa, None, "Summary", connection_ids, global_reservation_ids)
    log.msg('Query results:')
    log.msg( str(qc) )


@defer.inlineCallbacks
def querydetails(client, client_nsa, provider_nsa, connection_ids, global_reservation_ids):

    qc = yield client.query(client_nsa, provider_nsa, None, "Details", connection_ids, global_reservation_ids)
    log.msg('Query results:')
    log.msg( str(qc) )

