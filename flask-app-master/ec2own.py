from sys import stdin, stdout
import boto3
import botocore
import paramiko
import time


ec2 = boto3.resource('ec2', region_name='ap-south-1')
instance = ec2.create_instances(
    #change ImageId to your ImageId
    ImageId = 'ami-0bba69335379e17f8',
    MinCount = 1,
    MaxCount = 1,
    InstanceType = 't2.micro',
    #change Keyname to your KeyName
    KeyName = 'project1',
    #change SecurityGroupIds to your SecurityGroupIds
    SecurityGroupIds=[
        'sg-09cab75b9110cf7a4',
    ],
)
print (instance[0].id)
instance[0].wait_until_running()           
instance[0].reload()
print (instance[0].public_ip_address)
time.sleep(15)

#key = paramiko.RSAKey.from_private_key_file("lock101.pem")
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	

client.load_system_host_keys()
client.connect(hostname=instance[0].public_ip_address, port=22, username="ec2-user", key_filename="lock101.pem")
stdin, stdout, stderr = client.exec_command('sudo yum install git -y && git clone https://github.com/aniket666555/aniket.git && sudo bash ~/flask-app2/shell.sh')
print (stdout.readlines())
time.sleep(3)
stdin, stdout, stderr = client.exec_command('sudo python ~/flask-app2/app.py &')
#stdin, stdout, stderr = client.exec_command('hostname')
print (stdout.readlines())
time.sleep(3)
#client.close()
print ("Finished")

