# AWS - lambda - stopEc2Instances

Amazon Web Services Lambda function: stopEc2Instances

----

## Trigger

Example of the trigger configuration for this lambda:

- Trigger: CloudWatch Event
- Rule Type: Schedule expression
- Schedule expression (UTC): 00 5 * * ? *

## Resources

Example of the resources the lambda should have access to via its assigned role:

- AWS Managed Policy: AWSLambdaBasicExecutionRole
- Custom Policy:
  - ec2:DescribeInstances (any resource)
  - ec2:StartInstances (any resource)
  - ec2:StopInstances (any resource)

