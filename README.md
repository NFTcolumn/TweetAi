# Twitter Automation Tool

A Python-based tool that automatically posts tweets on a schedule, alternating between positive and motivational tweets.

## Features

- 🕒 Tweets automatically every 5 minutes
- 🔄 Alternates between positive and respect-based tweets
- 📝 Manages tweet history to avoid duplicates
- 🔌 Easy to set up and run continuously

## Prerequisites

- Python 3.10 or higher
- Chrome browser installed
- Twitter account

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/TweetAi.git
cd TweetAi
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required packages:
```bash
pip install selenium pandas schedule
```

## Setup

1. Log into your Twitter account:
```bash
python src/scripts/login.py
```
- This will open Chrome and prompt you to log in
- After logging in, your session will be saved for future use

2. Set up your tweets:
```bash
# Copy the template to create your tweets file
cp src/tweets_template.csv src/tweets.csv
```
- Edit `src/tweets.csv` with your own tweets
- Each tweet needs:
  * "tweet": Your tweet text
  * "type": Either "positive" or "respect"
  * "used": Start with 0 (will be managed by the script)
- Keep tweets under 280 characters
- You can add as many tweets as you want

## Usage

Run the scheduler to start automated tweeting:
```bash
python src/scripts/scheduler.py
```

The scheduler will:
- Tweet every 5 minutes
- Alternate between positive and respect tweets based on even/odd minutes
- Mark tweets as used to avoid duplicates
- Reset the used status when all tweets of a type have been used

To stop the scheduler, press `Ctrl+C`

## File Structure

```
TweetAi/
├── src/
│   ├── scripts/
│   │   ├── login.py          # Handles Twitter authentication
│   │   ├── tweet.py          # Core tweeting functionality
│   │   └── scheduler.py      # Manages tweet scheduling
│   └── tweets.csv            # Tweet database
├── cookies.pkl               # Stores Twitter session (auto-generated)
└── README.md                # This file
```

## Customization

### Modifying Tweet Schedule
To change the tweet frequency, edit `scheduler.py`:
```python
# Current setting (5 minutes)
seconds_to_wait = 300

# Example: Tweet every 10 minutes
seconds_to_wait = 600
```

### Adding New Tweets
Add tweets to `tweets.csv` in the format:
```csv
"Your tweet text here","positive",0
"Your respect tweet here","respect",0
```

## Troubleshooting

1. If login fails:
   - Delete `cookies.pkl`
   - Run `login.py` again
   - Make sure to complete login within the browser window

2. If tweets aren't sending:
   - Check your internet connection
   - Verify Twitter is accessible
   - Run `login.py` again to refresh your session

## Notes

- The tool uses Chrome in non-headless mode for better reliability
- Tweets are selected randomly from their respective categories
- Used tweets are tracked to ensure variety
- The scheduler syncs with 5-minute intervals (e.g., 12:00, 12:05, 12:10)

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is licensed under the MIT License - see the LICENSE file for details.
