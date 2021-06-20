"""
starts instances when called with the -on argument
and stops when called with -off
"""

import os
import argparse
import boto3
from botocore.exceptions import ClientError

# set our global boto variables
client = boto3.client('sts')
ec2 = boto3.client('ec2')

# ready our parser and args
parser = argparse.ArgumentParser()
parser.add_argument("-on", help="turns on the webserver",
                    action="store_true") # allows for conditional evaluation
parser.add_argument("-off", help="stops the webserver",
                    action="store_true")
args = parser.parse_args()


def get_temp_creds(): # ~just MFA things~
    creds = client.get_session_token(
        DurationSeconds=900, # i.e. 15 minutes
        SerialNumber='#OBTAIN FROM CONSOLE#', # virtual only
        TokenCode=input('enter the 6-digit code: '))

def get_ec2_ids():
    response = ec2.describe_instances()
    instance_id = str(response['Reservations'][0]['Instances'][0]['InstanceId'])
    return instance_id

def kickstart(ids):
    try: # dry run to verify permissions
        response=ec2.start_instances(
        InstanceIds=[ids],
        DryRun=True)

    except ClientError as e:
        if 'DryRunOperation' not in str(e):
            raise

    # no errors; liftoff!
    try:
        response=ec2.start_instances(
        InstanceIds=[ids],
        DryRun=False)

        print(response)

    except ClientError as e:
        print(e)

def kickstop(ids):
    try: # dry run to verify permissions
        response=ec2.stop_instances(
        InstanceIds=[ids],
        DryRun=True)

    except ClientError as e:
        if 'DryRunOperation' not in str(e):
            raise

    # no errors; liftoff!
    try:
        response=ec2.stop_instances(
        InstanceIds=[ids],
        DryRun=False)

        print(response)

    except ClientError as e:
        print(e)

# run it
if args.on:
    kickstart(get_ec2_ids())

elif args.off:
    kickstop(get_ec2_ids())

else:
    print('make sure you specify state')
    exit()
