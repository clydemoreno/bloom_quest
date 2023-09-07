import time

for i in range(10):
    progress_text = f"Progress: {i}/10"
    print(progress_text, end="\r")
    time.sleep(1)

# Ensure the line is cleared by printing spaces
print(" " * len(progress_text), end="\r")
print("Done")
