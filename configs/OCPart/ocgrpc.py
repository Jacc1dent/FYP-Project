import grpc
from gnmi.proto import gnmi_pb2, gnmi_pb2_grpc
import yaml
import json
import os

def load_devices(devices_file="devices.yaml"):
    """Load device information from a YAML file."""
    try:
        with open(devices_file, 'r') as file:
            devices = yaml.safe_load(file)
        print(f"Loaded {len(devices)} devices from {devices_file}")
        return devices
    except Exception as e:
        print(f"Error loading devices: {e}")
        return {}
    
def connect_to_device(device):
    """Connect to device using gNMI."""
    print(f"Connecting to device {device['host']} at {device['port']}...")
    
    channel = grpc.insecure_channel(f"{device['host']}:{device['port']}")
    stub = gnmi_pb2_grpc.gNMIStub(channel)

    # Authenticate if credentials are provided
    metadata = [
        ('username', 'grpcuser'),
        ('password', 'grpcpassword') 
    ]

    return stub, channel, metadata

def get_capabilities(stub, metadata):
    """Get gNMI capabilities."""
    request = gnmi_pb2.CapabilityRequest()
    try:
        response = stub.Capabilities(request, metadata=metadata)
        return response
    except grpc.RpcError as e:
        print(f"gNMI call failed: {e}")
        return None

def apply_config(stub, metadata, config_file):
    """Apply configuration to the device."""
    with open(config_file, 'r') as file:
        config = yaml.safe_load(file)

    success = True

    for path, value in config.items():
        print(f"Applying config to {path}...")

        path_elements = path.strip('/').split(':')
        gnmi_path = gnmi_pb2.Path(elem=[gnmi_pb2.PathElem(name=elem) for elem in path_elements])

        json_value = json.dumps(value).encode()
        typed_value = gnmi_pb2.TypedValue(json_ietf_val=json_value)

        update = gnmi_pb2.Update(path=gnmi_path, val=typed_value)

        request = gnmi_pb2.SetRequest(update=[update])

        try:
            response = stub.Set(request, metadata=metadata)
            print(f"Config applied successfully: {path}")
        except grpc.RpcError as e:
            print(f"Failed to apply config to {path}: {e}")
            success = False
    return success

def verify_config(stub, metadata, device_role):
    """Verify configuration by checking paths based on device role."""
    success = True
    check_paths = ["openconfig-interfaces:interfaces"]

    if device_role == "access":
        check_paths.append("openconfig-vxlan:vxlan")

    if device_role == ["access", "aggregation"]:
        check_paths.append("openconfig-network-instance:network-instances")

    for path_str in check_paths:
        print(f"Verifying config for {path_str}...")

        path_elements = path_str.strip('/').split(':')
        gnmi_path = gnmi_pb2.Path(elem=[gnmi_pb2.PathElem(name=elem) for elem in path_elements])

        request = gnmi_pb2.GetRequest(path=[gnmi_path], type=gnmi_pb2.GetRequest.Config)

        try:
            response = stub.Get(request, metadata=metadata)
            print(f"Config verified successfully for {path_str}")
        except grpc.RpcError as e:
            print(f"Failed to verify config for {path_str}: {e}")
            success = False
    return success

def main():
    print("OpenConfig and gRPC Network Configuration Tool\n")

    devices = load_devices()
    if not devices:
        print("No devices found. Exiting.")
        return
    
    if not os.path.exists("configs"):
        os.makedirs("configs")
        return
    
    for device_name, device_info in devices.items():
        config_file = f"configs/{device_name}.yaml"

        print(f"\n=== Processing {device_name} ({device_info['role']}) ===")

        if not os.path.exists(config_file):
            print(f"Config file {config_file} not found. Skipping device.")
            continue

        try:
            stub, channel, metadata = connect_to_device(device_info)

            capabilities = get_capabilities(stub, metadata)
            if capabilities:
                print(f"Device supports gNMI version: {capabilities.gnmi_version}")
                print(f"Supported encodings: {', '.join(str(e) for e in capabilities.supported_encodings)}")
                print(f"OpenConfig models count: {len(capabilities.supported_models)}")
            else:
                print("Failed to get capabilities. Skipping device.")
                
            print(f"\nApplying configuration from {config_file}...")
            success = apply_config(stub, metadata, config_file)

            if success:
                print(f"\nVerifying configuration on {device_name}...")
                verify_success = verify_config(stub, metadata, device_info['role'])
                if verify_success:
                    print(f"Configuration verified successfully on {device_name}.")
                else:
                    print(f"Configuration verification failed on {device_name}.")
            else:
                print(f"Configuration application failed on {device_name}.")
        except Exception as e:
            print(f"Error processing device {device_name}: {e}")

        finally:
            if "channel" in locals():
                channel.close()
                print(f"Connection to {device_name} closed.")

    print("\n=== All devices processed ===")

if __name__ == "__main__":
    main()
