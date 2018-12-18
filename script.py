from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.util import irange

class LinearTopo( Topo ):
    "Linear topology of k switches, with n hosts per switch."

    def build( self, k=2, n=1, **_opts):
        """k: number of switches
           n: number of hosts per switch"""
        self.k = k
        self.n = n

        if n == 1:
            genHostName = lambda i, j: 'h%s' % i
        else:
            genHostName = lambda i, j: 'h%ss%d' % ( j, i )

        lastSwitch = None
        second = None
        for i in irange( 1, k ):
            # Add switch
            switch = self.addSwitch( 's%s' % i )
            if i==2:
                second = switch
            # Add hosts to switch
            for j in irange( 1, n ):
                host = self.addHost( genHostName( i, j ) )
                self.addLink( host, switch )
            # Connect switch to previous
            if lastSwitch:
                self.addLink( switch, lastSwitch )
            lastSwitch = switch
        #if second is not None and second is not lastSwitch:
        #    self.addLink(lastSwitch, second)

class DynamicRoutingTest(Topo):
    def build( self, **_opts):
        #test = self.addHost('x')
        hA = self.addHost('h1')
        hB = self.addHost('h2')
        hC = self.addHost('h3')
        hD = self.addHost('h4')
        hE = self.addHost('h5')

        A = self.addSwitch('s1')
        B = self.addSwitch('s2')
        C = self.addSwitch('s3')
        D = self.addSwitch('s4')
        E = self.addSwitch('s5')
        
        self.addLink(hA, A)
        self.addLink(hB, B)
        self.addLink(hC, C)
        self.addLink(hD, D)
        self.addLink(hE, E)

        self.addLink(A,B)
        self.addLink(B,C)
        self.addLink(C,D)
        self.addLink(D,E)
        self.addLink(E,B)

TOPOS = {'LinearTopo':(lambda:LinearTopo()),
         'DynamicRoutingTest':(lambda:DynamicRoutingTest())}
def simpleTest():
        "Create and test a simple network"
        topo = LinearTopo(k=5,n=1) #DynamicRoutingTest() #LinearTopo(k=4,n=8)
        net = Mininet(topo)
        net.start()
        print "Dumping host connections"
        dumpNodeConnections(net.hosts)
        print "Testing network connectivity"
        net.pingAll()
        net.stop()

if __name__ == '__main__':
        # Tell mininet to print useful information
        setLogLevel('info')
        simpleTest()
