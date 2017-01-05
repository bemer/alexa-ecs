import boto3
import json



# This function lists the services running in a specific cluster.
def lambda_handler(event, context):
    client = boto3.client('ecs')

    response = client.list_clusters(maxResults=100)
    clusterArns = response['clusterArns']

    for i in clusterArns:
        response = client.describe_clusters(clusters=[i])
        print response['clusters'][0]['clusterName']

    return "OK"
