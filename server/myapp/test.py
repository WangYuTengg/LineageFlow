import os

credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
if not credentials_path or not os.path.exists(credentials_path):
    raise FileNotFoundError(f"Google application credentials file not found: {credentials_path}")