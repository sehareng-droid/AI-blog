import json
from groq import Groq
from datetime import date
from jinja2 import Template
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(BASE_DIR, "config", "config.json")
TEMPLATE_PATH = os.path.join(BASE_DIR, "templates", "post_template.md")
POSTS_DIR = os.path.join(BASE_DIR, "content", "posts")
print("BASE_DIR:", BASE_DIR)
print("POSTS_DIR:", POSTS_DIR)



# Create posts folder if not exists
os.makedirs(POSTS_DIR, exist_ok=True)

# ================= LOAD CONFIG =================
with open(CONFIG_PATH) as f:
    config = json.load(f)


client = Groq(api_key=config["groq_api_key"])
MODEL = config["model"]


# ================= LOAD TEMPLATE =================
from jinja2 import StrictUndefined

with open(TEMPLATE_PATH, encoding="utf-8") as f:
    template = Template(f.read(), undefined=StrictUndefined)


# ================= GENERATE POST =================
def generate_ai_post(topic):
    prompt = f"""
    Write a simple, beginner-friendly blog post about:

    {topic}
    
    Requirements:
    - Minimum 900 to 1200 words
    - Intro: 150–200 words
    - Each point: 150–250 words
    - Explain concepts step by step
    - Add simple examples
    - Use easy English
    - Include extra sections:
      - Why it matters
      - Simple explanation for beginners
      - Real-world use cases
      - Future of this AI tool
    - SEO guidelines:
      - Include a main keyword (1–3 words) naturally in the title, introduction, and conclusion
      - Include the keyword in at least one heading (H2 or H3)
      - Avoid keyword stuffing; use naturally within sentences
      - Optionally include secondary keywords or related terms once or twice

    Return STRICT JSON:
    {{
      "title": "",
      "intro": "",
      "points": [
        {{"title":"","detail":""}},
        {{"title":"","detail":""}},
        {{"title":"","detail":""}},
        {{"title":"","detail":""}},
        {{"title":"","detail":""}}
      ],
      "examples": ["","","","",""],
      "links": ["https://example.com","https://example.com","https://example.com"],
      "tips": ["","","","",""],
      "conclusion": ""
    }}
    """

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    xyz = response.choices[0].message.content
    #print("Raw AI response:\n", xyz)

    # ✅ Proper indentation
    xyz_clean = xyz.strip()
    #print ('xyz_clean', xyz_clean)

    import re
    try:
        json_match = re.search(r"\{.*\}", xyz_clean, re.DOTALL)
        if not json_match:
            print("❌ No JSON found in the response.")
            return None
        json_str = json_match.group()
        post_data = json.loads(json_str)
    except json.JSONDecodeError as e:
        print("❌ JSON decode error:", e)
        print("Response content was:\n", xyz_clean)
        return None

    return post_data

# ================= SAVE POST =================
def save_post(post_data):
    print("🚀 save_post() called")
    print("📄 TEMPLATE PATH:", TEMPLATE_PATH)
    print("📄 TEMPLATE SIZE:", os.path.getsize(TEMPLATE_PATH))


    try:
        content = template.render(
            title=post_data.get("title", "Untitled"),
            date=date.today().isoformat(),
            category="AI Tools",
            tags="AI, Automation, Agents",
            keyword = post_data.get("keyword", ""),
            secondary_keywords = post_data.get("secondary_keywords", []),
            intro=post_data.get("intro", ""),
            point1_title=post_data.get("points", [{}])[0].get("title", ""),
            point1_detail=post_data.get("points", [{}])[0].get("detail", ""),
            point2_title=post_data.get("points", [{},"",""])[1].get("title", ""),
            point2_detail=post_data.get("points", [{},"",""])[1].get("detail", ""),
            point3_title=post_data.get("points", [{},"",""])[2].get("title", ""),
            point3_detail=post_data.get("points", [{},"",""])[2].get("detail", ""),
            point4_title=post_data.get("points", [{},"",""])[3].get("title", ""),
            point4_detail=post_data.get("points", [{},"",""])[3].get("detail", ""),
            point5_title=post_data.get("points", [{},"",""])[4].get("title", ""),
            point5_detail=post_data.get("points", [{},"",""])[4].get("detail", ""),
            example1=post_data.get("examples", ["",""])[0],
            example2=post_data.get("examples", ["",""])[1],
            link1=post_data.get("links", ["https://example.com","https://example.com"])[0],
            link2=post_data.get("links", ["https://example.com","https://example.com"])[1],
            conclusion=post_data.get("conclusion", "")
        )
        print("✅ Template rendered successfully")
    except Exception as e:
        print("❌ ERROR in template.render():", e)
        return

        
    import re
    #print ('content', content)
    # Make a Windows-safe filename
    safe_title = post_data.get("title", "untitled").replace(" ", "-")
    safe_title = re.sub(r'[\\/*?:"<>|]', '', safe_title)
    filename = os.path.join(POSTS_DIR, f"{date.today()}-{safe_title}.md")

    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"✅ Saved: {filename}")


    #================= RUN TEST =================
'''if __name__ == "__main__":
    topic = "AI tools for business automation"
    post_data = generate_ai_post(topic)
    if post_data:
        #print (' post_data', post_data)
        save_post(post_data)
    else:
        print("❌ Post data not generated. File not saved.")'''
