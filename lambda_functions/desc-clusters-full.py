# -*- coding: UTF-8

from __future__ import print_function

import boto3
import json


client = boto3.client('ecs')

def lambda_handler(event, context):

    response = client.list_clusters(maxResults=100)
    clusterArns = response['clusterArns']
    clusterList = []

    for i in clusterArns:
        response = client.describe_clusters(clusters=[i])
        clusterList.insert(0,response['clusters'][0]['clusterName'])


    clusterList = json.dumps(clusterList)
    print(clusterList)

    clusterList = ''.join(clusterList)

    return clusterList
