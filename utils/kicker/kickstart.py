"""
returns instances in plain JSON,
 or starts the one when called with the -on argument
"""

import json
import os
import requests
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
args = parser.parse_args()


def get_temp_creds(): # ~just MFA things~
    creds = client.get_session_token(
        DurationSeconds=900, # i.e. 15 minutes
        SerialNumber='#GET FROM CONSOLE#', # virtual only
        TokenCode=input('enter the 6-digit code: ')
)

def get_ec2s():
    response = ec2.describe_instances()
    print(response)

def kickstart():
    try: # dry run to verify permissions
        response = ec2.start_instances(
        InstanceIds=[
        'i-035c5e31e024f530f'], #todo: replace hardcoded instance ids
        DryRun=True)

    except ClientError as e:
        if 'DryRunOperation' not in str(e):
            raise

    # success; run for real this time
    try:
        response = ec2.start_instances(
        InstanceIds=[
        'i-035c5e31e024f530f'],
        DryRun=False)

        print(response)
    except ClientError as e:
        print(e)

# run it
if args.on:
    kickstart()

else:
    get_ec2s()
