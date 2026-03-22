import os
import requests

# -------------------------
# 1️⃣ Hashnode credentials from GitHub Actions secrets
# -------------------------
TOKEN = os.environ.get("HASHNODE_TOKEN")
PUBLICATION_ID = os.environ.get("PUBLICATION_ID")
API_URL = "https://gql.hashnode.com"

# -------------------------
# 2️⃣ Local file paths
# -------------------------
NAMES_FILE = "names.txt"
PERSONALITY_FILE = "personality.txt"
DEFAULT_IMAGE_URL = "images/default.png"
POSTS_DIR = "posts"

# -------------------------
# 3️⃣ Create posts folder if it doesn't exist
# -------------------------
if not os.path.exists(POSTS_DIR):
    os.makedirs(POSTS_DIR)

# -------------------------
# 4️⃣ Read files
# -------------------------
with open(NAMES_FILE, encoding="utf-8") as f:
    names = [line.strip() for line in f if line.strip()]

with open(PERSONALITY_FILE, encoding="utf-8") as f:
    personalities = [line.strip() for line in f if line.strip()]

if len(names) != len(personalities):
    raise Exception("names.txt and personality.txt must have the same number of lines")

# -------------------------
# 5️⃣ GraphQL mutation for Hashnode
# -------------------------
mutation = """
mutation CreatePost($input: CreatePostInput!) {
  createPost(input: $input) {
    post {
      title
      url
    }
  }
}
"""

headers = {"Authorization": TOKEN}

# -------------------------
# 6️⃣ Generate posts
# -------------------------
for i, (name, trait) in enumerate(zip(names, personalities), start=1):
    # Generate Markdown content
    title = f"{name} Personality Analysis"
    content = f"""# {name} Personality Analysis

![Default Image]({DEFAULT_IMAGE_URL})

## Character Name
{name}

## Personality Trait
{trait}

## Analysis
This post discusses {
