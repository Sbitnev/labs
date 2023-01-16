#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import irange,dumpNodeConnections
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel


class CustomTopo(Topo):
    "Simple Data Center Topology"

    "linkopts - (1:core, 2:aggregation, 3: edge) parameters"
    "fanout - number of child switch per parent switch"
    def __init__(self, linkopts1, linkopts2, linkopts3, fanout=2, **opts):
        # Initialize topology and default options
        Topo.__init__(self, **opts)
        # Add your logic here ...
        core = self.addSwitch('core_cs1')

        for a in range(fanout):
            aggr = self.addSwitch('a%s' % (a + 1))
            self.addLink(aggr, core, **linkopts1)

            for e in range(fanout):
                edge = self.addSwitch('e%s' % ((a * fanout + e) + 1))
                self.addLink(edge, aggr, **linkopts2)

                for h in range(fanout):
                    host = self.addHost('h%s' % (((a * fanout + e) * fanout + h) + 1))
                    self.addLink(host, edge, **linkopts3)

def simple_test():
    print("1.")
    linkopts1 = {'bw': 50, 'delay': '5ms'}
    linkopts2 = {'bw': 30, 'delay': '10ms'}
    linkopts3 = {'bw': 10, 'delay': '15ms'}
    print("2.")
    topo = CustomTopo(linkopts1, linkopts2, linkopts3, fanout=2)

    print("3.")
    net = Mininet(topo=topo, host=CPULimitedHost, link=TCLink)
    net.start()
    dumpNodeConnections(net.hosts)
    print("4.")
    net.pingAll()

    print("5.")
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')


