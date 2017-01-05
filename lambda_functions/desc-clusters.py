import boto3
import json


class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return int(mktime(obj.timetuple()))

        return json.JSONEncoder.default(self, obj)


# This function lists the services running in a specific cluster.
def lambda_handler(event, context):
    client = boto3.client('ecs')

    response = client.describe_clusters(clusters=['alexademo'])

    clusterdesc = json.dumps(response, cls=MyEncoder)
    clusterdesc = json.loads(clusterdesc)

    return clusterdesc['clusterArns']