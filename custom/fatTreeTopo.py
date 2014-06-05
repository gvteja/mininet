"""Custom topology example

Two directly connected switches plus a host for each switch:

   host --- switch --- switch --- host

Adding the 'topos' dict with a key/value pair to generate our newly defined
topology enables one to pass in '--topo=mytopo' from the command line.
"""

from mininet.topo import Topo

class FatTreeTopo( Topo ):
    "Simple loop example."

    def __init__(self, k=4, **opts):
        """Init.
         k: #of pods"""

        # Initialize topology
        #super(SimpleTopo, self).__init__(**opts)
        #check how ot pass opts and hwat is it used for
        Topo.__init__( self )
        #if k < 3 return error

        self.k = k

        cs = []
        ags = []
        egs = []	
        hosts = []

        # Add hosts and switches and connect hosts to switches
        num_cs = (k ** 2)/4
        num_as = k/2
        num_es = k/2
        num_hosts = k/2
        
        count = 1

        #aggregate and edge switches and hosts
        for i in xrange(1, k + 1): #for each pod
            ags.append([])
            egs.append([])
            hosts.append([])
            for j in xrange(1, num_es + 1):
                s = self.addSwitch('a_' + str(j) + '_' + str(i), dpid=count)
                #s = self.addSwitch(str(count))
                count += 1
                ags[i-1].append(s)
                s = self.addSwitch('e_' + str(j) + '_' + str(i), dpid=count)
                #s = self.addSwitch(str(count))
                count += 1
                egs[i-1].append(s)
                hosts[i-1].append([])
                for m in xrange(1, num_hosts+1):
                    h = self.addHost('h' + str(m) + '_' + str(j) + '_' + str(i))
                    hosts[i-1][j-1].append(h)

        #core swithces
        for i in xrange(1, num_cs + 1):
            s = self.addSwitch('c' + str(i), dpid=count)
            #s = self.addSwitch(str(count))
            count += 1
            cs.append(s)


        # Add links from aggregate to core switches	
        for i in xrange(k):
            tmp_core = 0
            for j in xrange(num_as):
                for l in xrange(num_as):
                    self.addLink(ags[i][j],cs[tmp_core])
                    tmp_core += 1



        # Add Links between aggregate and edge switches
        for i in xrange(k):
            for j in xrange(num_as):
                for m in xrange(num_es):
                    self.addLink(ags[i][j],egs[i][m])
        # Add links between edge switches and host
        for i in xrange(k):
            for j in xrange(num_es):
                for m in xrange(num_hosts):
                    self.addLink(egs[i][j], hosts[i][j][m])

topos = { 'fattreetopo': ( lambda k = 4: FatTreeTopo(k) ) }
