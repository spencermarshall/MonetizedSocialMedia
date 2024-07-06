import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
import time
from datetime import datetime, timedelta, timezone

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def get_recent_tweets(username, num_tweets, days_limit=30):
    # Set up the WebDriver
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run in headless mode
    driver = webdriver.Chrome(service=service, options=options)

    try:
        # Navigate to the user's profile page
        url = f"https://twitter.com/{username}"
        logging.info(f"Navigating to {url}")
        driver.get(url)

        # Scroll down the page to load more tweets
        scroll_pause_time = 2
        last_height = driver.execute_script("return document.body.scrollHeight")

        tweets = []
        tweet_texts = set()  # To keep track of unique tweets
        recent_tweets_limit = datetime.now(timezone.utc) - timedelta(days=days_limit)

        while len(tweet_texts) < num_tweets:
            # Scroll down to bottom
            logging.info("Scrolling down to load more tweets")
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load the page
            time.sleep(scroll_pause_time)

            try:
                # Explicit wait for tweets to be present
                WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.XPATH, '//article[@role="article"]'))
                )
            except TimeoutException:
                logging.warning("Timeout waiting for tweets to load")
                break

            # Extract tweets after scrolling
            new_tweets = driver.find_elements(By.XPATH, '//article[@role="article"]')
            logging.info(f"Found {len(new_tweets)} tweets on the page")

            for tweet in new_tweets:
                try:
                    tweet_content_element = tweet.find_element(By.XPATH, './/div[@data-testid="tweetText"]')
                    tweet_date_element = tweet.find_element(By.XPATH, './/time')
                    tweet_content = tweet_content_element.text
                    tweet_date = tweet_date_element.get_attribute('datetime')
                    tweet_date_dt = datetime.fromisoformat(tweet_date.replace("Z", "+00:00"))
                except (StaleElementReferenceException, TimeoutException) as e:
                    logging.warning(f"Exception while fetching tweet content: {e}")
                    continue

                if tweet_content not in tweet_texts and tweet_date_dt > recent_tweets_limit:  # Ensure unique and recent tweets
                    tweet_texts.add(tweet_content)
                    tweets.append((tweet_content, tweet_date))

                if len(tweet_texts) >= num_tweets:
                    break

            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                logging.info("No more new tweets found")
                break
            last_height = new_height

        # Print the collected tweets
        logging.info(f"Collected {len(tweets)} tweets")
        for tweet_content, tweet_date in tweets[:num_tweets]:
            print(f"Date: {tweet_date}\nText: {tweet_content}\n")

    finally:
        # Close the WebDriver
        driver.quit()


# Example usage
get_recent_tweets("swmemes", 12)
