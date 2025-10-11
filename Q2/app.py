import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname='192.168.64.3', username='msfadmin', password='msfadmin')
stdin, stdout,stderr = ssh.exec_command("uname -a")
print(stdout.read().decode())
ssh.close()