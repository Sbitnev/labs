#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import irange,dumpNodeConnections
from mininet.log import 

class CustomTopo(Topo):
    "Simple Data Center Topology"

    "linkopts - (1:core, 2:aggregation, 3: edge) parameters"
    "fanout - number of child switch per parent switch"
    def __init__(self, linkopts1, linkopts2, linkopts3, fanout=2, **opts):
        # Initialize topology and default options
        Topo.__init__(self, **opts)
        
        # Add your logic here ...
        # Create the root switch
        rootSwitch = self.addSwitch('s1')
     
        # Create the child switches
        childSwitches = [self.addSwitch('s{}'.format(i)) for i in irange(2, fanout+1)]
    
        # Create the hosts
        hosts = [self.addHost('h{}'.format(i)) for i in irange(1, fanout**2+1)]
    
        # Create links between the root switch and child switches
        for s in childSwitches:
            self.addLink(rootSwitch, s, **linkopts)
    
        # Create links between the child switches and hosts
        for s in childSwitches:
            for h in hosts:
                self.addLink(s, h, **linkopts)
        
def perfTest():
    topo = CustomTopo(linkopts={'bw':10,'delay':'5ms','loss':1,'max_queue_size':1000},fanout=3)
    net = Mininet(topo=topo, host=CPULimitedHost, link=TCLink)
    net.start()
    dumpNodeConnections(net.hosts)
    net.pingAll()
    net.iperf()
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    perfTest()                    
