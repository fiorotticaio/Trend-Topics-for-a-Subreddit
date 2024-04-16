# Reddit Word Frequency Analyzer

This Python program analyzes the frequency of words in a specific subreddit within a given date range. It uses the Reddit API to fetch posts and their comments, tokenizes and sanitizes the comments, and then counts the frequency of each word. The top N most common words are then saved in a JSON file.

## How to Use

1. Run the `main.py` script in your Python environment.
2. When prompted, enter the name of the subreddit you want to analyze
3. Enter the start and end dates for the period you want to analyze. The dates should be in the format YYYY-MM-DD.
4. Enter the number N of top words you want to rank.
5. The program will then fetch the data, analyze it, and save the top N words in a file named 'top_words.json'.
6. After the program finishes, you can find the results in the 'top_words.json' file.

Please note that this program requires the `nltk` library for tokenizing the comments. Make sure to install it in your Python environment before running the program.