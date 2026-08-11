import os
import re

input_folder = "sections"
output_folder = "sections_clean"

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

files = os.listdir(input_folder)

for file in files:
    if ".txt" in file:

        input_path = os.path.join(input_folder, file)
        output_path = os.path.join(output_folder, file)

        with open(input_path, "r", encoding="utf-8") as f:
            text = f.read()

        # یکسان‌سازی حروف عربی و فارسی
        text = text.replace("ي", "ی")
        text = text.replace("ك", "ک")

        # حذف اعراب
        text = re.sub(r"[\u064B-\u065F]", "", text)

        # حذف علائم نگارشی
        text = re.sub(r"[^\w\s]", " ", text)

        # حذف فاصله‌های اضافی
        text = re.sub(r"\s+", " ", text)

        text = text.strip()

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(text)

        print(file, "cleaned successfully")

print("All sections cleaned!")