
import pandas as pd
from surprise import Reader, Dataset, SVD, accuracy
from surprise.model_selection import train_test_split

# Define a Surprise reader object
reader = Reader(rating_scale=(1, 5))

# Data Preparation Function
def prepare_data():
  # Download the MovieLens 100k dataset (you'll need to do this manually)
  # https://grouplens.org/datasets/movielens/latest/
  ratings_df = pd.read_csv('ml-100k/u.data', sep='\t', names=['userId', 'movieId', 'rating', 'timestamp'])
  return ratings_df

# Model Training and Evaluation Function
def train_model(data):
  # Create a Surprise dataset object
  data = Dataset.load_from_df(data[['userId', 'movieId', 'rating']], reader=reader)

  # Perform train-test split
  trainset, testset = train_test_split(data, test_size=0.25)

  # Define the recommender algorithm (SVD)
  algo = SVD()

  # Train the algorithm on the training set
  algo.fit(trainset)

  # Evaluate the algorithm on the test set
  predictions = algo.predict(testset)
  rmse = accuracy.rmse(predictions)
  print(f"Root Mean Squared Error (RMSE): {rmse}")
  return algo

# Recommendation Function
def get_top_n_recommendations(algo, user_id, n=10):
  # Get all items the user has already rated
  ratings_df = prepare_data()
  user_ratings = ratings_df[ratings_df['userId'] == user_id]
  rated_movies = user_ratings['movieId'].tolist()

  # Get predictions for all unrated movies
  predictions = [algo.predict(user_id, movieId) for movieId in range(1, max(ratings_df['movieId']) + 1) 
                 if movieId not in rated_movies]

  # Sort predictions by estimated rating in descending order
  predictions.sort(key=lambda x: x.est, reverse=True)

  # Return the top N movie recommendations
  top_n_recs = predictions[:n]
  movie_ids = [int(pred.iid) for pred in top_n_recs]
  return movie_ids

# Example Usage
def recommend_movies(user_id, n=5):
  # Prepare data and train model
  ratings_df = prepare_data()
  algo = train_model(ratings_df)

  # Get recommendations
  recommended_movies = get_top_n_recommendations(algo, user_id, n)

  # Print movie titles using the MovieLens movie file (you'll need to download this)
  movies_df = pd.read_csv('ml-100k/u.item', sep='|', encoding='latin-1', names=['movieId', 'title', 'genres'])
  recommended_movies_df = movies_df[movies_df['movieId'].isin(recommended_movies)]

  print(f"Top {n} Movie Recommendations for User {user_id}:")
  for i, row in recommended_movies_df.iterrows():
    print(f"{i+1}. {row['title']}")

# Example call with user ID 123
recommend_movies(123)
