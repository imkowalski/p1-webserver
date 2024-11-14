import sqlite3
import time
import random
from datetime import datetime, timedelta
import math
# Connect to the SQLite database
conn = sqlite3.connect('./instance/data.db')
c = conn.cursor()

# Create the table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS data (
                id INTEGER PRIMARY KEY,
                epoch_time INTEGER,
                temp1 REAL,
                dist1 REAL,
                dist2 REAL)''')

# Function to generate random data
def generate_perlin_noise(base, scale, time_point, frequency=1.0):
    return base + scale * (random.uniform(-1, 1) * 0.5 + 0.5 * (1 + math.sin(frequency * time_point.timestamp())))

# Get the current time and calculate the time two weeks ago
current_time = datetime.now()
two_weeks_ago = current_time - timedelta(weeks=2)

# Populate the database with random data for every hour in the last two weeks
time_point = two_weeks_ago
while time_point <= current_time:
    epoch_time = int(time_point.timestamp())
    
    temp1 = generate_perlin_noise(20, 5, time_point, frequency=0.1)
    dist1 = generate_perlin_noise(10, 2, time_point, frequency=0.2)
    dist2 = generate_perlin_noise(15, 3, time_point, frequency=0.3)
    
    c.execute("INSERT INTO data (epoch_time, temp1, dist1, dist2) VALUES (?, ?, ?, ?)",
              (epoch_time, temp1, dist1, dist2))
    time_point += timedelta(hours=1)

# Commit the changes and close the connection
conn.commit()
conn.close()