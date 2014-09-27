#!/usr/bin/python

import imp
import mininet
import pygraphviz
lst = imp.load_source('lst', 'learning-switch-topo.py')

def graph_network(topo):
    link = mininet.util.custom(mininet.link.TCLink)
    net = mininet.net.Mininet(topo=topo, link=link)
    mininet.util.dumpNetConnections(net)
    nodes = net.controllers + net.switches + net.hosts

    dot = pygraphviz.AGraph()

    edges = []

    for node in nodes:
        if 'c0' == node.name: continue
        dot.add_node(node.name)
        
        for intf in node.intfList():
            if not intf.link: continue
            (a, ai,) = intf.link.intf1.name.split('-')
            (b, bi,) = intf.link.intf2.name.split('-')
            ai = ai.replace('eth', 'p')
            bi = bi.replace('eth', 'p')
            s = [a, b]
            s.sort()
            if s not in edges:
                edges.append(s)
                dot.add_edge(a, b,
                             taillabel=ai+(' '*5),
                             headlabel=bi+(' '*5))

    dot.layout()
    dot.draw('topology.png', prog='dot')


def main():
    print "Starting topology"
    topo = lst.LSTopo()
    graph_network(topo)
    # net = Mininet(topo=topo, link=TCLink, controller=RemoteController, autoSetMacs=True)
    
    # net.start()
    # CLI(net)

if __name__ == '__main__':
    main()
