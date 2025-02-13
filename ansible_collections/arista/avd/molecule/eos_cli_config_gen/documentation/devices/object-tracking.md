# object-tracking

## Table of Contents

- [Management](#management)
  - [Management Interfaces](#management-interfaces)
- [Monitoring](#monitoring)
  - [Object Tracking](#object-tracking-1)

## Management

### Management Interfaces

#### Management Interfaces Summary

##### IPv4

| Management Interface | Description | Type | VRF | IP Address | Gateway |
| -------------------- | ----------- | ---- | --- | ---------- | ------- |
| Management1 | OOB_MANAGEMENT | oob | MGMT | 10.73.255.122/24 | 10.73.255.2 |

##### IPv6

| Management Interface | Description | Type | VRF | IPv6 Address | IPv6 Gateway |
| -------------------- | ----------- | ---- | --- | ------------ | ------------ |
| Management1 | OOB_MANAGEMENT | oob | MGMT | - | - |

#### Management Interfaces Device Configuration

```eos
!
interface Management1
   description OOB_MANAGEMENT
   vrf MGMT
   ip address 10.73.255.122/24
```

## Monitoring

### Object Tracking

#### Object Tracking Summary

| Name | Interface | Tracked Property |
| ---- | --------- | ---------------- |
| MyTrackNoProperty | Ethernet1/1 | line-protocol |
| MyTrackSetProperty | Ethernet2/1 | line-protocol |

#### Object Tracking Device Configuration

```eos
!
track MyTrackNoProperty interface Ethernet1/1 line-protocol
track MyTrackSetProperty interface Ethernet2/1 line-protocol
```
