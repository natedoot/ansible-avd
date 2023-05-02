import json
import re
import requests
from urllib.parse import quote
import yaml
from jinja2 import Environment, FileSystemLoader

def assign_unique_ips(mgmt_ip_range, node_list):
    start_ip, end_ip = mgmt_ip_range.split("-")
    start_ip_parts = [int(part) for part in start_ip.split(".")]
    end_ip_parts = [int(part) for part in end_ip.split(".")]

    nodes_ip_map = {}
    current_ip_parts = start_ip_parts

    for node in node_list:
        if current_ip_parts <= end_ip_parts:
            nodes_ip_map[node] = ".".join(str(part) for part in current_ip_parts)

            current_ip_parts[3] += 1
            if current_ip_parts[3] > 255:
                current_ip_parts[3] = 0
                current_ip_parts[2] += 1
                if current_ip_parts[2] > 255:
                    current_ip_parts[2] = 0
                    current_ip_parts[1] += 1
                    if current_ip_parts[1] > 255:
                        current_ip_parts[1] = 0
                        current_ip_parts[0] += 1
        else:
            raise Exception("The IP range is too small for the number of nodes.")

    return nodes_ip_map

def process_json_files():
    # Read JSON files
    with open("eve-nodes-result.json", "r") as f:
        eve_nodes_result = json.load(f)

    with open("eve-topology-result.json", "r") as f:
        eve_topology_result = json.load(f)

    # Process eve_topology_result and add name value from eve_nodes_result
    updated_topology_result = []
    for item in eve_topology_result:
        print(item["source_type"])
        if item["source_type"] == "node" and item["destination_label"] == "":
            source_id = re.sub("node", "", item["source"])
            source_name = eve_nodes_result.get(source_id, {"name": "unknown"})["name"]
            updated_item = {**item, "source": source_name}
            updated_topology_result.append(updated_item)
        elif item["source_type"] == "node" and item["destination_type"] == "node":
            source_id = re.sub("node", "", item["source"])
            destination_id = re.sub("node", "", item["destination"])
            source_name = eve_nodes_result.get(source_id, {"name": "unknown"})["name"]
            destination_name = eve_nodes_result.get(destination_id, {"name": "unknown"})["name"]
            updated_item = {**item, "source": source_name, "destination": destination_name}
            updated_topology_result.append(updated_item)
        else:
            print("unsupported")
    unique_node_names = set(item["source"] for item in updated_topology_result)
    nodes_ip_map = assign_unique_ips(mgmt_ip_range, unique_node_names)

    # Render the Jinja2 template and write the output to act-topology.yaml
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('./act_topology_template.j2')
    act_topology_yaml = template.render(
        updated_topology_result=updated_topology_result,
        act_veos_username=act_veos_username,
        act_veos_password=act_veos_password,
        veos_version=veos_version,
        act_cvp_user=act_cvp_user,
        act_cvp_password=act_cvp_password,
        act_cvp_version=act_cvp_version,
        act_add_cvp=act_add_cvp,
        act_cvp_ip=act_cvp_ip,
        nodes_ip_map=nodes_ip_map
    )

    with open("act-topology.yaml", "w") as f:
        f.write(act_topology_yaml)

if __name__ == "__main__":
    eve_api = "http://192.168.1.219/api/"
    lab_dir = "arista evpn"
    lab_name = "ally-avd.unl"
    veos_version = "4.28.0F"
    act_veos_username = "cvpadmin"
    act_veos_password = "arista123"
    mgmt_ip_range = "192.168.0.100-192.168.0.250"

    act_add_cvp = True

    act_cvp_version = "2022.2.1"
    act_cvp_user = "root"
    act_cvp_password = "cvproot"
    act_cvp_instance_type = "singlenode"
    act_cvp_ip = "192.168.0.5"

    # Auth to EVE
    auth_url = f"{eve_api}auth/login"
    headers = {"Accept": "application/json"}
    data = {"username": "admin", "password": "eve"}
    response = requests.post(auth_url, headers=headers, data=json.dumps(data), verify=False)
    response.raise_for_status()
    cookies = response.cookies

    # Get EVE topology
    topo_url = f"{eve_api}labs/{quote(lab_dir)}/{quote(lab_name)}/topology"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    response = requests.get(topo_url, headers=headers, cookies=cookies, verify=False)
    response.raise_for_status()
    topology = response.json()["data"]

    # Write EVE topology to file
    with open("eve-topology-result.json", "w") as f:
        json.dump(topology, f, indent=2)

    # Get node names
    nodes_url = f"{eve_api}labs/{quote(lab_dir)}/{quote(lab_name)}/nodes"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    response = requests.get(nodes_url, headers=headers, cookies=cookies, verify=False)
    response.raise_for_status()
    lab_nodes_result = response.json()["data"]

    # Write nodes to file
    with open("eve-nodes-result.json", "w") as f:
        json.dump(lab_nodes_result, f, indent=2)

    # Process JSON files and create a new YAML file
    process_json_files()
