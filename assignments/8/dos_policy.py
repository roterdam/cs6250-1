# Udacity
# Computer Networking
# Assignment 8: Applications of SDN
#
# Professor: Nick Feamster
# Teaching Assistant: Ben Jones
#
################################################################################
# Resonance Project                                                            #
# Resonance implemented with Pyretic platform                                  #
# author: Hyojoon Kim (joonk@gatech.edu)                                       #
# author: Nick Feamster (feamster@cc.gatech.edu)                               #
# author: Muhammad Shahbaz (muhammad.shahbaz@gatech.edu)                       #
################################################################################

from pyretic.lib.corelib import *
from pyretic.lib.std import *

from ..policies.base_policy import *
from ..drivers.sflow_event import *
from ..globals import *
import ast

import pprint

HOST = 'localhost'
PORT = 8008

class DDoSPolicy(BasePolicy):
    
    def __init__(self, fsm):
        self.fsm = fsm
        
    def allow_policy(self):
        return passthrough
    
    def action(self):

        if self.fsm.trigger.value == 0:
            print 'initializaing policy'
            disallowed = none

            # TODO- set the policy for this application
            #
            # To set the policy for this application, implement the
            # following steps:
            #
            # 1. get the list of hosts in ddos attacker state
            flows = self.fsm.get_flows('ddos-attacker')

            # 2. match the incoming packet's source and destination ip
            #  against that list of hosts (using pyretic predicates
            #  i.e., "match", "modify", and "if_" etc)
            for flow_str in flows:
                flow = ast.literal_eval(flow_str)
                if flow['srcip']:
                    pprint.pprint(flow)
                    print 'Dropping Packets From: %s'%flow['srcip']
                    cur = match(srcip=IPAddr(flow['srcip']))
                    disallowed = disallowed | cur

            pprint.pprint(disallowed)

            # 3. if there is a match apply drop policy, else apply
            #  policy passthrough and return the policy you just
            #  created
            retval = if_(disallowed, drop, passthrough)

            pprint.pprint(retval)

            # Parallel composition- return the policy that you created
            return retval

        else:
            print 'event was triggered!!'
            return self.turn_off_module(self.fsm.comp.value)
