import ptf
from ptf import mask, packet_scapy
import ptf.testutils as testutils
from ptf.testutils import group

from base import RouterBaseTest


@group("nat")
class NATTCPTest(RouterBaseTest):
    def setUp(self):
        RouterBaseTest.setUp(self)
    def tearDown(self):
        RouterBaseTest.tearDown(self)

    def runTest(self):
        pkt = testutils.simple_tcp_packet(ip_dst="1.1.1.1", ip_src="192.168.1.2", eth_dst="ee:33:33:33:33:33", eth_src="ee:11:11:11:11:11")
        
        exp_pkt = pkt.copy()
        
        exp_pkt[packet_scapy.Ether].src = "ee:44:44:44:44:44"
        exp_pkt[packet_scapy.Ether].dst = "ee:22:22:22:22:22"
        exp_pkt[packet_scapy.IP].src = "192.168.2.2"
        exp_pkt[packet_scapy.IP].ttl -= 1
        
        m = mask.Mask(exp_pkt=exp_pkt)
        m.set_do_not_care_scapy(packet_scapy.TCP, 'sport')
        
        testutils.send_packet(self, self.port_in, pkt)
        testutils.verify_packet(self, exp_pkt, self.port_out)


@group("nat")
class NATUDPTest(RouterBaseTest):
    def setUp(self):
        RouterBaseTest.setUp(self)
    def tearDown(self):
        RouterBaseTest.tearDown(self)

    def runTest(self):
        pkt = testutils.simple_udp_packet(ip_dst="1.1.1.1", ip_src="192.168.1.2", eth_dst="ee:33:33:33:33:33", eth_src="ee:11:11:11:11:11")
        
        exp_pkt = pkt.copy()
        
        exp_pkt[packet_scapy.Ether].src = "ee:44:44:44:44:44"
        exp_pkt[packet_scapy.Ether].dst = "ee:22:22:22:22:22"
        exp_pkt[packet_scapy.IP].src = "192.168.2.2"
        exp_pkt[packet_scapy.IP].ttl -= 1
        
        m = mask.Mask(exp_pkt=exp_pkt)
        m.set_do_not_care_scapy(packet_scapy.UDP, 'sport')
        
        testutils.send_packet(self, self.port_in, pkt)
        testutils.verify_packet(self, exp_pkt, self.port_out)

@group("nat")
class NATICMPTest(RouterBaseTest):
    def setUp(self):
        RouterBaseTest.setUp(self)
    def tearDown(self):
        RouterBaseTest.tearDown(self)

    def runTest(self):
        pkt = testutils.simple_icmp_packet(ip_dst="1.1.1.1", ip_src="192.168.1.2", eth_dst="ee:33:33:33:33:33", eth_src="ee:11:11:11:11:11")
        
        exp_pkt = pkt.copy()
        
        exp_pkt[packet_scapy.Ether].src = "ee:44:44:44:44:44"
        exp_pkt[packet_scapy.Ether].dst = "ee:22:22:22:22:22"
        exp_pkt[packet_scapy.IP].src = "192.168.2.2"
        exp_pkt[packet_scapy.IP].ttl -= 1
        
        testutils.send_packet(self, self.port_in, pkt)
        testutils.verify_packet(self, exp_pkt, self.port_out)


@group("nat")
class NATTCPBackTest(RouterBaseTest):
    def setUp(self):
        RouterBaseTest.setUp(self)
    def tearDown(self):
        RouterBaseTest.tearDown(self)

    def runTest(self):
        respkt = self.catchDirectPacket(packet_scapy.TCP)

        backpkt = testutils.simple_tcp_packet(ip_src="1.1.1.1", ip_dst="192.168.2.2", eth_dst="ee:44:44:44:44:44", eth_src="ee:22:22:22:22:22", tcp_dport=respkt.sport, tcp_sport=80)

        exp_pkt = backpkt.copy()
        
        exp_pkt[packet_scapy.Ether].src = "ee:33:33:33:33:33"
        exp_pkt[packet_scapy.Ether].dst = "ee:11:11:11:11:11"
        exp_pkt[packet_scapy.IP].dst = "192.168.1.2"
        exp_pkt[packet_scapy.IP].ttl -= 1
        exp_pkt[packet_scapy.TCP].dport = 3333
        
        testutils.send_packet(self, self.port_out, backpkt)
        testutils.add_filter(self.newDstFilter(dst='192.168.1.2'))
        testutils.verify_packet(self, exp_pkt, self.port_in)

@group("nat")
class NATUDPBackTest(RouterBaseTest):
    def setUp(self):
        RouterBaseTest.setUp(self)
    def tearDown(self):
        RouterBaseTest.tearDown(self)

    def runTest(self):
        respkt = self.catchDirectPacket(packet_scapy.UDP)

        backpkt = testutils.simple_udp_packet(ip_src="1.1.1.1", ip_dst="192.168.2.2", eth_dst="ee:44:44:44:44:44", eth_src="ee:22:22:22:22:22", udp_dport=respkt.sport, udp_sport=80)

        exp_pkt = backpkt.copy()
        
        exp_pkt[packet_scapy.Ether].src = "ee:33:33:33:33:33"
        exp_pkt[packet_scapy.Ether].dst = "ee:11:11:11:11:11"
        exp_pkt[packet_scapy.IP].dst = "192.168.1.2"
        exp_pkt[packet_scapy.IP].ttl -= 1
        exp_pkt[packet_scapy.UDP].dport = 3333
        
        testutils.send_packet(self, self.port_out, backpkt)
        testutils.add_filter(self.newDstFilter(dst='192.168.1.2'))
        testutils.verify_packet(self, exp_pkt, self.port_in)

@group("nat")
class NATICMPBackTest(RouterBaseTest):
    def setUp(self):
        RouterBaseTest.setUp(self)
    def tearDown(self):
        RouterBaseTest.tearDown(self)

    def runTest(self):
        _ = self.catchDirectPacket(packet_scapy.ICMP)

        backpkt = testutils.simple_icmp_packet(ip_src="1.1.1.1", ip_dst="192.168.2.2", eth_dst="ee:44:44:44:44:44", eth_src="ee:22:22:22:22:22", icmp_type=0)

        exp_pkt = backpkt.copy()
        
        exp_pkt[packet_scapy.Ether].src = "ee:33:33:33:33:33"
        exp_pkt[packet_scapy.Ether].dst = "ee:11:11:11:11:11"
        exp_pkt[packet_scapy.IP].dst = "192.168.1.2"
        exp_pkt[packet_scapy.IP].ttl -= 1
    
        testutils.send_packet(self, self.port_out, backpkt)
        testutils.add_filter(self.newDstFilter(dst='192.168.1.2'))
        testutils.verify_packet(self, exp_pkt, self.port_in)
