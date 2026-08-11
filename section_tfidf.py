import os
from sklearn.feature_extraction.text import TfidfVectorizer

folder = "sections_clean"

with open("persian_stopwords.txt", "r", encoding="utf-8") as f:
    stopwords = f.read().split()

documents = []
names = []

for file in os.listdir(folder):
    if ".txt" in file:
        with open(os.path.join(folder, file), "r", encoding="utf-8") as f:
            documents.append(f.read())
        names.append(file)

vectorizer = TfidfVectorizer(
    tokenizer=lambda x: x.split(),
    stop_words=stopwords,
    lowercase=False
)

tfidf_matrix = vectorizer.fit_transform(documents)

words = vectorizer.get_feature_names_out()

for i, name in enumerate(names):
    print("\n======================")
    print(name)

    scores = tfidf_matrix[i].toarray()[0]

    top_indices = scores.argsort()[-20:][::-1]

    for index in top_indices:
        print(words[index], ":", round(scores[index], 3))