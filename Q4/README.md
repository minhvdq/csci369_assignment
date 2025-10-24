# Ransomware Tool

## Overview

This is a ransomware implementation that encrypts important files on a target machine and demands payment for decryption. The ransomware uses a hybrid encryption approach combining AES-256-CBC symmetric encryption for the target file and RSA asymmetric encryption for the decryption key. When executed, it encrypts the `my_secrets.txt` file in the same directory and holds it for ransom until the specified payment is provided.

## Prerequisites

### Required Software

The ransomware requires **OpenSSL** to be installed on the target system for cryptographic operations:

```bash
# On Ubuntu/Debian systems
sudo apt-get install openssl

# On CentOS/RHEL systems
sudo yum install openssl

# On macOS
brew install openssl
```

### File Requirements

- `my_secrets.txt`: The target file containing important information to be encrypted
- The ransomware will create several temporary files during execution:
  - `key.txt`: AES encryption key (temporarily created)
  - `key_cipher.txt`: RSA-encrypted version of the AES key
  - `data_cyper.txt`: AES-encrypted version of the target file

## Usage

### Execution

```bash
python3 ransonware.py
```

### What Happens During Execution

1. **Key Generation**: Creates a random 16-byte base64-encoded AES key
2. **RSA Key Pair**: Generates a 2048-bit RSA public/private key pair
3. **File Encryption**: Encrypts `my_secrets.txt` using AES-256-CBC with the generated key
4. **Key Encryption**: Encrypts the AES key using the RSA public key
5. **Cleanup**: Deletes the original `my_secrets.txt` and the unencrypted AES key
6. **Ransom Demand**: Displays the ransom message and waits for payment

### Example Session

**Initial Execution:**
```bash
$ python3 ransonware.py
Your file important.txt is encrypted. To decrypt it, you need to pay me $10000 and send key_cipher.txt to me!
HihiHaha: 
```

**During Ransom Process:**
```bash
HihiHaha: hello
HihiHaha: who are you
HihiHaha: $10000
```

**After Payment (Decryption Process):**
- The ransomware automatically decrypts the files
- `my_secrets.txt` is restored to its original state
- All encrypted files are cleaned up
- The program exits

### File States

**Before Ransomware Execution:**
```
Q4/
├── ransonware.py
└── my_secrets.txt          # Contains: "Hello Worlddd!!!"
```

**After Ransomware Execution:**
```
Q4/
├── ransonware.py
├── key_cipher.txt          # RSA-encrypted AES key
└── data_cyper.txt          # AES-encrypted target file
```

**After Payment and Decryption:**
```
Q4/
├── ransonware.py
└── my_secrets.txt          # Restored to original content
```

### Encryption Process Details

1. **Symmetric Encryption (AES-256-CBC)**:
   - Encrypts the target file (`my_secrets.txt`)
   - Uses a randomly generated 16-byte key
   - Outputs encrypted data to `data_cyper.txt`

2. **Asymmetric Encryption (RSA)**:
   - Generates 2048-bit RSA key pair
   - Encrypts the AES key with the public key
   - Outputs encrypted key to `key_cipher.txt`

3. **Key Management**:
   - Private key is kept in memory during execution
   - Public key is used to encrypt the AES key
   - Both keys are destroyed after encryption

### Recovery Process

To decrypt the files, the user must:
1. Type exactly `$10000` when prompted
2. The ransomware will:
   - Decrypt the AES key using the RSA private key
   - Decrypt the target file using the recovered AES key
   - Restore `my_secrets.txt` to its original state
   - Clean up all encrypted files

### Security Features

- **Hybrid Encryption**: Combines symmetric and asymmetric encryption for security
- **Key Destruction**: Original keys are deleted after encryption
- **File Verification**: Checks for file existence before operations
- **Error Handling**: Graceful error handling for missing files or failed operations