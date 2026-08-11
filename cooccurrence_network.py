import os
from collections import Counter

# پوشه فایل‌های متنی
input_folder = "sections"

# اندازه پنجره هم‌رخدادی
window_size = 5

# فایل‌های ورودی
files = [
    "opening.txt_01",
    "birds_journey.txt_02",
    "seven_valleys.txt_03",
    "simurgh_encounter.txt_04",
    "final_state.txt_05"
]

# خواندن stopwords
with open("persian_stopwords.txt", "r", encoding="utf-8") as f:
    stopwords = set(f.read().split())

# مفاهیم مورد مطالعه
keywords = {
    "جان",
    "دل",
    "خویش",
    "راه",
    "عشق",
    "طلب",
    "درد",
    "سیمرغ",
    "مرغ",
    "محو",
    "فنا",
    "بقا",
    "خاک",
    "تن",
    "جسم",
    "پاک",
    "عقل",
    "نفس"
}

# نرمال‌سازی مفاهیم
normalization = {
    "ره": "راه"
}


for filename in files:

    filepath = os.path.join(input_folder, filename)

    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()

    # حذف stopwords و انتخاب keywords
    words = [
        w for w in text.split()
        if w not in stopwords and w in keywords
        or w in normalization
    ]

    # اعمال normalization
    words = [
        normalization.get(w, w)
        for w in words
    ]

    pairs = Counter()

    for i in range(len(words)):

        window = words[i:i + window_size]

        for w1 in window:

            for w2 in window:

                if w1 < w2:
                    pairs[(w1, w2)] += 1

    print("\n======================")
    print(filename)

    for pair, count in pairs.most_common(20):

        print(pair, ":", count)