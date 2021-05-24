"""
This script will find your public IP address, and update the appropriate EC2 security policy.
At the current time, we have blocked all access to the site except for our public IP addresses.
Because it's annoying to constantly find and update our IP addresses in the security policy,
 this script will do that for us.

This is also a learning exercise for working with Amazon's Python SDK. :)
"""

import json
import os
import requests
import sys

import boto3
import botocore

#Gathering user info, and saving it to save-data.json
#If there is something already saved here, we'll use that value instead.
#The user will determine which secuirty policy is updated.

if os.path.exists('./save-data.json'):
    with open('./save-data.json', 'r') as save_data:
        save_data_dict = json.load(save_data)

        #range_descriptoin contains the value we'll be looking to validate against later.
        range_description = save_data_dict['range_description']

else:
    name = ''
    while name not in ('AUSTIN', 'ADAM'):
        #Gathering input, and rejecting invalid input.
        name = input("I need to know who you are, who are you? (Austin/Adam)")
        name = name.upper()

        if name == 'AUSTIN':
            range_description = 'Home (Austin)'

            #Saving values for later use.
            with open('save-data.json', 'w') as save_data_file:
                save_data = {
                    "name": name,
                    "range_description": range_description
                }

                json.dump(save_data, save_data_file)

        elif name == 'ADAM':
            range_description = 'Home (Adam)'

            #Saving values for later use.
            with open('save-data.json', 'w') as save_data_file:
                save_data = {
                    "name": name,
                    "range_description": range_description
                }

                json.dump(save_data, save_data_file)

        else:
            print('Invalid input, unable to determine user...')

if os.path.exists('../../auth/aws_keys.json'):
    with open('../../auth/aws_keys.json', 'r') as auth_file:
        auth_dict = json.load(auth_file)

else:
    print(f"""
    It looks like you need to generate some access keys to use this script.
    Step 1: Navigate here and sign in: https://997723378435.signin.aws.amazon.com/console
    Step 2: Navigate here and generate some API access keys: https://console.aws.amazon.com/iam/home?region=us-east-2#/security_credentials

    WARNING! YOU CAN ONLY GENERATE THESE KEYS ONCE! THEY ARE ONLY VIEWABLE ONCE! Document these keys somewhere safe.
    (This app will also save them locally in ./auth/aws_keys.json if you are lazy.)


    """)
    access_key_id = input("Paste your Access Key ID here: ")
    secret_access_key = input("Paste your Secret Access Key here: ")

    auth_dict = {
        'access_key_id': access_key_id,
        'secret_access_key': secret_access_key
    }

    with open('../../auth/aws_keys.json', 'w') as auth_file:
        json.dump(auth_dict, auth_file)

ec2 = boto3.resource('ec2',
                     aws_access_key_id=auth_dict['access_key_id'],
                     aws_secret_access_key=auth_dict['secret_access_key'],
                     region_name='us-east-2')

allow_home_ip_security_groups = ec2.SecurityGroup('sg-0b78bce9d3f627bf9')

#References
#Article: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.SecurityGroup.authorize_ingress
#GUI Secuirty policy: https://us-east-2.console.aws.amazon.com/ec2/v2/home?region=us-east-2#SecurityGroup:groupId=sg-0b78bce9d3f627bf9


def check_and_update_policy():
    """
    This function takes no arguments. 
    This function will gather your current IP address and compare it to the IP address
     for your profile in the AWS security policies.
    If the IP addresses don't match, then it will revoke access from the old IP and
     grant access to your new current IP.
    """
    ip_response = requests.get('https://checkip.amazonaws.com')
    #ip.text = '###.###.###.###'
    public_ip = ip_response.text.strip()

    #print(json.dumps(allow_home_ip_security_groups.ip_permissions, indent=4))

    ip_ranges = allow_home_ip_security_groups.ip_permissions[0]['IpRanges']

    for ip in ip_ranges:
        if range_description == ip['Description']:
            cidrIp_in_policy = ip['CidrIp']
            ip_in_policy = ip['CidrIp'][:-3]

    if public_ip != ip_in_policy:
        print("Your current IP does not mach the IP in the security policy.")
        print(f"Your IP: {public_ip}")
        print(f"IP in Policy: {ip_in_policy}")
        print("Updating the IP now...")

        #Revoking the old IP access...
        revoke_response = allow_home_ip_security_groups.revoke_ingress(
            IpPermissions=[{
                'IpProtocol':
                'All',
                'IpRanges': [{
                    "CidrIp": cidrIp_in_policy,
                    "Description": range_description
                }]
            }])

        #Authorizing the new IP address...
        authorize_response = allow_home_ip_security_groups.authorize_ingress(
            IpPermissions=[{
                'IpProtocol':
                'All',
                'IpRanges': [{
                    'CidrIp': public_ip + '/32',
                    'Description': range_description
                }]
            }])

    else:
        print(
            "Your current public IP and the IP in the policy match. Exiting program..."
        )
        sys.exit()


try:  #Attempting to do stuff here.
    check_and_update_policy()

except botocore.exceptions.ClientError as error:  #If try block fails, it's likely due to auth issue.
    print(f"""
    Encounted a client error. This is likely becuase you're not authenticated. Error details below: 
    {error}

    Please sign in here: https://997723378435.signin.aws.amazon.com/console

    After signing in, navigate here: https://console.aws.amazon.com/iam/home?region=us-east-2#/security_credentials
    When looking at your security credentails, please create API access keys. 
    WARNING! 
    You can only create them once, and they are no longer viewable after creation. DOCUMENT THEM SOMEWHERE SAFE.
    
    """)

    access_key_id = input(
        "After you have documented your keys, paste the Access Key ID here:")
    secret_access_key = input("Now paste your Secret Access Key here: ")

    auth_dict = {
        'access_key_id': access_key_id,
        'secret_access_key': secret_access_key
    }

    with open('../../auth/aws_keys.json', 'w') as auth_file:
        json.dump(auth_dict, auth_file)

    #Try stuff again:
    #Generating a new resource with fresh credentials
    ec2 = boto3.resource('ec2',
                         aws_access_key_id=auth_dict['access_key_id'],
                         aws_secret_access_key=auth_dict['secret_access_key'],
                         region_name='us-east-2')

    allow_home_ip_security_groups = ec2.SecurityGroup('sg-0b78bce9d3f627bf9')

    check_and_update_policy()
