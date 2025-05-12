# Event_Recommendation_System.ipynb

import pandas as pd
from surprise import SVD, Dataset, Reader
from surprise.model_selection import train_test_split
from surprise import accuracy

# 1. Charger les données
df = pd.read_csv('../data/event_data.csv')

# 2. Créer un Reader et charger dans Surprise
reader = Reader(rating_scale=(0, 1))
data = Dataset.load_from_df(df[['user_id', 'event_id', 'attended']], reader)

# 3. Split des données
trainset, testset = train_test_split(data, test_size=0.2, random_state=42)

# 4. Créer le modèle SVD
model = SVD()
model.fit(trainset)

# 5. Prédiction et évaluation
predictions = model.test(testset)
rmse = accuracy.rmse(predictions)
print("RMSE:", rmse)

# 6. Recommander des événements pour un utilisateur
def get_top_n(predictions, n=5):
    from collections import defaultdict
    top_n = defaultdict(list)
    for uid, iid, true_r, est, _ in predictions:
        top_n[uid].append((iid, est))
    for uid, user_ratings in top_n.items():
        user_ratings.sort(key=lambda x: x[1], reverse=True)
        top_n[uid] = user_ratings[:n]
    return top_n

top_n = get_top_n(predictions, n=5)

# Afficher les recommandations pour un utilisateur exemple
print("Top 5 événements recommandés pour l'utilisateur 42:")
print(top_n.get('42', 'Utilisateur non trouvé'))
