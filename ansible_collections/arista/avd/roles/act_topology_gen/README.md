# act_topology_gen

## Overview

**act_topology_gen** is a role that generates an Arista Clout Test topology file based on AVD fabric.

The **act_topology_gen** role:

- Designed to create valid ACT topology file.

### Tasks

1. Create lab topology folder
2. Collect host variables
3. Generate ACT topology file

### Example Playbooks

Inserted into basic AVD fabric deployment playbook

```yaml
---

- name: Build Switch configuration
  hosts: branch_a_fabric
  connection: local
  gather_facts: false
  collections:
    - arista.avd
    - arista.cvp

  tasks:
    - name: 'reset local folders for output'
      tags: [ build, generate ]
      import_role:
        name: arista.avd.build_output_folders

    - name: generate intended variables
      tags: [ build, generate ]
      import_role:
        name: arista.avd.eos_designs

    - name: generate device intended config and documentation
      tags: [ build, generate ]
      import_role:
        name: eos_cli_config_gen

    - name: Build a act topolgy
      tags: [ build ]
      import_role:
        name: avd_to_act
      vars:
        veos_version: '4.28.2F'
        act_veos_username: "admin"
        act_veos_password: "arista123"
```
