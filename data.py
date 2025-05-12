# Générer un jeu de données simulé : event_data.csv

import pandas as pd
import numpy as np
import random

n_users = 50
n_events = 30

data = []
for _ in range(1000):
    user = random.randint(1, n_users)
    event = random.randint(1, n_events)
    attended = random.choice([0, 1])
    lat = random.uniform(36.0, 37.0)   # Exemple : latitude en Tunisie
    lon = random.uniform(9.0, 10.0)    # Exemple : longitude en Tunisie
    data.append([str(user), str(event), attended, lat, lon])

df = pd.DataFrame(data, columns=["user_id", "event_id", "attended", "location_lat", "location_lon"])
df.to_csv("data/event_data.csv", index=False)
