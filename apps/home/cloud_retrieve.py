import os
import boto3
import tempfile
import time
from django.conf import settings

# Replace with your AWS credentials
AWS_ACCESS_KEY_ID = 'AKIA3TNC54RBJ7LOYW5R'
AWS_SECRET_ACCESS_KEY = 'mRal/pxFi2Gj9l09jPC9HSWZEHSyE3B4c9eVZm1C'
AWS_BUCKET_NAME = 'summar'

def retrieve_files_with_contents_from_s3(folder_name):
    s3 = boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )

    # List all objects in the specified S3 bucket
    response = s3.list_objects_v2(Bucket=AWS_BUCKET_NAME)

    files_with_contents = []
    summary_content = []

    # Loop through each object to find files in the desired folder
    for obj in response['Contents']:
        key = obj['Key']

        # Check if the object (file) is in the specified folder
        if key.startswith(folder_name):
            # Extract the date of upload (LastModified) for each file
            date_uploaded = obj['LastModified']

            # Read the content of the file (audio or video file)
            if key.endswith('.mp3') or key.endswith('.mp4'):
                file_content = s3.get_object(Bucket=AWS_BUCKET_NAME, Key=key)['Body'].read()

                # Save the file temporarily in Django media directory
                with tempfile.NamedTemporaryFile(suffix=os.path.splitext(key)[1], delete=False) as tmp_file:
                    tmp_file.write(file_content)
                    local_file_path = tmp_file.name

                # Append the file path, content, and date of upload to the list
                files_with_contents.append((local_file_path, file_content, date_uploaded))
            elif key.endswith('.txt'):
                # Read the content of the text file
                if os.path.basename(key) == 'summary.txt':
                    text_content = s3.get_object(Bucket=AWS_BUCKET_NAME, Key=key)['Body'].read().decode()

                    # Append the file path, content, and date of upload to the list
                    files_with_contents.append((key, text_content, date_uploaded))

                    if 'summary' in key.lower():
                        summary_content.append(text_content)

    return files_with_contents,summary_content