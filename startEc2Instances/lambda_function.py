"""
Title: Start EC2 Instances Lambda
Description: Start all ec2 instances with a certain tag key:value
"""

import boto3


def lambda_handler(event, context):
    # Create boto3 ec2 resource and client object
    ec2_resource = boto3.resource("ec2")
    ec2_client = boto3.client("ec2")

    # Tag key:value on instances
    tag_key = "stop"
    tag_value = "nightly"

    # Prepend 'tag:' to tag_key for Filter API call
    tag_key = "tag:" + tag_key

    # Filter the list by tag key/value
    ec2_resource_list = list(
        ec2_resource.instances.filter(
            Filters=[{"Name": tag_key, "Values": [tag_value]}]
        )
    )

    # Build a list of id strings from stopped instances only
    ec2_id_list = []
    for instance in ec2_resource_list:
        if instance.state["Name"] == "stopped":
            ec2_id_list.append(instance.id)

    if ec2_id_list:
        print(f">> Starting instances: {ec2_id_list}")
        ec2_client.start_instances(InstanceIds=ec2_id_list)
    else:
        print(f">> No stopped instances to start")

    return {"statusCode": 200}
