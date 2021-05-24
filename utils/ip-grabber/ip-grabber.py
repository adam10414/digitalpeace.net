"""
This script will find your public IP address, and update the appropriate EC2 security policy.
"""

import json
import os

import boto3

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
"""
ip = requests.get('https://checkip.amazonaws.com')
#ip.text = '###.###.###.###'

print(ip.text)
"""

#TODO:
#REMOVE ACCESS KEYS FROM HARD CODE
#PUT THEM IN THE AUTH FOLDER AND CALL THEM SYMBOLICALLY
#git igore auth folder.

ec2 = boto3.resource(
    'ec2',
    aws_access_key_id='',  #KEY GOES HERE
    aws_secret_access_key='',  #KEY GOES HERE
    region_name='us-east-2')

allow_home_ip_security_group = ec2.SecurityGroup('sg-0b78bce9d3f627bf9')

#TODO:
#Reference the below article and update the policies.
#Add a check to see if we even need to do anything.
#Article: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.SecurityGroup.authorize_ingress
#GUI Secuirty policy: https://us-east-2.console.aws.amazon.com/ec2/v2/home?region=us-east-2#SecurityGroup:groupId=sg-0b78bce9d3f627bf9

print(json.dumps(allow_home_ip_security_group.ip_permissions, indent=4))
