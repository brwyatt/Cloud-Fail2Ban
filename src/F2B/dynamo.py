import boto3
from boto3.dynamodb.conditions import Key


table = boto3.resource('dynamodb', region_name='us-west-2').Table('F2B')
