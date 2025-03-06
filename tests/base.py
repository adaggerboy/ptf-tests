import ptf
from ptf.base_tests import BaseTest
from ptf import packet_scapy
import ptf.testutils as testutils

class RouterBaseTest(BaseTest):
    def setUp(self):
        BaseTest.setUp(self)
        self.dataplane = ptf.dataplane_instance
        self.dataplane.flush()
        testutils.FILTERS = []

        self.port_in = 0
        # self.port_in2 = 1
        self.port_out = 1
    
    def tearDown(self):
        BaseTest.tearDown(self)

    def newDstFilter(self, dst):
        def __filter(pkt_str):
            pkt = packet_scapy.Ether(pkt_str)
            return pkt[packet_scapy.IP].dst == dst
        return __filter

    def catchDirectPacket(self, protoLayer, sport=3333, dport=80, dst='1.1.1.1', src='192.168.1.2', smac='ee:11:11:11:11:11', dmac='ee:33:33:33:33:33'):
        sendpkt = None
        if protoLayer == packet_scapy.UDP:
            sendpkt = testutils.simple_udp_packet(ip_dst=dst, ip_src=src, eth_dst=dmac, eth_src=smac, udp_sport=sport, udp_dport=dport)        
        elif protoLayer == packet_scapy.TCP:
            sendpkt = testutils.simple_tcp_packet(ip_dst=dst, ip_src=src, eth_dst=dmac, eth_src=smac, tcp_sport=sport, tcp_dport=dport)        
        elif protoLayer == packet_scapy.ICMP:
            sendpkt = testutils.simple_icmp_packet(ip_dst=dst, ip_src=src, eth_dst=dmac, eth_src=smac)        
        testutils.send_packet(self, self.port_in, sendpkt)

        testutils.add_filter(self.newDstFilter(dst=dst))
        result = testutils.dp_poll(self, port_number=self.port_out)
        
        self.dataplane.flush()
        testutils.FILTERS = []

        return packet_scapy.Ether(result.packet)[protoLayer]

        