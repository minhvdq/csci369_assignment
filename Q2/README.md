# SSH Brute Force Tool

## Overview

This is an SSH brute force tool that attempts to authenticate to an SSH server by trying multiple passwords from a provided list. It uses the Paramiko library to establish SSH connections and tests each password sequentially until a successful connection is made.


## Prerequisites

### Required Package

You need to install **Paramiko**, a Python library for SSH protocol implementation:

```bash
pip install paramiko
```

## Usage

### Command

```bash
python3 ssh_bruteforce.py <Target IP> <Username> <Password1> <Password2> <Password3> ... <Password10>
```

### Parameters

- `<Target IP>`: The IP address of the SSH server you want to test
- `<Username>`: The username to attempt authentication with
- `<Password1> ... <Password10>`: A list of 10 possible passwords to try

**Note**: The script expects exactly 10 password arguments (total of 12 arguments including script name, target IP, and username).

### Example

```bash
python3 ssh_bruteforce.py 192.168.1.100 admin password123 admin123 root letmein 12345678 qwerty welcome password admin
```

This command will:
1. Connect to the SSH server at 192.168.1.100
2. Attempt to login with username "admin"
3. Try each of the 10 provided passwords in sequence
4. Report success when a valid password is found or failure if none work

### Output

- **Success**: `You have successfully connected to <Target IP>! \n Password is <Password>`
- **Failure**: `No invalid password for <Target IP>!!!`

