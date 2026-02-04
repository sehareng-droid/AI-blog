import os, json
from datetime import date
from ai_topic_generate import generate_daily_topic
from ai_content_agent import generate_ai_post, save_post

# ================= BASE PATH =================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CONFIG_DIR = os.path.join(BASE_DIR, "config")
CONTENT_DIR = os.path.join(BASE_DIR, "content")
POST_FOLDER = os.path.join(CONTENT_DIR, "posts")
USED_TOPICS_FILE = os.path.join(CONFIG_DIR, "used_topics.json")

print("BASE_DIR:", BASE_DIR)
print("POST_FOLDER:", POST_FOLDER)
print("USED_TOPICS_FILE:", USED_TOPICS_FILE)

# ================= CREATE FOLDERS =================
os.makedirs(POST_FOLDER, exist_ok=True)
os.makedirs(CONFIG_DIR, exist_ok=True)

# ================= LOAD USED TOPICS =================
if os.path.exists(USED_TOPICS_FILE):
    with open(USED_TOPICS_FILE, "r", encoding="utf-8") as f:
        try:
            used_topics = json.load(f)
        except json.JSONDecodeError:
            used_topics = []
else:
    used_topics = []

print("📚 Used topics:", used_topics)

# ================= GENERATE UNIQUE TOPIC =================
topic = None

for _ in range(5):
    topics = generate_daily_topic(1)
    if not topics:
        continue

    topic = topics[0]

    if topic not in used_topics:
        break
else:
    topic = f"AI topic {date.today()}"

print("🧠 Selected topic:", topic)

# ================= SAVE TOPIC =================
used_topics.append(topic)

with open(USED_TOPICS_FILE, "w", encoding="utf-8") as f:
    json.dump(used_topics, f, indent=2, ensure_ascii=False)

print("✅ Topic saved to used_topics.json")

# ================= GENERATE BLOG POST =================
post_data = generate_ai_post(topic)

if post_data:
    save_post(post_data)
    print("🚀 Blog updated successfully")
else:
    print("❌ Blog generation failed")
