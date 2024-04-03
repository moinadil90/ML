from kafka import KafkaConsumer
from json import loads

# Replace with your actual data processing and model update functions
def process_new_rating(data):
  # Extract user ID, movie ID, and rating from the data
  user_id = data['user_id']
  movie_id = data['movie_id']
  rating = data['rating']

  # Update your model or user profile based on the new rating
  # (This part would depend on your specific implementation)
  print(f"Received new rating: User {user_id} rated movie {movie_id} with {rating}.")

# Kafka consumer configuration (replace with your details)
consumer = KafkaConsumer(
    'movie_ratings',  # Replace with your topic name
    bootstrap_servers=['localhost:9092'],  # Replace with your Kafka broker address
    auto_offset_reset='earliest',
    value_deserializer=lambda x: loads(x.decode('utf-8'))  # Deserialize JSON data
)

# Continuously listen for new messages
for message in consumer:
  process_new_rating(message.value)

print("Consumer stopped.")
