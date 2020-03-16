# AWS - lambda - convertImage

Amazon Web Services Lambda function: convertImage

----

## Trigger

Example of the trigger configuration for this lambda:

- Trigger: S3
- Bucket: mybucket
- Event type: ObjectCreated
- Prefix: new-images
- Suffix: .gif

## Resources

Example of the resources the lambda should have access to via its assigned role:

- AWS Managed Policy: AWSLambdaBasicExecutionRole
- Custom Policy:
  - s3:PutObject (mybucket/*)
  - s3:GetObject (mybucket/*)
  - s3:ListObject (mybucket/*)
  - s3:HeadBucket (any resource)

