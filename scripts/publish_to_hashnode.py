import requests
import os

# -------------------------
# 1️⃣ Hashnode credentials
# -------------------------
API_URL = "https://gql.hashnode.com"
TOKEN = "c087f0c7-ac69-4410-8ce3-901fd4420d98"
PUBLICATION_ID = "69bfe39f4a1e513e41d1cf99"

# -------------------------
# 2️⃣ GitHub repo URLs
# -------------------------
# Replace USERNAME and REPO with your GitHub repo info
GITHUB_BASE_URL = "https://raw.githubusercontent.com/characterswiki/Personality-Analysis/main/"
NAMES_FILE_URL = GITHUB_BASE_URL + "names.txt"
PERSONALITY_FILE_URL = GITHUB_BASE_URL + "personality.txt"
DEFAULT_IMAGE_URL = GITHUB_BASE_URL + "images/default.png"

# -------------------------
# 3️⃣ Function to fetch lines from GitHub files
# -------------------------
def fetch_file_lines(url):
    r = requests.get(url)
    if r.status_code == 200:
        return [line.strip() for line in r.text.splitlines() if line.strip()]
    else:
        print(f"❌ Failed to fetch {url}")
        return []

names = fetch_file_lines(NAMES_FILE_URL)
personalities = fetch_file_lines(PERSONALITY_FILE_URL)

# Check if the number of names and personalities match
if len(names) != len(personalities):
    raise Exception("❌ names.txt and personality.txt must have the same number of lines.")

# -------------------------
# 4️⃣ GraphQL mutation to create post
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

headers = {
    "Authorization": TOKEN
}

# -------------------------
# 5️⃣ Create posts folder if not exists (for backup)
# -------------------------
if not os.path.exists("../posts"):
    os.makedirs("../posts")

# -------------------------
# 6️⃣ Generate and publish posts
# -------------------------
for i, (name, trait) in enumerate(zip(names, personalities), start=1):
    # Generate title and Markdown content
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

    # Optional: save Markdown locally in posts/ folder
    safe_name = name.lower().replace(" ", "-")
    md_filename = f"../posts/{safe_name}.md"
    with open(md_filename, "w", encoding="utf-8") as f:
        f.write(content)

    # Prepare GraphQL variables
    variables = {
        "input": {
            "publicationId": PUBLICATION_ID,
            "title": title,
            "contentMarkdown": content
        }
    }

    # Send request to Hashnode API
    response = requests.post(API_URL, json={"query": mutation, "variables": variables}, headers=headers)

    try:
        data = response.json()
        post_url = data["data"]["createPost"]["post"]["url"]
        print(f"✅ Published ({i}): {title} → {post_url}")
    except Exception as e:
        print(f"❌ Failed to publish ({i}): {title}")
        print(response.text)
