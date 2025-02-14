#!/bin/bash

echo "Requesting DHCP lease..."
udhcpc -i eth0 -q
