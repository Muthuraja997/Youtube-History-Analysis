import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load JSON data
df = pd.read_json('youtube_watch_data.json')

# Transpose the DataFrame and reset the index
df = df.T.reset_index()
df.rename(columns={'index': 'video_id'}, inplace=True)  # Rename the index column to 'video_id'

# Handle missing descriptions by filling them with empty strings
df['description'] = df['description'].fillna('')

# Combine title and description for content-based filtering
df['content'] = df['title'] + ' ' + df['description']

# Create TF-IDF matrix
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(df['content'])

# Compute cosine similarity
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Function to get recommendations
def get_recommendations(video_id, cosine_sim=cosine_sim):
    # Find the index of the video
    idx = df.index[df['video_id'] == video_id].tolist()[0]
    
    # Get similarity scores for the video
    sim_scores = list(enumerate(cosine_sim[idx]))
    
    # Sort by similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    
    # Get top 10 similar videos (excluding the video itself)
    sim_scores = sim_scores[1:11]
    
    # Get video indices
    video_indices = [i[0] for i in sim_scores]
    
    # Return the top 10 similar videos
    return df.iloc[video_indices]

# Example: Get recommendations for a video
recommendations = get_recommendations('dgq6qProUQM')
print(recommendations[['title', 'channel']])