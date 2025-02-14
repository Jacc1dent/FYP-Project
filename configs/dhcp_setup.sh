#!/bin/bash

echo "[INFO] Installing necessary packages..."
apt update && apt install -y isc-dhcp-server vlan iproute2
apt upgrade -y

echo "[INFO] Creating VLAN interfaces..."
modprobe 8021q

ip link add link eth0 name eth0.10 type vlan id 10 || echo "[ERROR] Failed to create eth0.10"
ip link set eth0.10 up

ip link add link eth0 name eth0.20 type vlan id 20 || echo "[ERROR] Failed to create eth0.20"
ip link set eth0.20 up

ip link add link eth0 name eth0.30 type vlan id 30 || echo "[ERROR] Failed to create eth0.30"
ip link set eth0.30 up

echo "[INFO] Verifying VLAN interfaces..."
ip link show

echo "[INFO] Ensuring DHCP lease file exists..."
touch /var/lib/dhcp/dhcpd.leases

echo "[INFO] Configuring interfaces for DHCP server..."
echo "INTERFACESv4=\"eth0.10 eth0.20 eth0.30\"" > /etc/default/isc-dhcp-server
echo "INTERFACESv6=\"\"" >> /etc/default/isc-dhcp-server

echo "[INFO] Starting DHCP server..."
service isc-dhcp-server restart

echo "[INFO] Checking DHCP server status..."
service isc-dhcp-server status

journalctl -u isc-dhcp-server --no-pager
