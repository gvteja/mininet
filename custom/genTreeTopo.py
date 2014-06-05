"""Custom topology example

Two directly connected switches plus a host for each switch:

   host --- switch --- switch --- host

Adding the 'topos' dict with a key/value pair to generate our newly defined
topology enables one to pass in '--topo=mytopo' from the command line.
"""

from mininet.topo import Topo

class GenTreeTopo( Topo ):
    "Simple loop example."

    def __init__(self, num_pods = 4, num_core = 2, num_agg = 2, num_edge = 4, num_hosts = 2, **opts):
        """Init.
         k: #of pods"""

        # Initialize topology
        #super(SimpleTopo, self).__init__(**opts)
        #check how ot pass opts and hwat is it used for
        Topo.__init__( self )
        #if k < 3 return error


        cs = []
        ags = []
        egs = []	
        hosts = []

        # Add hosts and switches and connect hosts to switches
        
        count = 1
        num_links = 0

        #aggregate and edge switches and hosts
        for i in xrange(1, num_pods + 1): #for each pod
            ags.append([])
            egs.append([])
            hosts.append([])
            for j in xrange(1, num_agg + 1):
                s = self.addSwitch('a_' + str(j) + '_' + str(i), dpid=count)
                count += 1
                ags[i-1].append(s)
            for j in xrange(1, num_edge + 1):                
                s = self.addSwitch('e_' + str(j) + '_' + str(i), dpid=count)
                count += 1
                egs[i-1].append(s)
                hosts[i-1].append([])
                for m in xrange(1, num_hosts+1):
                    h = self.addHost('h' + str(m) + '_' + str(j) + '_' + str(i))
                    hosts[i-1][j-1].append(h)

        #core swithces
        for i in xrange(1, num_core + 1):
            s = self.addSwitch('c' + str(i), dpid=count)
            count += 1
            cs.append(s)


        # Add links from aggregate to core switches	
        for i in xrange(num_pods):
            for j in xrange(num_agg):
                for k in xrange(num_core):
                    self.addLink(ags[i][j],cs[k])
                    num_links += 1



        # Add Links between aggregate and edge switches
        for i in xrange(num_pods):
            for j in xrange(num_agg):
                for k in xrange(num_edge):
                    self.addLink(ags[i][j],egs[i][k])
                    num_links += 1
                    
                    
        # Add links between edge switches and host
        for i in xrange(num_pods):
            for j in xrange(num_edge):
                for k in xrange(num_hosts):
                    self.addLink(egs[i][j], hosts[i][j][k])

        print 'Number of switch to switch links : {0}'.format(num_links)

topos = { 'gentreetopo': ( lambda num_pods = 4, num_core = 2, num_agg = 2, num_edge = 4, num_hosts = 2 : GenTreeTopo(num_pods,num_core,num_agg,num_edge,num_hosts) ) }
