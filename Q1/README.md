# ARP Spoofing Tool

## Overview

This is an ARP spoofing tool that performs a Man-in-the-Middle (MITM) attack by poisoning the ARP cache of a target device and gateway. It intercepts network traffic between the victim and the gateway by sending forged ARP packets.

## Prerequisites

### Required Package

You need to install **Scapy**, a powerful Python library for network packet manipulation:

```bash
pip install scapy
```

### Permissions

This script requires **root/administrator privileges** to send raw network packets.

## Usage

### Command

```bash
sudo python3 arpspoof.py <Target IP> <Gateway IP>
```

### Parameters

- `<Target IP>`: The IP address of the victim device you want to spoof
- `<Gateway IP>`: The IP address of the network gateway (usually your router)

### Example

```bash
sudo python3 arpspoof.py 192.168.1.100 192.168.1.1
```

This command will:
1. Discover the MAC addresses of both the target and gateway
2. Continuously send spoofed ARP packets to poison both devices' ARP caches
3. Position your machine as a man-in-the-middle between the target and gateway

### Stopping the Attack

Press **Ctrl+C** to stop the attack. The script will automatically restore the correct ARP entries on both the target and gateway before exiting.
