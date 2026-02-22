import os
import random
import subprocess

# -----------------------------
# Step 0: Set your Chromecast IP in .local\chromecast_ip.txt
# -----------------------------
ip_file = os.path.join('.local', 'chromecast_ip.txt')
try:
    with open(ip_file, 'r', encoding='utf-8') as f:
        ip_address = f.read().strip()
except FileNotFoundError:
    print(f"Chromecast IP file not found at {ip_file}")
    exit(1)

# -----------------------------
# Step 1: Get all files in the database directory
# -----------------------------
directory = '.local/db'
files = [os.path.join(directory, file) for file in os.listdir(directory) 
         if os.path.isfile(os.path.join(directory, file))]

# -----------------------------
# Step 2: Read all lines from all files
# -----------------------------
all_lines = []
for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        for line in f:
            all_lines.append((file, line.strip()))  # Store tuple of filename and line

if not all_lines:
    print("No lines found in the database files.")
    exit(1)

# -----------------------------
# Step 3: Pick a random line and its corresponding file
# -----------------------------
random_file, random_line = random.choice(all_lines)
print(f"File: {random_file}\nLine: {random_line}")

# -----------------------------
# Step 4: Run chromecast.py with IP and video ID
# -----------------------------
subprocess.run(['python', 'chromecast.py', ip_address, random_line])