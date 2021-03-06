# Secondary Repository for OpenNSA #

The primary repository for OpenNSA is available at http://git.nordu.net/?p=opennsa.git;a=summary and git://git.nordu.net/opennsa.git .

This secondary repository for OpenNSA allows users to submit issues, follow the development online, and to push patches (the above is a read-only repository).
It tries to follow development from the primary repository, but the github repository is not guaranteed to be up to date.


# OpenNSA #

OpenNSA is an implementation of the Network Service Interface (NSI).

NSI (Network Service Interface) is (or should be) a protocol agnostic interface
for provisioning network links, i.e., providing networking as a service.

There are several documents concerning NSI. See the OGF work group page for the
latest revisions. http://forge.gridforum.org/sf/projects/nsi-wg

OpenNSA consists of several modules for various functionality. These include
topology database and parser, protocol handlers, and the core agent itself.

OpenNSA is currently in a state of heavy prototyping and nothing is set in
stone, and there are probably more temporary constructions in the code than
final.

Requirements:

* Python 2.6 or newer (Python 3 will not work)

* Twisted, http://twistedmatrix.com/trac/

* SUDS, https://github.com/htj/suds-htj
  The SUDS homepage is https://fedorahosted.org/suds/, but is unmaintained.
  The last SUDS release (0.4) has several bugs regarding namespaces, and
  timezone issues and will not work with OpenNSA. The version from github
  is hence recommended.

Python and Twisted should be included in the package system in most recent
Linux distributions.

If you use a backend which uses SSH (JunOS, Force10), there is a patch to
remove some of the log statements in the Twisted SSH module, which is rather
noisy. This makes the log a lot easier to read.


Command line tool:

Start test service:
twistd -noy opennsa.tac

Make a reservation:
./onsa reserve -u http://localhost:9080/NSI/services/ConnectionService -p OpenNSA-HTJClient -r Aruba -s Aruba:A1 -d Aruba:A4

Do a ./onsa --help for more information.


License: 3-clause BSD. See LICENSE for more details.

Developer contact: htj <at> nordu.net
Copyright: NORDUnet (2011)

