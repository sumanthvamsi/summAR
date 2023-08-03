import boto3
import os
import datetime
from botocore.exceptions import ClientError
from django.conf import settings
import pytz

AWS_ACCESS_KEY = 'AKIA3TNC54RBJ7LOYW5R'
AWS_SECRET_KEY = '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'
S3_BUCKET_NAME = 'summar'

# Function to upload file to S3 with a specific folder and filename
def upload_to_s3(file_path, folder_name, filename):
    s3_client = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)

    try:
        s3_client.upload_file(file_path, S3_BUCKET_NAME, f"{folder_name}/{filename}")
        return True
    except ClientError as e:
        print("Error uploading file to S3:", e)
        return False

# Function to generate a date-based subfolder
def create_date_folder():
    utc_now = datetime.datetime.utcnow()
    tz = pytz.timezone('Asia/Kolkata')
    indian_time = utc_now.astimezone(tz)
    

    a= datetime.datetime.now().strftime("%Y-%m-%d")
    v= indian_time.strftime('%H:%M:%S')
    res=f'{a}_{v}'
    return res

def main(path,num,name):
    # Example input for patient details (you can modify this based on your use case)
    patient_id = f"{name}_{num}"  # Replace with the patient's unique ID
    audio_file_path = path  # Replace with the path to your audio file
    transcript = os.path.join(settings.MEDIA_ROOT, 'new_transcripts/transcript.txt')
    summary = os.path.join(settings.MEDIA_ROOT, 'new_transcripts/summary.txt')
    # transcript = "C:/Users/sumit/Summarizer/media/new_transcripts/transcript.txt"  # Replace with actual transcript
    # summary = "C:/Users/sumit/Summarizer/media/new_transcripts/script.txt"  # Replace with actual summary

    # Generate a unique ID for the patient's folder if not provided
    

    # Generate unique filenames for transcript and summary
    audio_filename = 'audio.mp3'
    transcript_filename = "transcript.txt"
    summary_filename = "summary.txt"
     # You can extract the filename from the audio_file_path

    # Generate a date-based subfolder using the current date (YYYY-MM-DD)
    date_subfolder = create_date_folder()

    # Upload the audio file to S3 within the unique ID folder and date subfolder
    upload_status_audio = upload_to_s3(audio_file_path, f"{patient_id}/{date_subfolder}", audio_filename)
    upload_status_transcript = upload_to_s3(transcript, f"{patient_id}/{date_subfolder}", transcript_filename)
    upload_status_summary = upload_to_s3(summary, f"{patient_id}/{date_subfolder}", summary_filename)


    if upload_status_audio:
        print("File uploaded successfully.")
    else:
        print("Failed to upload the file.")
