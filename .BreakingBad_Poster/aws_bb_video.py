import boto3 #this is pre-downloaded on aws
import random
import tweepy







def lambda_handler(event, context):
    #AWS api key's
    #...
    #...
    #...

    # Initialize the S3 client
    s3_client = boto3.client('s3')

    # Define your S3 bucket name
    bucket_name = 'your-s3-bucket-name'

    # List objects in the bucket
    response = s3_client.list_objects_v2(Bucket=bucket_name)

    client = tweepy.Client(bearer_token=bearer_token,
                           consumer_key=API_KEY, consumer_secret=API_SECRET_KEY,
                           access_token=access_token, access_token_secret=access_token_secret)

    auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET_KEY, access_token, access_token_secret)
    api = tweepy.API(auth)

    # Check if there are any objects in the bucket
    if 'Contents' not in response:
        return {
            'statusCode': 404,
            'body': 'No files found in the S3 bucket.'
        }

    # Filter the list to include only .mp4 files
    mp4_files = [file['Key'] for file in response['Contents'] if file['Key'].endswith('.mp4')]

    # If there are no MP4 files
    if not mp4_files:
        return {
            'statusCode': 404,
            'body': 'No MP4 files found in the S3 bucket.'
        }

    # Select a random MP4 file
    random_file = random.choice(mp4_files)

    # Return the randomly selected file
    return {
        'statusCode': 200,
        'body': f'Random MP4 file selected: {random_file}'
    }










video_path = '../.StarWars_Poster/videos/2 Ahsoka Short (trailer) 30s - Copy.mp4'
media = api.media_upload(video_path)

client.create_tweet(text="Ahsoka", media_ids=[media.media_id])

#IAM permission for lambda function according to chat-gpt
# {
#   "Effect": "Allow",
#   "Action": [
#     "s3:ListBucket",
#     "s3:GetObject"
#   ],
#   "Resource": [
#     "arn:aws:s3:::your-s3-bucket-name",
#     "arn:aws:s3:::your-s3-bucket-name/*"
#   ]
# }
