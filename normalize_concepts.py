# Concept normalization for the network analysis

NORMALIZATION = {
    "ره": "راه",
}

print("Concept normalization rules:")
print("----------------------------")

for old, new in NORMALIZATION.items():
    print(f"{old} -> {new}")

print("\nNormalization ready.")