#! /usr/bin/python3

"""Legacy Network for CST311 Programming Assignment 4"""
__author__ = "Team 9"
__credits__ = [
    "Nima Mahanloo",
    "Dawn Petersen",
    "Armondo Lopez",
    "Christopher Loi"
]

from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from subprocess import call
from cert_keygen import create_cert
from mininet.term import makeTerm
from time import sleep

def myNetwork():
    cn_webserver = input("Enter the CN for the web server> ")
    cn_chatserver = input("Enter the CN for the chat server> ")
    create_cert(cn_webserver, '10.0.3.3')
    create_cert(cn_chatserver, '10.0.5.3')


    net = Mininet( topo=None,
                   build=False,
                   ipBase='10.0.0.0/24')

    info('*** Adding controller\n')
    c0=net.addController(name='c0',
                         controller=Controller,
                         protocol='tcp',
                         port=6633)

    info('*** Add switches\n')
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch)
    s2 = net.addSwitch('s2', cls=OVSKernelSwitch)

    info('*** Add routers\n')
    r3 = net.addHost('r3', cls=Node, ip='10.0.3.1/24')
    r3.cmd('sysctl -w net.ipv4.ip_forward=1')
    r4 = net.addHost('r4', cls=Node, ip='192.168.1.1/30')
    r4.cmd('sysctl -w net.ipv4.ip_forward=1')
    r5 = net.addHost('r5', cls=Node, ip='10.0.5.1/24')
    r5.cmd('sysctl -w net.ipv4.ip_forward=1')

    info('*** Add hosts\n')
    h1 = net.addHost('h1', ip='10.0.3.2/24', defaultRoute='via 10.0.3.1')
    h2 = net.addHost('h2', ip='10.0.3.3/24', defaultRoute='via 10.0.3.1')
    h3 = net.addHost('h3', ip='10.0.5.2/24', defaultRoute='via 10.0.5.1')
    h4 = net.addHost('h4', ip='10.0.5.3/24', defaultRoute='via 10.0.5.1')

    info('*** Add links\n')
    net.addLink(h1, s1)
    net.addLink(h2, s1)
    net.addLink(h3, s2)
    net.addLink(h4, s2)
    net.addLink(s1, r3)
    net.addLink(s2, r5)
    net.addLink(r3, r4, intfName1='r3-eth2', intfName2='r4-eth1', params1={'ip':'192.168.1.2/30'}, params2={'ip':'192.168.1.3/30'})
    net.addLink(r4, r5, intfName1='r4-eth2', intfName2='r5-eth2', params1={'ip':'192.168.2.1/30'}, params2={'ip':'192.168.2.2/30'})

    info('*** Starting network\n')
    net.build()

    info('*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info('*** Starting switches\n')
    net.get('s1').start([c0])
    net.get('s2').start([c0])

    info('*** Post configure switches and hosts\n')
    r3.cmd('ip route add 192.168.2.0/30 via 192.168.1.3 dev r3-eth2')
    r3.cmd('ip route add 192.168.2.0/30 via 192.168.2.1 onlink dev r3-eth2')
    r3.cmd('ip route add 10.0.5.0/24 via 192.168.2.1 onlink dev r3-eth2')
    r4.cmd('ip route add 10.0.3.0/24 via 192.168.1.2 dev r4-eth1')
    r4.cmd('ip route add 10.0.5.0/24 via 192.168.2.2 dev r4-eth2')
    r5.cmd('ip route add 192.168.1.0/30 via 192.168.2.1 dev r5-eth2')
    r5.cmd('ip route add 10.0.3.0/24 via 192.168.2.1 dev r5-eth2')

    makeTerm(h4, title="chat server", term="xterm", display=None, cmd=f"python3 chat_server.py   {cn_chatserver}; bash")
    makeTerm(h2, title="web server", term="xterm", display=None, cmd=f"python3 tls_server.py     {cn_webserver}; bash")
    sleep(2)
    makeTerm(h1, title="chat client1", term="xterm", display=None, cmd=f"python3 chat_client.py {cn_chatserver}; bash")
    makeTerm(h3, title="chat client2", term="xterm", display=None, cmd=f"python3 chat_client.py {cn_chatserver}; bash")

    CLI(net)
    net.stop()
    net.stopXterms()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()