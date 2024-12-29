import time
import subprocess
import random

def send_tweet():
    # Get current minute to determine tweet type
    current_minute = int(time.strftime('%M'))
    # Use positive tweets on even minutes, respect tweets on odd minutes
    tweet_type = 'positive' if current_minute % 2 == 0 else 'respect'
    
    try:
        subprocess.run(['python', 'src/scripts/tweet.py', tweet_type])
        print(f"Tweet ({tweet_type}) sent at {time.strftime('%H:%M:%S')}")
    except Exception as e:
        print(f"Error sending tweet: {str(e)}")

def main():
    print("Tweet scheduler started")
    print("- Tweeting every 5 minutes")
    print("  * Even minutes: Positive tweets")
    print("  * Odd minutes: Respect tweets")
    print("Press Ctrl+C to stop")
    
    # Run first tweet immediately
    send_tweet()
    
    while True:
        # Sleep until next 5-minute mark
        current_minute = int(time.strftime('%M'))
        next_minute = ((current_minute // 5) * 5 + 5) % 60
        seconds_to_wait = (next_minute - current_minute) * 60 - int(time.strftime('%S'))
        if seconds_to_wait <= 0:
            seconds_to_wait += 300  # Wait for next 5-minute interval
        
        time.sleep(seconds_to_wait)
        send_tweet()

if __name__ == "__main__":
    main()
