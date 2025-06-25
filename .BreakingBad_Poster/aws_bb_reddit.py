
# Initialize Reddit API
reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_USER_AGENT
)
client = tweepy.Client(bearer_token=bearer_token,
                           consumer_key=api_key, consumer_secret=api_key_secret,
                           access_token=access_token, access_token_secret=access_token_secret)

auth = tweepy.OAuth1UserHandler(api_key, api_key_secret, access_token, access_token_secret)
api = tweepy.API(auth)

def fetch_top_post_with_media():
    """Fetch the top post from r/breakingbadmemes in the last 6 hours that has valid media."""
    subreddit = reddit.subreddit('breakingbadmemes')
    recent_posts = subreddit.new(limit=30)  # Fetch recent posts to cover at least 6 hours
    now = time.time()
    six_hours_ago = now - (6 * 3600)  # Calculate timestamp for 6 hours ago

    # Filter posts: within 6 hours, not NSFW, not stickied, and has valid media
    eligible_posts = [
        post for post in recent_posts
        if post.created_utc >= six_hours_ago
        and not post.over_18
        and not post.stickied
        and post.url.endswith(('.jpg', '.jpeg', '.png', '.gif', '.mp4', '.webp'))
    ]

    if eligible_posts:
        # Select the post with the highest score
        top_post = max(eligible_posts, key=lambda p: p.score)
        print(f"Valid post found: {top_post.title}, URL: {top_post.url}, Posted at {datetime.utcfromtimestamp(top_post.created_utc)} UTC")
        return top_post
    else:
        print("No suitable post with media found in the last 6 hours.")
        return None

def lambda_handler(event, context):
    def post_to_twitter(post):
        try:
            # Download media from the post URL
            filename = '/tmp/temp_media'
            response = requests.get(post.url, timeout=10)
            response.raise_for_status()
            with open(filename, 'wb') as file:
                file.write(response.content)

            # Upload media to Twitter
            media = api.media_upload(filename)
            text = post.title

            # Clean the title by removing brackets if present
            if post.title[0] == '[':
                text = post.title[4:]
            if post.title[-1] == ']':
                text = post.title[:len(post.title)-4]

            tweet_text = f"{text}"
            print(f"Posting to Twitter: {tweet_text}")
            client.create_tweet(text="", media_ids=[media.media_id])
            print(f"Successfully posted: {post.title}")
        except tweepy.errors.TweepyException as e:
            print("An error occurred while posting to Twitter.")
            if hasattr(e, 'response') and e.response is not None:
                print("HTTP Status Code:", e.response.status_code)
                print("Reason:", e.response.reason)
                try:
                    error_details = e.response.json()
                    print("Error Details:", json.dumps(error_details, indent=4))
                except Exception as json_error:
                    print("Error while parsing response JSON:", json_error)
            else:
                print("No response object available in the exception.")
            print("Error Message:", str(e))
        except requests.exceptions.RequestException as e:
            print("An error occurred while downloading media.")
            print("Error Type:", type(e).__name__)
            print("Error Message:", str(e))
        except Exception as e:
            print("An unexpected error occurred.")
            print("Error Type:", type(e).__name__)
            print("Error Message:", str(e))

    post = fetch_top_post_with_media()
    if post:
        post_to_twitter(post)
        return {
            'statusCode': 200,
            'body': json.dumps(f"Posted: {post.title}")
        }
    else:
        print("No suitable post with media found.")
        return {
            'statusCode': 200,
            'body': json.dumps('No suitable post with media found.')
        }