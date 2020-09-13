import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# PYTHON3
hostname = input("Enter host IP address: ")
username = input("Enter SSH Username: ")
password = input("Enter SSH Password: ")
command = input("Enter command to execute: ")
port = 22

ssh.connect(hostname, port, username, password, look_for_keys=False)
stdin,stdout,stderr = ssh.exec_command(command)
output = stdout.readlines()
print('\n'.join(output))