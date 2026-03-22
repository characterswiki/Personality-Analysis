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

# -------------------------
# 3️⃣ Read files
# -------------------------
with open(NAMES_FILE, encoding="utf-8") as f:
    names = [line.strip() for line in f if line.strip()]

with open(PERSONALITY_FILE, encoding="utf-8") as f:
    personalities = [line.strip() for line in f if line.strip()]

if len(names) != len(personalities):
    raise Exception("names.txt and personality.txt must have the same number of lines")

# -------------------------
# 4️⃣ GraphQL mutation
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
# 5️⃣ Loop and publish
# -------------------------
for i, (name, trait) in enumerate(zip(names, personalities), start=1):
    title = f"{name} Personality Analysis"
    content = f"""# {name} Personality Analysis

![Default Image]({DEFAULT_IMAGE_URL})

## Character Name
{name}

## Personality Trait
{trait}

## Analysis
This post discusses {name}'s personality based on their actions and character in the anime/manga world.
"""
    variables = {"input": {"publicationId": PUBLICATION_ID, "title": title, "contentMarkdown": content}}

    response = requests.post(API_URL, json={"query": mutation, "variables": variables}, headers=headers)
    try:
        post_url = response.json()["data"]["createPost"]["post"]["url"]
        print(f"✅ Published ({i}): {title} → {post_url}")
    except Exception:
        print(f"❌ Failed ({i}): {title}")
        print(response.text)
