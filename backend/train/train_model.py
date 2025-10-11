import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import joblib, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DATA = os.path.join(ROOT, "dataset", "symptom_disease.csv")
OUT = os.path.join(ROOT, "diseases_model")
os.makedirs(OUT, exist_ok=True)

df = pd.read_csv(DATA)   # columns: 'symptoms','disease'
df = df.dropna(subset=["symptoms","disease"])
le = LabelEncoder()
y = le.fit_transform(df["disease"])
vec = TfidfVectorizer(max_features=5000, ngram_range=(1,2))
X = vec.fit_transform(df["symptoms"])

X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)
clf = RandomForestClassifier(n_estimators=200, random_state=42)
clf.fit(X_train, y_train)
print("Train score:", clf.score(X_train, y_train))
print("Val score:", clf.score(X_val, y_val))

joblib.dump(clf, os.path.join(OUT,"model.pkl"))
joblib.dump(vec, os.path.join(OUT,"vectorizer.pkl"))
joblib.dump(le, os.path.join(OUT,"labelencoder.pkl"))
print("Saved models to", OUT)
