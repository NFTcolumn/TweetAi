import schedule
import time
import subprocess
import random

def send_tweet():
    # Randomly choose between positive and respect tweets
    tweet_type = random.choice(['positive', 'respect'])
    try:
        subprocess.run(['python', 'src/scripts/tweet.py', tweet_type])
        print(f"Scheduled tweet ({tweet_type}) completed at {time.strftime('%H:%M:%S')}")
    except Exception as e:
        print(f"Error sending scheduled tweet: {str(e)}")

def main():
    # Schedule tweets every 30 minutes
    schedule.every(30).minutes.do(send_tweet)
    
    print("Tweet scheduler started. Will tweet every 30 minutes.")
    print("Press Ctrl+C to stop")
    
    # Send first tweet immediately
    send_tweet()
    
    # Keep running
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
