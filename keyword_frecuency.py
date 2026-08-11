from collections import Counter

input_file = "mantigh_al_tayr_clean.txt"
stopwords_file = "persian_stopwords.txt"

with open(input_file, "r", encoding="utf-8") as f:
    text = f.read()

with open(stopwords_file, "r", encoding="utf-8") as f:
    stopwords = set(f.read().splitlines())

words = text.split()

filtered_words = [
    word for word in words
    if word not in stopwords
]

frequency = Counter(filtered_words)

for word, count in frequency.most_common(50):
    print(word, ":", count)