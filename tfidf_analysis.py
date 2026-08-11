from sklearn.feature_extraction.text import TfidfVectorizer

input_file = "mantigh_al_tayr_clean.txt"
stopwords_file = "persian_stopwords.txt"

with open(input_file, "r", encoding="utf-8") as f:
    text = f.read()

with open(stopwords_file, "r", encoding="utf-8") as f:
    stopwords = f.read().splitlines()


vectorizer = TfidfVectorizer(
    tokenizer=lambda x: x.split(),
    stop_words=stopwords
)

tfidf_matrix = vectorizer.fit_transform([text])

feature_names = vectorizer.get_feature_names_out()

scores = tfidf_matrix.toarray()[0]

tfidf_words = sorted(
    zip(feature_names, scores),
    key=lambda x: x[1],
    reverse=True
)

for word, score in tfidf_words[:50]:
    print(word, ":", round(score, 4))