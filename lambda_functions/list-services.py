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

    cluster = "test"

    response = client.list_services(
        cluster=cluster,
        maxResults=20
    )

    serviceList = json.dumps(response, cls = MyEncoder)
    serviceList = json.loads(serviceList)

    return serviceList['serviceArns']
