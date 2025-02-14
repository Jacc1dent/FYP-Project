from gnmi.client import gNMIClient

# Defining switches
devices = {
    "core1": {"ip": "192.168.1.1", "port": 6030},
    "core2": {"ip": "192.168.1.2", "port": 6030},
    "agg1": {"ip": "192.168.2.1", "port": 6030},
    "agg2": {"ip": "192.168.2.2", "port": 6030},
    "agg3": {"ip": "192.168.3.1", "port": 6030},
    "agg4": {"ip": "192.168.3.2", "port": 6030},
    "acc1": {"ip": "192.168.4.1", "port": 6030},
    "acc2": {"ip": "192.168.4.2", "port": 6030},
    "acc3": {"ip": "192.168.5.1", "port": 6030},
    "acc4": {"ip": "192.168.5.2", "port": 6030}
}

# VLANs & Interfaces
vlan_config = {
    "vlan10": {"id": 10, "description": "Clients VLAN 10", "interfaces": ["ethernet-1/1", "ethernet-1/2"]},
    "vlan20": {"id": 20, "description": "Clients VLAN 20", "interfaces": ["ethernet-1/3", "ethernet-1/4"]},
    "vlan30": {"id": 30, "description": "Clients VLAN 30", "interfaces": ["ethernet-1/5", "ethernet-1/6"]},
    "vlan99": {"id": 99, "description": "Management VLAN", "interfaces": ["ethernet-1/7"]}
}

dhcp_server = {
    "name": "dhcp_server",
    "ip": "192.168.99.1",
    "port": 6030
}

def config_vlan(switch_name, switch_info):
    with gNMIClient(target=(switch_info["ip"], switch_info["port"])) as client:
        for vlan, config in vlan_config.items():
            path = f"/network-instances/network-instance[name=default]/vlans/vlan[id={config['id']}]"
            update = {
                "id": config["id"],
                "description": config["description"]
            }
            print(f"Configuring {vlan} on {switch_name}...")
            client.set(update=[(path, update)])

def config_intervlan_routing(core_switch_name, core_switch_info):
    with gNMIClient(target=(core_switch_info["ip"], core_switch_info["port"])) as client:
        for vlan, config in vlan_config.items():
            path = f"/network-instances/network-instance[name=default]/interfaces/interfaces[name=vlan{config['id']}]"
            update = {
                "name": f"vlan{config['id']}",
                "subinterface": {
                    "ipv4": {
                        "addresses": [
                            {
                                "ip": f"192.168.{config['id']}.1",
                                "prefix-length": 24
                            }
                        ]
                    }
                }
            }
            print(f"Configuring Inter-VLAN Routing for VLAN {config['id']} on {core_switch_name}...")
            client.set(update=[(path, update)])

# Apply VLAN config to access switches
for switch, info in devices.items():
    if "acc" in switch:
        config_vlan(switch, info)

# Apply Inter-VLAN Routing on Core Switches
for switch, info in devices.items():
    if "core" in switch:
        config_intervlan_routing(switch, info)

print("VLAN & Inter-VLAN Routing configuration applied successfully.")
