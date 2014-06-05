import random
from threading import Timer
from time import sleep, ctime, time

results = []

def genTraffic(hosts, parsePingOutput, gap=0.01, timeout=1, count=3, file_name = None):
    "pings 2 random hosts every gap s until timeout. if gap is 0, pump out as much traffic as possible in that timeout. if timeout is 0, never stop pumping"
    num_pings = 0
    num_op = 0
    pkts_sent = 0
    pkts_recvd = 0
    rtt_total = 0.0
    num_hosts = len(hosts)
    current_op = ['' for i in range(num_hosts)]
    indices = range(num_hosts)
    cont = [True]
    isGap = gap!=0
    random.seed()
    p = False
    if file_name == '.':
        p = True
        file_name = None
    if file_name:
        f = open(file_name,'w')
    def stopTraffic():
        cont[0] = False
    if timeout<0:
        pkts_to_send = -timeout*1000
        pkts_commited = 0
    if(timeout > 0):
        Timer(timeout,stopTraffic).start()
    s = 'Start time : {0}'.format(ctime())
    if p:
        print s
    elif file_name:
        f.write(s)

    start_time = int(time())
    while cont[0]:
        index = random.sample(indices, 2)
        nodes = [ hosts[i] for i in index ]
        i = index[0]
        if(nodes[0].waiting):
            op = nodes[0].monitor(0)
            current_op[i] += op
            if not nodes[0].waiting:
                num_op += 1
                op_tuple = parsePingOutput(current_op[i])
                sent, received, rttmin, rttavg, rttmax, rttdev = op_tuple
                pkts_sent += sent
                pkts_recvd += received
                rtt_total += rttavg
                res = 'host : {0} cmd : {1} output :\n--@--\n{2}\n--@--\n'.format( nodes[0].name, nodes[0].lastCmd, current_op[i].strip() )
                if op_tuple == (1,0,0,0,0,0):
                    if file_name:
                        f.write('\nERROR ERROR\nDetails : \n' + res)
                    elif p:
                        print 'The parse error was for the following : ' + res 
                elif received < sent:
                    if file_name:
                        f.write('\nPackets Dropped!\n Details : \n' + res)
                    elif p:
                        print 'Packets Dropped! Details : ' + res
                else:
                    if file_name:
                        f.write(res+'\n')
                    elif p:
                        print res
                if (timeout < 0) and (pkts_sent >= pkts_to_send):
                    cont[0] = False
                current_op[i] = ''
            else:
                continue
        #dont think i should check for 2nd host running a cmd. coz we sendin only on 1st host
        res = '| {0} --> {1} |'.format(nodes[0].name, nodes[1].name)
        if file_name:
            f.write(res+'\n')
        elif p:
            print res
        if count < 1:#non stop ping
            nodes[0].sendCmd( 'ping -w %s %s' % ( (timeout - int(time()) + start_time), nodes[1].IP() ))
        else:
            nodes[0].sendCmd( 'ping -c %s %s' % (count, nodes[1].IP() ))
            if timeout < 0:
                pkts_commited += count
                if pkts_commited >= pkts_to_send:
                    cont[0] = False
        num_pings += 1
        if isGap:
            sleep(gap)
    #here traverse through all the hosts once and get the ops. 
    for i in indices:
        host = hosts[i]
        if host.waiting:
            op = current_op[i] + host.waitOutput()#this is a bust wait
            num_op += 1
            op_tuple = parsePingOutput(op)
            sent, received, rttmin, rttavg, rttmax, rttdev = op_tuple
            pkts_sent += sent
            pkts_recvd += received
            rtt_total += rttavg
            res = 'host : {0} cmd : {1} output :\n--@--\n{2}\n--@--\n'.format( host.name, host.lastCmd, op.strip() )
            if file_name:
                if op_tuple == (1,0,0,0,0,0):
                    f.write('\nERROR ERROR\n')
                f.write(res+'\n')
            elif p:
                print res
    s = 'End time : {0}'.format(ctime())
    if file_name:
        f.write(s)
    elif p:
        print s
    if num_op == 0:
        res = 'No op parsed. Num ping cmds sent : {0}'.format(num_pings)
    else:
        res = 'Total ping cmds:{0}, op parsed:{1}, pkts sent:{2}, pkts recvd:{3}, avg rtt:{4}'.format(num_pings, num_op, pkts_sent, pkts_recvd, (rtt_total/num_op) )
    print res
    if file_name:
        f.write(res)
    if file_name:
        f.close()
    return res
