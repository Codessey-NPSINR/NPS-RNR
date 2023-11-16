import random

# Function to generate random latitude and longitude within India's approximate range
def generate_random_coordinates():
    # India's approximate latitude and longitude range
    min_lat, max_lat = 8.4, 37.6  # Approximate latitude range of India
    min_lon, max_lon = 68.1, 97.4  # Approximate longitude range of India

    # Generate random latitude and longitude within the range
    latitude = round(random.uniform(min_lat, max_lat), 6)
    longitude = round(random.uniform(min_lon, max_lon), 6)
    return latitude, longitude

# Create a list of 10 tuples with random latitude and longitude values within India
coordinates_list = [generate_random_coordinates() for _ in range(10)]

print(coordinates_list)