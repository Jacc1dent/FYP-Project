#!/bin/bash

DEVICE="172.20.20.8"
PORT=57401
USERNAME="grpcuser"
PASSWORD="grpcpassword"

CONFIG_DIR="./configs"
GNMIC_PATH="/usr/local/bin/gnmic"

echo "==== Campus Network Management ===="
echo "Configuring: $DEVICE"

apply_config() {
	local PATH=$1
	local FILE=$2
	
	echo "Applying configuration: $PATH from file $FILE"
	$GNMIC_PATH -a $DEVICE:$PORT -u $USERNAME -p $PASSWORD --insecure -e JSON_IETF set --prefix 'native:' --update-path "$PATH" --update-file "$FILE"
	
	if [ $? -eq 0 ]; then
		echo "Success"
	else
		echo "Failed"
	fi
	echo "=================================="
}

echo "Configuring interfaces..."
apply_config "/" "$CONFIG_DIR/ethernet-1-1.json"
apply_config "/" "$CONFIG_DIR/ethernet-1-2.json"

echo "Configuring default network instance with BGP..."
apply_config "/" "$CONFIG_DIR/bgp.json"

echo "Configuring VXLAN tunnels..."
apply_config "/" "$CONFIG_DIR/vxlan10.json"

echo "Configuring EVPN..."
apply_config "/" "$CONFIG_DIR/bgp-evpn.json"

echo "Configuring MAC-VRF..."
apply_config "/" "$CONFIG_DIR/mac-vrf-10.json"

echo "Configuring IP-VRF..."
apply_config "/" "$CONFIG_DIR/ip-vrf-10.json"

echo "==== Configuration Completed ===="
