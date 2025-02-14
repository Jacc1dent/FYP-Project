#!/bin/bash

# Move to parent directory to deploy topology
cd "$(dirname "$0")/.." || exit

echo "[INFO] Deploying Containerlab Topology..."
sudo containerlab deploy -t topology.clab.yml

# Move back to config folder
cd configs || exit

echo "[INFO] Configuring VLANs and Interfaces..."
python3 intervlan_routing.py > setup_log.txt 2>&1

if [ $? -eq 0 ]; then
	echo "[SUCCESS] VLAN and Inter-VLAN Routing Configured."
else
	echo "[ERROR] VLAN Configuration Failed. Check setup_log.txt for details."
	exit 1
fi

echo "[INFO] Starting DHCP Server..."
sudo docker exec -it clab-topology-dhcp_server keactrl start

if [ $? -eq 0 ]; then
	echo "[SUCCESS] DHCP Server started successfully!"
else
	echo "[ERROR] Failed to start DHCP Server. Check setup_log.txt for details"
	exit 1
fi

echo "[INFO] Network Deployment Complete."
