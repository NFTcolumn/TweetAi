from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pickle
import time
import sys
import pandas as pd
import random

def get_unused_tweet(tweet_type=None):
    try:
        # Read the CSV file
        df = pd.read_csv('src/tweets.csv')
        
        # Convert used column to integer
        df['used'] = df['used'].astype(int)
        
        # Filter for unused tweets
        unused_tweets = df[df['used'] == 0]
        
        # If no unused tweets, reset all tweets to unused
        if len(unused_tweets) == 0:
            print("All tweets have been used, resetting...")
            df['used'] = 0
            unused_tweets = df
        
        # Filter by type if specified
        if tweet_type:
            unused_tweets = unused_tweets[unused_tweets['type'] == tweet_type]
        
        if len(unused_tweets) == 0:
            print(f"No unused tweets of type {tweet_type}, using any type...")
            unused_tweets = df[df['used'] == 0]
        
        # Get a random unused tweet
        tweet = unused_tweets.sample(n=1).iloc[0]
        print(f"Selected tweet: {tweet['tweet']}")
        
        # Mark the tweet as used
        tweet_text = tweet['tweet']
        df.loc[df['tweet'] == tweet_text, 'used'] = 1
        
        # Save the updated CSV with proper permissions
        try:
            # Convert used column to int to ensure proper saving
            df['used'] = df['used'].astype(int)
            
            # Save with proper encoding
            df.to_csv('src/tweets.csv', index=False, quoting=1, encoding='utf-8')
            
            # Verify the save was successful
            saved_df = pd.read_csv('src/tweets.csv')
            if saved_df.loc[saved_df['tweet'] == tweet_text, 'used'].iloc[0] == 1:
                print("Successfully updated CSV file and verified changes")
            else:
                print("Warning: CSV update could not be verified")
        except Exception as e:
            print(f"Error saving CSV: {str(e)}")
            # Try alternative save method
            df.to_csv('src/tweets.csv', index=False, mode='w')
        print(f"Marked tweet as used: {tweet_text}")
        
        return tweet_text
        
    except Exception as e:
        print(f"Error in get_unused_tweet: {str(e)}")
        # Return a default tweet if there's an error
        return "Every day is a new opportunity."

def send_tweet(tweet_text):
    # Set up Chrome options
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--start-maximized')

    # Initialize the Chrome WebDriver
    driver = webdriver.Chrome(options=chrome_options)

    try:
        # Load Twitter
        driver.get('https://twitter.com/home')

        # Load cookies
        with open('cookies.pkl', 'rb') as file:
            cookies = pickle.load(file)
            for cookie in cookies:
                driver.add_cookie(cookie)

        # Refresh page to apply cookies
        driver.refresh()
        time.sleep(3)

        # Wait for page to load
        time.sleep(5)
        
        try:
            # Press 'n' to open new tweet dialog
            webdriver.ActionChains(driver).send_keys('n').perform()
            time.sleep(2)
            
            # Wait for and fill tweet textarea
            tweet_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="tweetTextarea_0"]'))
            )
            tweet_input.send_keys(tweet_text)
            time.sleep(2)
            
            # Press Cmd+Enter to send tweet
            webdriver.ActionChains(driver).key_down(Keys.COMMAND).send_keys(Keys.RETURN).key_up(Keys.COMMAND).perform()
            time.sleep(3)
            
        except Exception as e:
            print(f"Error in tweet workflow: {str(e)}")
            raise e

        print(f"Tweet sent successfully: {tweet_text}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

    finally:
        # Close the browser
        driver.quit()

if __name__ == "__main__":
    # Get tweet type from command line argument
    tweet_type = sys.argv[1] if len(sys.argv) > 1 else None
    
    # Get and send tweet
    tweet_text = get_unused_tweet(tweet_type)
    send_tweet(tweet_text)
