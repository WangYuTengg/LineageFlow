import os
import json

GOOGLE_APPLICATION_CREDENTIALS_PATH = 'techjam-427909-1358131fa173.json'

# Print statements for debugging
print("Current working directory:", os.getcwd())
print("Google application credentials path:", GOOGLE_APPLICATION_CREDENTIALS_PATH)

# Set the environment variable
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = GOOGLE_APPLICATION_CREDENTIALS_PATH

# Ensure the path is correct
if not os.path.exists(GOOGLE_APPLICATION_CREDENTIALS_PATH):
    raise FileNotFoundError(f"Google application credentials file not found: {GOOGLE_APPLICATION_CREDENTIALS_PATH}")

with open(os.environ['GOOGLE_APPLICATION_CREDENTIALS']) as f:
    d = json.load(f)
    print(d)