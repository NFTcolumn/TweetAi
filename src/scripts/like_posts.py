from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pickle
import time

try:
    # Load cookies from the file
    with open('cookies.pkl', 'rb') as file:
        cookies = pickle.load(file)

    # Set up Chrome options
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless=new')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--window-size=1920,1080')

    # Initialize the Chrome WebDriver
    driver = webdriver.Chrome(options=chrome_options)

    print("Starting browser...")
    
    # Open Twitter and set up cookies
    driver.get('https://twitter.com/home')
    print("Loading cookies...")
    for cookie in cookies:
        driver.add_cookie(cookie)
    
    print("Loading Following feed...")
    driver.get('https://twitter.com/home/following')
    time.sleep(5)
    
    # Wait for tweets to load
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'article[data-testid="tweet"]'))
        )
        print("Successfully loaded Following feed")
    except:
        print("Retrying with home feed...")
        driver.get('https://twitter.com/home')
        time.sleep(5)
        # Try clicking Following tab
        tabs = driver.find_elements(By.CSS_SELECTOR, '[role="tab"]')
        for tab in tabs:
            if "Following" in tab.text:
                tab.click()
                print("Clicked Following tab")
                time.sleep(5)
                break
    
    # Verify we're on the Following feed
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'article[data-testid="tweet"]'))
        )
        print("Successfully loaded Following feed")
    except:
        raise Exception("Failed to load Following feed")

    # Function to like all posts from followed users
    def like_all_posts():
        liked_count = 0
        max_likes = 1  # Only like 1 tweet per session (10 sessions per hour = 10 likes per hour)
        max_scrolls = 10  # Increase max scrolls to find fresh tweets
        scroll_count = 0
        
        while scroll_count < max_scrolls:
            try:
                print("Waiting for feed to load...")
                # Wait for tweets to be present
                WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'article[data-testid="tweet"]'))
                )
                
                print("Looking for tweets...")
                # Find all tweets
                tweets = driver.find_elements(By.CSS_SELECTOR, 'article[data-testid="tweet"]')
                print(f"Found {len(tweets)} tweets")
                
                for tweet in tweets:
                    try:
                        # Skip ads
                        if "Ad" in tweet.text:
                            print("Skipping ad...")
                            continue
                            
                        # Get tweet text for context
                        tweet_text = tweet.text[:50]
                        print(f"\nProcessing tweet: {tweet_text}...")
                        
                        # Store tweet ID or some unique identifier to avoid duplicates
                        tweet_id = tweet.get_attribute('data-testid')
                        
                        # Try to find and click like button with retries
                        max_retries = 3
                        for attempt in range(max_retries):
                            try:
                                # Find the like button by data-testid
                                like_button = WebDriverWait(tweet, 5).until(
                                    EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="like"]'))
                                )
                                
                                # Check if already liked
                                aria_label = like_button.get_attribute('aria-label')
                                if aria_label and 'Liked' in aria_label:
                                    print("Tweet already liked, skipping...")
                                    break
                                
                                # Ensure tweet is in view
                                driver.execute_script(
                                    "arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});",
                                    tweet
                                )
                                time.sleep(1)
                                
                                # Click like button
                                if like_button.is_displayed():
                                    driver.execute_script("arguments[0].click();", like_button)
                                    liked_count += 1
                                    print(f"Successfully liked tweet #{liked_count}")
                                    time.sleep(1.5)
                                    if liked_count >= max_likes:
                                        print(f"Reached maximum likes ({max_likes}) for this session")
                                        return
                                    break
                                    
                            except Exception as e:
                                if attempt == max_retries - 1:
                                    print(f"Failed to like tweet after {max_retries} attempts")
                                time.sleep(1)
                        
                    except Exception as e:
                        print(f"Error liking tweet: {str(e)}")
                        continue
                
                # Scroll down to load more posts
                print("Scrolling for more posts...")
                driver.execute_script(
                    "window.scrollTo(0, window.scrollY + window.innerHeight);"
                )
                time.sleep(3)  # Give more time for new posts to load
                scroll_count += 1
                
            except Exception as e:
                print(f"Error while liking posts: {str(e)}")
                time.sleep(5)

    print("Starting to like posts...")
    like_all_posts()

except Exception as e:
    print(f"An error occurred: {str(e)}")

finally:
    # Close the browser
    driver.quit()
