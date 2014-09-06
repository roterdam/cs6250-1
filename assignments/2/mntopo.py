#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.util import custom
from mininet.net import Mininet

import mininet
from mininet.node import CPULimitedHost
from graphviz import Graph
import tempfile
import os

def graph_network(topo):
    # naiive implementation -- don't care
    host = custom(CPULimitedHost, cpu=.15)
    link = custom(TCLink, max_queue_size=200)
    net = Mininet(topo=topo, host=host, link=link)
    mininet.util.dumpNetConnections(net)
    nodes = net.controllers + net.switches + net.hosts

    dot = Graph(comment='Your Assignment 2 Topology')

    edges = []

    for node in nodes:
        if 'c0' == node.name: continue
        dot.node(node.name)
        
        for intf in node.intfList():
            if not intf.link: continue
            a = intf.link.intf1.name.split('-')[0]
            b = intf.link.intf2.name.split('-')[0]
            s = [a, b]
            s.sort()
            if s not in edges:
                edges.append(s)
                dot.edge(a, b)

    t = tempfile.NamedTemporaryFile(delete=False)
    t.write(dot.source)
    t.close()
    print dot.render(t.name)
    os.unlink(t.name)

# Topology to be instantiated in Mininet
class MNTopo(Topo):
    "Mininet test topology"

    def __init__(self, cpu=.1, max_queue_size=None, **params):

        # Initialize topo
        Topo.__init__(self, **params)

        # Host and link configuration
        hostConfig = {'cpu': cpu}
        linkConfig = {'bw': 50,
                      'delay': '10ms',
                      'loss': 0,
                      'max_queue_size': max_queue_size }

        # Hosts and switches
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        sender = self.addHost('sender', **hostConfig)
        receiver = self.addHost('receiver', **hostConfig)

        # Wire receiver
        self.addLink(receiver, s2, **linkConfig)

        # Connect the dots...I mean switches
        self.addLink(s2, s1, **linkConfig)

        # Wire sender
        self.addLink(sender, s1, **linkConfig)


if __name__ == '__main__':
    topo = MNTopo()
    graph_network(topo)
