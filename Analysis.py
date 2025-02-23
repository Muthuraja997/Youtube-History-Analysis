from textblob import TextBlob
import pandas as pd
df = pd.read_json('youtube_watch_data.json')
df=df.T
df=df.head(400)
print(df.columns)

# Assuming df is your DataFrame
df['title_sentiment'] = df['title'].apply(lambda x: TextBlob(x).sentiment.polarity)
df['description_sentiment'] = df['description'].apply(lambda x: TextBlob(x).sentiment.polarity)

# Check sentiment
# print(df[['title', 'description', 'title_sentiment', 'description_sentiment']])

# You can also classify sentiments as positive, negative, or neutral based on thresholds
def classify_sentiment(polarity):
    if polarity > 0:
        return 1
    elif polarity < 0:
        return -1
    else:
        return 0

df['title_sentiment_class'] = df['title_sentiment'].apply(classify_sentiment)
df['description_sentiment_class'] = df['description_sentiment'].apply(classify_sentiment)

# print(df[['title', 'description', 'title_sentiment_class', 'description_sentiment_class']])
mv =df["title_sentiment_class"].mean()
if mv<0:
    print("Negative")
elif mv<1:
    print("Nutral")
else:
    print("Positive")