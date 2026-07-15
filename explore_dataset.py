import os

BASE_DIR = r"C:\Users\Shalini\Desktop\IBS2_PROJECT\dataset"

print("\n📂 DATASET CONTENTS:")
for item in os.listdir(BASE_DIR):
    print(" -", item)

print("\n📂 METHYLATION FOLDER CONTENTS:")
meth_dir = os.path.join(BASE_DIR, "methylation_450k")
if os.path.exists(meth_dir):
    for f in os.listdir(meth_dir):
        print(" -", f)
else:
    print("❌ methylation_450k folder not found")
