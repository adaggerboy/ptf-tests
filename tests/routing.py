import ptf
import ptf.testutils as testutils
from ptf import packet_scapy
from ptf.testutils import group

from base import RouterBaseTest

@group("routing")
class RoutingTest(RouterBaseTest):
    def setUp(self):
        RouterBaseTest.setUp(self)
    def tearDown(self):
        RouterBaseTest.tearDown(self)

    def runTest(self):
        pkt = testutils.simple_ip_packet(ip_dst="1.1.1.1", ip_src="192.168.1.2", eth_dst="ee:33:33:33:33:33", eth_src="ee:11:11:11:11:11")

        exp_pkt = pkt.copy()
        
        exp_pkt[packet_scapy.Ether].src = "ee:44:44:44:44:44"
        exp_pkt[packet_scapy.Ether].dst = "ee:22:22:22:22:22"
        exp_pkt[packet_scapy.IP].src = "192.168.2.2"
        exp_pkt[packet_scapy.IP].ttl -= 1

        testutils.send_packet(self, self.port_in, pkt)
        testutils.verify_packet(self, exp_pkt, self.port_out)

