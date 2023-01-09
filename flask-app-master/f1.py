import boto3
import botocore
import paramiko
import time

def menu():
    regionname = "ap-northeast-1"
    keyname = input("Enter yoyr key name: ")
    github_repo = input("Enter the github repository url: ")

    return regionname, keyname, github_repo


def get_image_id(regionname):
    try:
        image_id = ""
        ec2 = boto3.resource('ec2',region_name=regionname)
        filters = [
            {'Name': 'owner-id', 'Values': ['423864825172']},
            {'Name': 'description', 'Values': ['amzn2-ami-Kernel-5.10-hvm-2.0.20221210.1-x86_64-gp2']}
         ]
        images = ec2.images.filter(Filters=filters).all()

        for images in images:
             image_id = image.id

        return image_id

    except Exception as e:
            print(e)


def get_vpc_id(regionname):
    client = boto3.client('ec2', region_name=regionname)
    response = client.describe_vpcs()
    resp = response['Vpcs']
    vpc_id = resp[0]['VpcId']

    return vpc_id  