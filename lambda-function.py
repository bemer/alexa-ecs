import boto3

def lambda_handler(event, context):

    client = boto3.client('ecs')

    cluster = "test"
    service = "mySite"

    if event['method'] == "upgrade":
        try:
            taskDefinition = "mySite:2"
            response = client.update_service(
                cluster=cluster,
                service=service,
                taskDefinition=taskDefinition
            )

        except Exception,e:
            return str(e)

    if event['method'] == "downgrade":
        try:
            taskDefinition = "mySite:1"
            response = client.update_service(
                cluster=cluster,
                service=service,
                taskDefinition=taskDefinition
            )

        except Exception,e:
            return str(e)


    return "Task definition sucessfully updated to %s." % taskDefinition.replace(":", " ")
