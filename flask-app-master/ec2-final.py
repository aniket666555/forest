import boto3, io
import botocore
import paramiko
import time

def menu():
    regionname = "ap-northeast-1"
    keyname = input("Enter your key name: ")
    github_repo = input("Enter your github repository url: ")

    return regionname, keyname, github_repo

#def get_image_id(regionname):
#    ec2_client = boto3.client('ec2', region_name=regionname) # Change as appropriate
#    image_id = ec2_client.describe_images(Owners=['self'])
#    return image_id
def get_image_id(regionname):
    try:
        image_id = ""
        ec2 = boto3.resource('ec2', region_name=regionname)
        filters = [
            {'Name': 'owner-id', 'Values': ['423864825172']},
            {'Name': 'description', 'Values': ['amzn2-ami-kernel-5.10-hvm-2.0.20220912.1-x86_64-gp2']}
        ]
        images = ec2.images.filter(Filters=filters).all()

        for image in images:
            image_id = image.id

        return image_id
    
    except Exception as e:
        print(e)
""" def create_key_pair(regionname):
    ec2_client = boto3.client("ec2", region_name=regionname)
    key_pair = ec2_client.create_key_pair(KeyName="Boto3_Key")
    data = key_pair["KeyMaterial"]
    with io.open("Boto3_Key.pem", "w", encoding="utf-8") as f1:
        f1.write(str(data))
        f1.close()
    keyname = "Boto3_Key"
    return keyname """

def get_vpc_id(regionname):
    client = boto3.client('ec2', region_name=regionname)
    response = client.describe_vpcs()
    resp = response['Vpcs']
    vpc_id = resp[0]['VpcId']

    return vpc_id

def create_security_group(vpc_id, regionname):

    ec2 = boto3.resource('ec2', region_name=regionname)
    sec_group = ec2.create_security_group(
        GroupName='flask_group', Description='flask_group', VpcId=vpc_id)
    sec_group.authorize_ingress(
        CidrIp='0.0.0.0/0',
        IpProtocol='tcp',
        FromPort=80,
        ToPort=80
    )
    sec_group.authorize_ingress(
        CidrIp='0.0.0.0/0',
        IpProtocol='tcp',
        FromPort=22,
        ToPort=22
    )
    sec_group.authorize_ingress(
        CidrIp='0.0.0.0/0',
        IpProtocol='tcp',
        FromPort=5000,
        ToPort=5000
    )

def get_security_group_id(regionname):
    client = boto3.client('ec2', region_name=regionname)
    response=client.describe_security_groups(
        Filters=[{'Name': 'group-name', 'Values': ['flask_group']}],
    )

    if (response['SecurityGroups']):
        security_group_id = response['SecurityGroups'][0]['GroupId']
    else:
        security_group_id = ''
    
    return security_group_id


def create_ec2_instance(regionname, image_id, keyname, security_group_id):
    ec2 = boto3.resource('ec2', region_name=regionname)
    instance = ec2.create_instances(
        ImageId = image_id,
        MinCount = 1,
        MaxCount = 1,
        InstanceType = 't2.micro',
        KeyName = keyname,
        SecurityGroupIds=[
            security_group_id,
        ],
    )
    print (instance[0].id)
    instance[0].wait_until_running()
    instance[0].reload()
    time.sleep(30)
    host_id = instance[0].public_ip_address
    return host_id

def launch_app(host_id, keyname, github_repo):
    dir_name =  github_repo.split("/")
    dir_name = dir_name.pop().removesuffix('.git')
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	
    client.load_system_host_keys()
    client.connect(hostname="host_id", username="ec2-user", key_filename='./'+keyname+'.pem')
    stdin, stdout, stderr = client.exec_command('sudo yum install git -y && git clone '+github_repo+' && sudo bash ~/'+dir_name+'/shell.sh')
    print (stdout.readlines())
    time.sleep(3)
    stdin, stdout, stderr = client.exec_command('sudo python ~/'+dir_name+'/app.py &')
    print (stdout.readlines())
    time.sleep(3)
    #client.close()
	
    print ("Finished")

def main():
    user_inputs = menu()
    regionname = user_inputs[0]
    keyname = user_inputs[1]
    github_repo = user_inputs[2]
    #keyname = create_key_pair(regionname)
    image_id = get_image_id(regionname)
#    image_id = user_inputs
    print (image_id)
    vpc_id = get_vpc_id(regionname)
    print (vpc_id)
    security_group_id = get_security_group_id(regionname)
    if (not security_group_id):
        create_security_group(vpc_id, regionname)
        security_group_id = get_security_group_id(regionname)
    host_id = create_ec2_instance(regionname, "ami-0bba69335379e17f8", keyname, security_group_id)
    print (host_id)
    launch_app(host_id, keyname, github_repo)

if __name__== "__main__":
    main()
