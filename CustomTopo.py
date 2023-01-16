#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import irange,dumpNodeConnections
from mininet.log import setLogLevel

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
    print ("1. --Задаем параметры")
    linkopts1 = {'bw':50, 'delay':'5ms'}
    linkopts2 = {'bw':30, 'delay':'10ms'}
    linkopts3 = {'bw':10, 'delay':'15ms'}
    print ("2. --Реализуем нашу топологию с праметрами")
    topo = CustomTopo(linkopts1, linkopts2, linkopts3, fanout=2)

    print ("3. --Создаем сеть из нашей топологии ")
    net = Mininet(topo=topo, host=CPULimitedHost, link=TCLink)
    net.start()
    dumpNodeConnections(net.hosts)
    print ("4. --Тестируем сеть ")
    net.pingAll()

    print ("5. --Останавливаем")
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    perfTest()                    
