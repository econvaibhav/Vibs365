# -*- coding: utf-8 -*-
"""youtubecomments(1).ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1VAAyz3p9orlY9RDKnTdi7bV46p3lOnDm
"""

pip install emoji

!pip install vaderSentiment

# For Fetching Comments
from googleapiclient.discovery import build
import re
# For filtering comments with just emojis
import emoji
# Analyze the sentiments of the comment
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt

from urllib.parse import urlparse, parse_qs

input_urls = input('Enter YouTube Video URLs separated by commas: ')
urls = input_urls.split(',')

# Parsing the URLs and extracting the video IDs
video_ids = []
for url in urls:
    parsed_url = urlparse(url.strip())
    query_string = parse_qs(parsed_url.query)
    video_id = query_string['v'][0] if 'v' in query_string else None
    if video_id:
        video_ids.append(video_id)
        print("Video ID: " + video_id)
    else:
        print("Invalid YouTube URL or video ID not found for:", url)

print(f"Total valid Video IDs found: {len(video_ids)}")

comments = []
youtube = build('youtube', 'v3', developerKey='AIzaSyBqtVGzn9I_hD5rSlEnRBN2heGp-XPJ8A4')

for video_id in video_ids:
    print(f"Fetching comments for video ID: {video_id}...")
    nextPageToken = None
    try:
        while True:
            request = youtube.commentThreads().list(
                part='snippet',
                videoId=video_id,
                maxResults=100,
                pageToken=nextPageToken,
                textFormat='plainText'
            )
            response = request.execute()

            if 'items' in response:
                for item in response['items']:
                    comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
                    comments.append(comment)

                nextPageToken = response.get('nextPageToken')
                if not nextPageToken:
                    break
            else:
                print("No more comments available for video ID:", video_id)
                break
    except Exception as e:
        print(f"Failed to fetch comments for video ID {video_id} due to:", e)

print(f"Total comments fetched: {len(comments)}")

comments

import re
import emoji

# Enhanced regex pattern to catch hyperlinks more effectively
hyperlink_pattern = re.compile(
    r'https?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')

threshold_ratio = 0.65

relevant_comments = []

# Assuming 'comments' is a list of comment strings fetched previously
for comment_text in comments:
    # Normalize and strip whitespace
    comment_text = comment_text.lower().strip()

    # Count emojis in the comment
    emojis = emoji.emoji_count(comment_text)

    # Count text characters, excluding spaces and accounting for non-ASCII characters
    text_characters = len(re.sub(r'\s+', '', comment_text, flags=re.UNICODE))

    # Check if the comment has alphanumeric characters (accounting for Unicode) and no hyperlinks
    if (any(char.isalnum() for char in comment_text)) and not hyperlink_pattern.search(comment_text):
        # Check the proportion of text to emoji
        if emojis == 0 or (text_characters / (text_characters + emojis)) > threshold_ratio:
            relevant_comments.append(comment_text)

# Print the first few relevant comments, if available
print("Relevant comments:", relevant_comments[:5] if relevant_comments else "No relevant comments found.")

# Open the file using 'with' to ensure it gets closed after the block is executed
with open("ytcomments.txt", 'w', encoding='utf-8') as f:
    for idx, comment in enumerate(relevant_comments):
        f.write(f"{comment}\n")  # Using f-string for better readability and performance

print("Comments stored successfully!")

import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

# Ensure that the VADER lexicon is downloaded
nltk.download('vader_lexicon')

def sentiment_score(comment):
    # Creating a SentimentIntensityAnalyzer object.
    sentiment_object = SentimentIntensityAnalyzer()
    sentiment_dict = sentiment_object.polarity_scores(comment)
    return sentiment_dict['compound']

# Lists to store categorized comments
positive_comments = []
negative_comments = []
neutral_comments = []

# Reading comments from file
with open("ytcomments.txt", 'r', encoding='utf-8') as f:
    comments = f.readlines()

print("Analysing Comments...")
for comment in comments:
    score = sentiment_score(comment.strip())

    if score > 0.05:
        positive_comments.append(comment)
    elif score < -0.05:
        negative_comments.append(comment)
    else:
        neutral_comments.append(comment)

# Example: Print the number of comments in each category
print(f"Positive: {len(positive_comments)}, Negative: {len(negative_comments)}, Neutral: {len(neutral_comments)}")

# Printing out comments from each category
# Adjust the number below to change the number of comments displayed
number_of_comments_to_display = 300

print("Positive Comments:")
for comment in positive_comments[:number_of_comments_to_display]:
    print(comment.strip())

print("\nNegative Comments:")
for comment in negative_comments[:number_of_comments_to_display]:
    print(comment.strip())

print("\nNeutral Comments:")
for comment in neutral_comments[:number_of_comments_to_display]:
    print(comment.strip())

positive_count = len(positive_comments)
negative_count = len(negative_comments)
neutral_count = len(neutral_comments)

# labels and data for Bar chart
labels = ['Positive', 'Negative', 'Neutral']
comment_counts = [positive_count, negative_count, neutral_count]

# Creating bar chart
plt.bar(labels, comment_counts, color=['blue', 'red', 'grey'])

# Adding labels and title to the plot
plt.xlabel('Sentiment')
plt.ylabel('Comment Count')
plt.title('Sentiment Analysis of Comments')

# Displaying the chart
plt.show()

import nltk
nltk.download('stopwords')

import matplotlib.pyplot as plt
from wordcloud import WordCloud
from nltk.corpus import stopwords

# Load English stopwords (use 'finnish' for Finnish language)
stop_words = set(stopwords.words('english'))

# Define additional unnecessary words
additional_words = {'good', 'bad', 'question', 'right', 'great', 'really', 'well','even','idea','like','also','would','thing'}

# Combined stopwords
all_stopwords = stop_words.union(additional_words)

# Function to generate a word cloud and display it
def generate_word_cloud(text, title):
    # Generating the word cloud
    wordcloud = WordCloud(width=800, height=400, background_color='white', stopwords=all_stopwords).generate(text)

    # Displaying the word cloud using matplotlib
    plt.figure(figsize=(8, 4), facecolor=None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.title(title)
    plt.tight_layout(pad=0)

    plt.show()

# Function to clean and concatenate comments
def clean_and_concatenate(comments):
    return " ".join(
        " ".join(word for word in comment.strip().lower().split() if word not in all_stopwords)
        for comment in comments
    )

# Combine and clean all comments in each category
positive_text = clean_and_concatenate(positive_comments)
negative_text = clean_and_concatenate(negative_comments)
neutral_text = clean_and_concatenate(neutral_comments)

# Generating and displaying word clouds
generate_word_cloud(positive_text, "Positive Comments Word Cloud")
generate_word_cloud(negative_text, "Negative Comments Word Cloud")
generate_word_cloud(neutral_text, "Neutral Comments Word Cloud")

!pip install emoji
!pip install vaderSentiment

# For Fetching Comments
from googleapiclient.discovery import build
# For filtering comments
import re
# For filtering comments with just emojis
import emoji
# Analyze the sentiments of the comment
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
# For visualization
import matplotlib.pyplot as plt
from urllib.parse import urlparse, parse_qs

# Taking input from the user
input_url = input('Enter Youtube Video URL: ')

# Parsing the URL and extracting the video ID
parsed_url = urlparse(input_url)
query_string = parse_qs(parsed_url.query)
video_id = query_string['v'][0] if 'v' in query_string else None

if video_id:
    print("Video ID: " + video_id)

    # Getting the channelId of the video uploader using the YouTube API
    video_response = youtube.videos().list(
        part='snippet',
        id=video_id
    ).execute()

    # Check if the response contains any items
    if video_response['items']:
        video_snippet = video_response['items'][0]['snippet']
        uploader_channel_id = video_snippet['channelId']
        print("Channel ID: " + uploader_channel_id)
    else:
        print("No video found with the specified ID.")
else:
    print("Invalid YouTube URL or video ID not found.")