import json
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import nltk
from nltk.corpus import stopwords
import praw
from Stock_Identifier import *
import nltk
from nltk.tokenize import sent_tokenize
import random

#Downloads a list of stopwords, words such as "the", "a", "an" and so on. Words that don't give any "information"
nltk.download('stopwords')
              
#Open the .json data set
with open("processed_sentiment_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

#Using pandas dataframe as df
df = pd.DataFrame(data)

# Splitting the dataset
X_train, X_test, y_train, y_test = train_test_split(df['sentence'], df['sentiment'], test_size=0.25, random_state=42)

# Converting text into vectors
vectorizer = CountVectorizer(stop_words=stopwords.words('english'))
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

model = LogisticRegression()
model.fit(X_train_vec, y_train)

predictions = model.predict(X_test_vec)
print('Accuracy:', accuracy_score(y_test, predictions))

# Initialize Reddit API client using credentials from a created Reddit app
reddit = praw.Reddit(
    client_id="V4ih-2hjCDRjUqIs6hX-Zw",
    client_secret="1xZktDJo7oPKd23a2sIV9OBtvc3x2A",
    user_agent="My Reddit app by u/AdvertisingSecret327",
    username="AdvertisingSecret327",
    password="Dart#32493"
)

# Select the subreddit to browse
subreddit = reddit.subreddit("stocks")

# Ensure the necessary resources are downloaded
nltk.download('punkt')


while True:
    Success = False # Variable for if everything is working

    # Retrieve the top post of the day from the r/stocks subreddit
    for submission in subreddit.top(time_filter = "day", limit=1000):

        
        # Splits text into chunks of 2-3 sentences each
        # Makes the sentiment analyisis more reliable when splitting up the post rather than doing the entire post
        def split_text_into_chunks(text):
            sentences = sent_tokenize(text)  # Split text into individual sentences
            chunks = []
            i = 0
        
            while i < len(sentences):
                chunk_size = random.choice([2, 3])  # Randomly choose 2 or 3 sentences per chunk
                chunk = " ".join(sentences[i:i + chunk_size])  # Merge sentences into one chunk
                chunks.append(chunk)
                i += chunk_size  # Move to the next chunk
        
            return chunks

        # A list with the different created chunks
        chunks = split_text_into_chunks(submission.selftext) #Submission.selftext is the content from the subreddit post
        # Running each chunk through the sentiment analysis
        for chunk in chunks:
            new_reviews = [chunk]
            new_reviews_vec = vectorizer.transform(new_reviews)
            predictions = model.predict(new_reviews_vec)
            print(predictions)
            if "Positive" in predictions:
                if stockfinder(str(new_reviews)): #Checks to see if the other functions return True inorder to then exit.
                    Success = True
                    break
        
        #Checks to see that everything is working and then stops the loop
        if Success:
            break
        
    if Success:
        break