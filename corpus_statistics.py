input_file = "data\mantigh_al_tayr_clean.txt"

with open(input_file, "r", encoding="utf-8") as f:
    text = f.read()

lines = text.splitlines()
words = text.split()

print("Number of lines:", len(lines))
print("Number of words:", len(words))
print("Number of characters:", len(text))
