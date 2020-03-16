"""
Lambda function that converts objects in a s3 bucket
from a .gif to a .png.
"""
# AWS API
import boto3
from botocore.exceptions import ClientError

# Image convertor
from PIL import Image


def lambda_handler(event, context):
    """
    Lambda handler triggered on s3 bucket object create.
    Download the gif, make a new png and upload it to s3.
    """
    # Show event and context data
    print(f">> Triggered event was: {event}")
    print(
        f""">> Context info\n
        function_name: {context.function_name}\n
        function_version: {context.function_version}
        """
    )

    # Retrieve bucket and object from passed in event
    bucket_name = event["Records"][0]["s3"]["bucket"]["name"]
    object_key = event["Records"][0]["s3"]["object"]["key"]

    # Will hold any object prefixes found
    prefix_name = ""

    # Check to see if the object key has a prefix
    if "/" in object_key:
        # Split key into a list
        object_key_list = object_key.split("/")
        # Last item in the list is the object
        object_name = object_key_list.pop()

        # Create a prefix structure from remaining list items
        for item in object_key_list:
            prefix_name = prefix_name + item + "/"

    else:
        object_name = object_key

    # Temp dir for object downloads
    tmp_dir = "/tmp/"

    # Create s3 client object
    s3_client = boto3.client("s3")

    # Download file to temp location
    print(
        f"-> Downloading object from (s3://{bucket_name}/{prefix_name + object_name}) to ({tmp_dir}{object_name})"
    )
    s3_client.download_file(
        bucket_name, prefix_name + object_name, tmp_dir + object_name
    )

    # Manipulate object
    print(f"-> Converting {object_name} from gif to png")
    image = Image.open(tmp_dir + object_name)
    modified_file = object_name.rstrip(".gif") + ".png"
    image.save(tmp_dir + modified_file, "png")

    print(f"-> Converted file is: {modified_file}")

    # Upload file to s3
    print(
        f"-> Uploading file ({tmp_dir}{modified_file}) to (s3://{bucket_name}/{prefix_name + modified_file})"
    )

    try:
        response = s3_client.upload_file(
            tmp_dir + modified_file, bucket_name, prefix_name + modified_file
        )
        print(f"-> Response to file upload: {response}")
    except ClientError as error:
        print(f"-> Error uploading file: {error}")
        print(f"-> Response to file upload: {response}")
        return False

    return True
