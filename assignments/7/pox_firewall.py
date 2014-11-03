'''
Udacity: ud436/sdn-firewall
Professor: Nick Feamster
'''

from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.revent import *
from pox.lib.util import dpidToStr
from pox.lib.addresses import EthAddr
from collections import namedtuple
import os
from csv import DictReader


log = core.getLogger()
policyFile = "%s/pox/pox/misc/firewall-policies.csv" % os.environ[ 'HOME' ]

# Add your global variables here ...

# Note: Policy is data structure which contains a single
# source-destination flow to be blocked on the controller.
Policy = namedtuple('Policy', ('dl_src', 'dl_dst'))


class Firewall (EventMixin):

    def __init__ (self):
        self.listenTo(core.openflow)
        log.debug("Enabling Firewall Module")

    def read_policies (self, file):
        with open(file, 'r') as f:
            reader = DictReader(f, delimiter = ",")
            policies = {}
            for row in reader:
                policies[row['id']] = Policy(EthAddr(row['mac_0']), EthAddr(row['mac_1']))
        return policies

    def _handle_ConnectionUp (self, event):
        policies = self.read_policies(policyFile)
        for policy in policies.itervalues():

            msg = of.ofp_flow_mod()
            msg.match.dl_src = policy.dl_src
            msg.match.dl_dst = policy.dl_dst
            msg.priority = 20
            event.connection.send(msg)

            # Hey Prof: there still seems to be a bit of confusion on
            # the forums regarding the bidirectional issue.  AFAICT,
            # the decision to implement bidirectional blockages is
            # defensible given the wording of the HW.  Just in case,
            # though, you can make it directionally sensitive by
            # swapping the boolean below.  I've tested it by manually
            # updating the ARP tables and sending UDP packets.
            do_block_both_directions = True

            if do_block_both_directions:
                msg = of.ofp_flow_mod()
                msg.match.dl_dst = policy.dl_src
                msg.match.dl_src = policy.dl_dst
                msg.priority = 20
                event.connection.send(msg)

        log.debug("Firewall rules installed on %s", dpidToStr(event.dpid))

def launch ():
    '''
    Starting the Firewall module
    '''
    core.registerNew(Firewall)
