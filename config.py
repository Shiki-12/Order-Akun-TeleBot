import os
from dotenv import load_dotenv

load_dotenv()

# Telegram User IDs allowed to use restock (owner + selected users)
OWNER_ID = int(os.getenv("OWNER_ID", 0))
ALLOWED_USERS = list(map(int, os.getenv("ALLOWED_USERS", "").split(","))) if os.getenv("ALLOWED_USERS") else []

# Combine owner and allowed users
RESTOCK_ALLOWED = [OWNER_ID] + ALLOWED_USERS
