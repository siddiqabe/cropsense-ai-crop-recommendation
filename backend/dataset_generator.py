import pandas as pd
import numpy as np
import random

# Define crops and their typical parameter ranges
crops_data = {
    'rice': {'N': (80,120), 'P': (40,60), 'K': (40,60), 'temp': (20,35), 'humidity': (70,85), 'ph': (5.0,7.0), 'rain': (100,300)},
    'wheat': {'N': (80,120), 'P': (40,60), 'K': (30,50), 'temp': (10,25), 'humidity': (60,75), 'ph': (6.0,7.5), 'rain': (50,150)},
    'maize': {'N': (100,150), 'P': (50,70), 'K': (40,60), 'temp': (18,32), 'humidity': (65,80), 'ph': (5.5,7.0), 'rain': (50,120)},
    'potato': {'N': (100,150), 'P': (60,90), 'K': (100,150), 'temp': (15,25), 'humidity': (70,85), 'ph': (5.0,6.5), 'rain': (50,120)},
    'tomato': {'N': (100,150), 'P': (60,80), 'K': (60,80), 'temp': (20,30), 'humidity': (70,85), 'ph': (6.0,7.0), 'rain': (50,100)},
    'onion': {'N': (80,120), 'P': (40,60), 'K': (60,80), 'temp': (15,30), 'humidity': (65,80), 'ph': (6.0,7.5), 'rain': (50,100)},
    'cotton': {'N': (80,120), 'P': (40,60), 'K': (40,60), 'temp': (20,40), 'humidity': (60,75), 'ph': (6.0,7.5), 'rain': (50,100)},
    'sugarcane': {'N': (150,250), 'P': (60,100), 'K': (80,150), 'temp': (20,35), 'humidity': (70,85), 'ph': (6.0,7.5), 'rain': (150,250)},
    'coffee': {'N': (80,100), 'P': (40,50), 'K': (40,50), 'temp': (15,28), 'humidity': (70,85), 'ph': (5.0,6.5), 'rain': (150,250)},
    'tea': {'N': (60,80), 'P': (30,40), 'K': (30,40), 'temp': (18,30), 'humidity': (75,85), 'ph': (4.5,5.5), 'rain': (150,300)},
    'groundnut': {'N': (20,40), 'P': (40,60), 'K': (30,40), 'temp': (25,35), 'humidity': (60,75), 'ph': (6.0,7.0), 'rain': (50,100)},
    'soybean': {'N': (20,40), 'P': (40,60), 'K': (20,40), 'temp': (20,30), 'humidity': (65,80), 'ph': (6.0,7.5), 'rain': (50,100)},
    'banana': {'N': (150,250), 'P': (60,100), 'K': (100,200), 'temp': (25,30), 'humidity': (75,85), 'ph': (6.0,7.5), 'rain': (90,120)},
    'mango': {'N': (80,120), 'P': (40,60), 'K': (60,80), 'temp': (18,35), 'humidity': (60,80), 'ph': (5.5,7.5), 'rain': (50,100)},
    'grapes': {'N': (100,150), 'P': (50,70), 'K': (60,80), 'temp': (25,32), 'humidity': (60,75), 'ph': (6.0,7.5), 'rain': (65,90)},
}

# Generate samples
samples = []
crops = list(crops_data.keys())

for crop in crops:
    params = crops_data[crop]
    # Generate 30 samples per crop
    for _ in range(30):
        N = random.randint(params['N'][0], params['N'][1])
        P = random.randint(params['P'][0], params['P'][1])
        K = random.randint(params['K'][0], params['K'][1])
        temp = random.randint(params['temp'][0], params['temp'][1])
        humidity = random.randint(params['humidity'][0], params['humidity'][1])
        ph = round(random.uniform(params['ph'][0], params['ph'][1]), 1)
        rain = random.randint(params['rain'][0], params['rain'][1])
        samples.append([N, P, K, temp, humidity, ph, rain, crop])

# Create DataFrame
df = pd.DataFrame(samples, columns=['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall', 'label'])

# Save to CSV
df.to_csv('dataset/crop_data.csv', index=False)
print(f"✅ Generated {len(df)} samples for {len(crops)} crops")
print(df.head())