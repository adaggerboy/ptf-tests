#!/bin/bash

# Define the names for the namespace and interfaces
NS_NAME="router"
TEST_NS_NAME="test"

LAN_INTERFACE="lan0"       # Internal interface in the network namespace
WAN_INTERFACE="wan0"       # External interface (connected to the outside world) on the host

VETH_IN="in"      # Internal interface inside the namespace
VETH_OUT="out"          # Peer interface to be connected to the host

ip netns add $NS_NAME
ip netns add $TEST_NS_NAME

ip link add $VETH_IN type veth peer name $LAN_INTERFACE
ip link add $VETH_OUT type veth peer name $WAN_INTERFACE
ip link set $LAN_INTERFACE netns $NS_NAME
ip link set $WAN_INTERFACE netns $NS_NAME
ip link set $VETH_IN netns $TEST_NS_NAME
ip link set $VETH_OUT netns $TEST_NS_NAME

ip netns exec $TEST_NS_NAME ip link set $VETH_IN address ee:11:11:11:11:11
ip netns exec $TEST_NS_NAME ip link set $VETH_IN up
ip netns exec $TEST_NS_NAME ip link set $VETH_OUT address ee:22:22:22:22:22
ip netns exec $TEST_NS_NAME ip link set $VETH_OUT up
ip netns exec $NS_NAME ip link set $LAN_INTERFACE address ee:33:33:33:33:33
ip netns exec $NS_NAME ip link set $LAN_INTERFACE up
ip netns exec $NS_NAME ip link set $WAN_INTERFACE address ee:44:44:44:44:44
ip netns exec $NS_NAME ip link set $WAN_INTERFACE up

ip netns exec $TEST_NS_NAME ip addr add 192.168.1.2/24 dev $VETH_IN
ip netns exec $TEST_NS_NAME ip addr add 192.168.2.1/24 dev $VETH_OUT
ip netns exec $TEST_NS_NAME ip route add default via 192.168.1.1 

ip netns exec $NS_NAME ip addr add 192.168.1.1/24 dev $LAN_INTERFACE
ip netns exec $NS_NAME ip addr add 192.168.2.2/24 dev $WAN_INTERFACE

ip netns exec $NS_NAME iptables -A INPUT -i $LAN_INTERFACE -j ACCEPT
ip netns exec $NS_NAME iptables -A INPUT -i $WAN_INTERFACE -j ACCEPT
ip netns exec $NS_NAME iptables -A FORWARD -i $LAN_INTERFACE -o $WAN_INTERFACE -j ACCEPT
ip netns exec $NS_NAME iptables -A FORWARD -i $WAN_INTERFACE -o $LAN_INTERFACE -j ACCEPT
ip netns exec $NS_NAME iptables -t nat -A POSTROUTING -o $WAN_INTERFACE -j MASQUERADE

ip netns exec $NS_NAME sysctl -w net.ipv4.ip_forward=1

ip netns exec $NS_NAME ip route add default via 192.168.2.1

echo "NAT Router and Test NS setup complete!"
