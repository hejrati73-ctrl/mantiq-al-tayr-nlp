import os

folder = "sections_clean"

for file in os.listdir(folder):
    if ".txt" in file:

        path = os.path.join(folder, file)

        with open(path, "r", encoding="utf-8") as f:
            text = f.read()

        words = text.split()
        unique_words = set(words)

        total_words = len(words)
        unique_count = len(unique_words)

        diversity = unique_count / total_words

        print("\n----------------------")
        print(file)
        print("Words:", total_words)
        print("Unique words:", unique_count)
        print("Lexical diversity:", round(diversity, 3))