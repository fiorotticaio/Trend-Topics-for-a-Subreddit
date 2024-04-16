import praw
import json
import nltk
from nltk.corpus import stopwords
from collections import Counter
from datetime import datetime
from dotenv import load_dotenv
import os

def configure():
    load_dotenv()

configure() # Load environment variables

# Initialize the nltk library and download the list of stop words
nltk.download('stopwords')
nltk.download('punkt')
stop_words = set(stopwords.words('english'))  # Adjust to 'english' if it's another language

# Configure the Reddit API
reddit = praw.Reddit(
    client_id=os.getenv('client_id'),
    client_secret=os.getenv('client_secret'),
    user_agent=os.getenv('user_agent')
)


def get_top_words(subreddit_name, start_date, end_date, N):
    subreddit = reddit.subreddit(subreddit_name)

    # Convert dates to UNIX timestamp format
    start_timestamp = int(datetime.strptime(start_date, "%Y-%m-%d").timestamp())
    end_timestamp = int(datetime.strptime(end_date, "%Y-%m-%d").timestamp())
    
    # Initialize a counter to store words
    word_count = Counter()
    
    # Collect subreddit posts within the specified time range
    posts = subreddit.hot(limit=None) # FIXME: It is not getting all posts of the subreddit
    for post in posts:
        created_utc_timestamp = int(post.created_utc) # Convert to int to compare with the other timestamps

        # Check if the post is within the specified time range
        if created_utc_timestamp < start_timestamp or created_utc_timestamp > end_timestamp:
            continue

        for comment in post.comments.list():
            if hasattr(comment, 'body'): # Check if the comment has text
                # Tokenize and sanitize comment text
                tokens = nltk.word_tokenize(comment.body.lower())
                tokens = [word for word in tokens if word.isalnum() and word not in stop_words]
            
            word_count.update(tokens) # Update word counter

    top_words = word_count.most_common(N) # Get the top N most common words
    
    # Save the top N most common words in JSON format
    with open('top_words.json', 'w', encoding='utf-8') as f:
        json.dump(top_words, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    subreddit_name = input("Enter the subreddit name (e.g., KneeInjuries): ")
    # subreddit_name = "KneeInjuries"
    start_date = input("Enter the start date (format YYYY-MM-DD): ")
    # start_date = "2023-03-01"
    end_date = input("Enter the end date (format YYYY-MM-DD): ")
    # end_date = "2024-03-02"
    N = int(input("Enter the number N of words for ranking: "))
    # N = 10

    get_top_words(subreddit_name, start_date, end_date, N)
    print(f"The top {N} words have been saved in 'top_words.json'.")
