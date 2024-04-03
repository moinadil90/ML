# Example configuration file (config.py)
DATA_PATH = "data/"  # Path to your movie data files (u.data, u.item)
MOVIE_DATA_FILE = "u.item"  # Name of the movie data file
RATINGS_DATA_FILE = "u.data"  # Name of the ratings data file
MODEL_SAVE_PATH = "models/"  # Path to save trained models

# Hyperparameters for your recommender algorithm (adjust as needed)
ALGORITHM = "SVD"  # Choose your recommender algorithm (e.g., SVD, ALS)
N_FACTORS = 100  # Number of latent factors for matrix factorization
LEARNING_RATE = 0.01  # Learning rate for the algorithm
EPOCHS = 10  # Number of training epochs

# Other configurations (e.g., database connection details, logging settings)
