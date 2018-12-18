from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from mininet.util import dumpNodeConnections
import os
class LinuxRouter( Node ):
    "A Node with IP forwarding enabled."

    def config( self, **params ):
        super( LinuxRouter, self).config( **params )
        # Enable forwarding on the router
        self.cmd( 'sysctl net.ipv4.ip_forward=1' )

    def terminate( self ):
        self.cmd( 'sysctl net.ipv4.ip_forward=0' )
        super( LinuxRouter, self ).terminate()

class NetworkTopo( Topo ):
    "A LinuxRouter connecting three IP subnets"

    def build( self, **_opts ):
        s1, s2, s3 = [ self.addSwitch( s ) for s in ( 's1', 's2', 's3' ) ]

        r1 = self.addNode( 'r1', cls=LinuxRouter, ip="192.168.1.1/24" )
        self.addLink( s1, r1, intfName2='r1-eth1', params2={ 'ip' : "192.168.1.1/24" } )  # for clarity
        h1 = self.addHost( 'h1', ip='192.168.1.100/24', defaultRoute='via 192.168.1.1' )
        self.addLink(s1,h1)

        r2 = self.addNode( 'r2', cls=LinuxRouter, ip="192.168.2.1/24" )
        self.addLink( s2, r2, intfName2='r2-eth1', params2={ 'ip' : "192.168.2.1/24" } )  # for clarity
        h2 = self.addHost( 'h2', ip='192.168.2.100/24', defaultRoute='via 192.168.2.1' )
        self.addLink(s2,h2)

#        self.addLink(r1, r2, intfName1='r1-eth2', intfName2='r2-eth2')
        
# self.addLink( s2, router, intfName2='r0-eth2',
       #               params2={ 'ip' : '172.16.0.1/12' } )
       # self.addLink( s3, router, intfName2='r0-eth3',
       #               params2={ 'ip' : '10.0.0.1/8' } )

        
#h2 = self.addHost( 'h2', ip='172.16.0.100/12',
        #                   defaultRoute='via 172.16.0.1' )
        #h3 = self.addHost( 'h3', ip='10.0.0.100/8',
        #                   defaultRoute='via 10.0.0.1' )

        #for h, s in [ (h1, s1), (h2, s2), (h3, s3) ]:
        #    self.addLink( h, s )
        #h1 = self.addHost('h1', ip='10.0.0.10/24', defaultRoute='via 10.0.0.2')
        #h2 = self.addHost('h2', ip='10.0.2.10/24', defaultRoute='via 10.0.3.1')

        #r1 = self.addHost('r1', ip='10.0.3.0/24')#, defaultRoute='via 10.0.1.2')
        #r2 = self.addHost('r2', ip='10.0.3.0/24')#, defaultRoute='via 10.0.2.2')
        #self.addLink(r1, r2, intfName1='r1-eth1', intfName2='r2-eth2')

        
        #self.addLink(h1,r1, intfName1='h1-eth0', intfName2='r1-eth0')
        #self.addLink(h2,r2, intfName1='h2-eth0', intfName2='r2-eth1')
        
        
        #defaultIPR1 = '192.168.1.1/24'  # IP address for r0-eth1
        #r1 = self.addNode( 'r1', cls=LinuxRouter, ip=defaultIPR1 )
        #h1 = self.addHost( 'h1', ip='192.168.1.100/24', defaultRoute='via 192.168.1.1' )
        #self.addLink(h1, r1, intfName2='r1-eth1',params2={'ip':defaultIPR1})
        
        #defaultIPR2 = '192.168.2.1/24'
        #r2 = self.addNode( 'r2', cls=LinuxRouter, ip=defaultIPR2 )
        #h2 = self.addHost( 'h2', ip='192.168.2.100/24', defaultRoute='via 192.168.2.1' )
        #self.addLink(h2, r2, intfName2='r2-eth1',params2={'ip':defaultIPR2})
        
        #self.addLink(r1,r2, intfName2='r2-eth2',params2={'ip':defaultIPR2})
        #self.addLink(r1, r2, intfName2='r1-eth2')
        #h2 = self.addHost( 'h2', ip='172.16.0.100/12',
        #                   defaultRoute='via 172.16.0.1' )
        #h3 = self.addHost( 'h3', ip='10.0.0.100/8',
        #                   defaultRoute='via 10.0.0.1' )

        #for h, s in [ (h1, s1), (h2, s2), (h3, s3) ]:
        #    self.addLink( h, s )

def waitForEnter():
    raw_input("Press enter to continue when you are ready...")
def startWireshark():
    os.system("sudo wireshark&")
    print "Please allow Wireshark to run. Please dismiss any and all pop ups that limit the application from running." 
    waitForEnter()
    
    print "Please enter 'of' in the filter field. Then click 'apply'"
    waitForEnter()
    
    print "In Wireshark, click Capture, then Interfaces, then select Start on the loopback interface (lo)"
    waitForEnter()

def run():
    "Test linux router"
    topo = NetworkTopo()
    net = Mininet( topo=topo )  # controller is used by s1-s3
    net.start()
    info( '*** Routing Table on Router:\n' )
    info( net[ 'r1' ].cmd( 'route' ) )
    #info( net['r1'].cmd('ifconfig r1-eth1 10.0.2.1/24'))
    info( net[ 'r2' ].cmd( 'route' ) )
    #startWireshark()
    net.pingAll()
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    run()
