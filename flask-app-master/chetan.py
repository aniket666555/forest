import paramiko
import time

clinet=paramiko.SSHClient()
clinet.set_missing_host_key_policy(paramiko.AutoAddPolicy())
clinet.connect(hostname='18.183.239.210',username='ec2-user',key_filename='D:/Users/hp/Downloads/flask-app-master/key/project1.pem')
stdin,stdout,stderr=clinet.exec_command('uname -r')
print(stdout.readlines())
clinet.close()