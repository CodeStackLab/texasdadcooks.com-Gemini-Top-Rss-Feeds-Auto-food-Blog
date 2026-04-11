"""
Test Script: justcookdaily.com n8n Workflow Simulation
Tests each step of the workflow independently to find failures.
"""
import requests
import random
import re
import json
import time

# ===================== CONFIG (from workflow) =====================
GEMINI_API_KEY = "AIzaSyA55SJDCybRgZ7ZoyeE-XuWqBLIT81eZgU"
PEXELS_API_KEY = "lsxGULh0YmwITJ7q7lEdpROYPbyalyCglIOmJLkKgeIf5QeH5qTvtzUs"
WP_URL = "https://justcookdaily.com"
WP_USER = "bf149a"
WP_APP_PASSWORD = "nQq4 nD4T rPtF xb3C eMw6 iw2s"

# ===================== RSS FEEDS =====================
RSS_FEEDS = [
    'https://minimalistbaker.com/feed/',
    'https://www.loveandlemons.com/feed/',
    'https://damndelicious.net/feed/',
    'https://pinchofyum.com/feed',
    'https://www.skinnytaste.com/feed/',
    'https://www.budgetbytes.com/feed/',
    'https://smittenkitchen.com/feed/',
    'https://cookieandkate.com/feed/',
    'https://www.recipetineats.com/feed/',
    'https://www.gimmesomeoven.com/feed/',
    'https://www.acouplecooks.com/feed/',
    'https://www.inspiredtaste.net/feed/',
    'https://natashaskitchen.com/feed/',
    'https://cafedelites.com/feed/',
    'https://www.spendwithpennies.com/feed/',
    'https://www.jocooks.com/feed/',
    'https://www.wellplated.com/feed/',
    'https://www.themediterraneandish.com/feed/',
    'https://www.eatwell101.com/feed',
    'https://www.halfbakedharvest.com/feed/',
    'https://sallysbakingaddiction.com/feed/',
    'https://www.onceuponachef.com/feed',
    'https://www.tasteofhome.com/feed/',
    'https://thekitchn.com/feed',
    'https://www.seriouseats.com/feed',
    'https://www.simplyrecipes.com/feed/',
    'https://food52.com/blog/feed',
]

def step_separator(title):
    print(f"\n{'='*60}")
    print(f"  STEP: {title}")
    print(f"{'='*60}")

# ===================== STEP 1: Fetch RSS Feed =====================
def test_rss_feeds():
    step_separator("1. Fetch Cooking RSS Feeds")
    random.shuffle(RSS_FEEDS)
    
    for i, feed_url in enumerate(RSS_FEEDS[:8]):
        try:
            print(f"  [{i+1}] Trying: {feed_url[:50]}...")
            resp = requests.get(feed_url, timeout=12, headers={
                'User-Agent': 'Mozilla/5.0 (compatible; JustCookDaily/1.0)'
            })
            if resp.status_code == 200 and len(resp.text) > 300:
                print(f"  ✅ SUCCESS! Got {len(resp.text)} bytes from {feed_url}")
                return resp.text, feed_url
            else:
                print(f"  ❌ Bad response: status={resp.status_code}, length={len(resp.text)}")
        except Exception as e:
            print(f"  ❌ Error: {str(e)[:60]}")
    
    print("  🔴 ALL RSS FEEDS FAILED!")
    return None, None

# ===================== STEP 2: Parse RSS & Select Article =====================
def test_parse_rss(raw_xml):
    step_separator("2. Parse RSS & Select Article")
    
    if not raw_xml:
        print("  🔴 No XML data to parse!")
        return None
    
    # Parse items
    item_blocks = re.findall(r'<item>([\s\S]*?)</item>', raw_xml)
    print(f"  Found {len(item_blocks)} <item> blocks")
    
    articles = []
    for item in item_blocks:
        # Title
        cdata_title = re.search(r'<title><!\[CDATA\[([^\]]+)\]\]></title>', item)
        plain_title = re.search(r'<title>([^<]+)</title>', item)
        title = (cdata_title.group(1) if cdata_title else (plain_title.group(1) if plain_title else '')).strip()
        
        # Description
        cdata_desc = re.search(r'<description><!\[CDATA\[([\s\S]*?)\]\]></description>', item)
        plain_desc = re.search(r'<description>([\s\S]*?)</description>', item)
        desc = (cdata_desc.group(1) if cdata_desc else (plain_desc.group(1) if plain_desc else ''))
        desc = re.sub(r'<[^>]*>', ' ', desc).strip()[:400]
        
        # Content
        encoded = re.search(r'<content:encoded><!\[CDATA\[([\s\S]*?)\]\]></content:encoded>', item)
        content = ''
        if encoded:
            content = re.sub(r'<[^>]*>', ' ', encoded.group(1)).strip()[:1500]
        
        if len(title) > 10:
            articles.append({
                'title': title,
                'description': desc,
                'content': content or desc
            })
    
    print(f"  Parsed {len(articles)} valid articles")
    
    if articles:
        # Show first 5 titles
        print(f"\n  📋 Available topics:")
        for i, a in enumerate(articles[:5]):
            print(f"     {i+1}. {a['title'][:70]}")
        
        selected = random.choice(articles[:10])
        print(f"\n  ✅ SELECTED: \"{selected['title']}\"")
        print(f"  📝 Context: {selected['description'][:150]}...")
        return selected
    else:
        print("  🔴 No articles parsed! RSS format may be different.")
        return None

# ===================== STEP 3: Test Gemini API =====================
def test_gemini(article):
    step_separator("3. Generate Article via Gemini 1.5 Pro")
    
    if not article:
        print("  🔴 No article topic to send to Gemini!")
        return None
    
    topic = article['title']
    context = article.get('description', '')[:500]
    source_content = article.get('content', '')[:1200]
    
    prompt = f"""You are a professional food writer for justcookdaily.com. Write a COMPLETELY ORIGINAL, SEO-optimized cooking article.

INSPIRATION TOPIC: "{topic}"
BRIEF CONTEXT: "{context}"
REFERENCE (for inspiration ONLY — DO NOT COPY): "{source_content}"

CRITICAL RULES:
- Write a 100% ORIGINAL article — do NOT copy any text from the reference.
- Create YOUR OWN unique title, your own angle, your own structure.
- English only. Warm, friendly, conversational food blog tone.
- Target length: 1200 to 1500 words TOTAL.
- NO H1 tag. NO promotional text. NO filler. NO placeholders like [content].
- Include REAL cooking tips and specific measurements.

OUTPUT — write EXACTLY this structure:

TITLE: [YOUR OWN unique long-tail SEO title, 8-12 words]
CATEGORY: [Single number from: 27 = Quick & Easy | 28 = Breakfast | 29 = Lunch | 30 = Dinner | 31 = Healthy | 32 = Vegetarian | 33 = Desserts | 34 = Snacks | 35 = Beverages | 36 = Tips]
SLUG: [seo-friendly-slug]
META: [SEO meta description 130-155 chars]
TAGS: [tag1],[tag2],[tag3],[tag4],[tag5],[tag6]
EXCERPT: [2 compelling sentences]
QUERY1: [Pexels search: beautiful finished plate of this dish]
QUERY2: [Pexels search: fresh raw ingredients for this dish]
QUERY3: [Pexels search: close-up cooking process action shot]

===START===

<p>[Strong opening hook]</p>

<h2>What Makes This Dish So Special</h2>
<p>[3-4 paragraphs]</p>

<h2>Ingredients You Will Need</h2>
<p>[Detailed ingredient list]</p>

<h2>Step-by-Step Instructions</h2>
<p>[Detailed numbered steps]</p>

<h2>Pro Tips for Perfect Results</h2>
<p>[Expert tips]</p>

<h2>Variations and Substitutions</h2>
<p>[At least 3 variations]</p>

<h2>Frequently Asked Questions</h2>
<p>[3 Q&As]</p>

<h2>Final Thoughts</h2>
<p>[Warm closing]</p>

===END===

REMINDER: Write REAL content. 1200-1500 words minimum."""

    body = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "maxOutputTokens": 8192,
            "temperature": 0.75
        }
    }
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"
    
    print(f"  📡 Calling Gemini 1.5 Pro (timeout=180s)...")
    print(f"  📝 Topic: \"{topic}\"")
    start = time.time()
    
    try:
        resp = requests.post(url, json=body, timeout=180, headers={'Content-Type': 'application/json'})
        elapsed = time.time() - start
        print(f"  ⏱️  Response time: {elapsed:.1f}s")
        print(f"  📊 Status: {resp.status_code}")
        
        if resp.status_code != 200:
            print(f"  🔴 ERROR: {resp.text[:300]}")
            return None
        
        data = resp.json()
        raw_text = data.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', '')
        
        if not raw_text or len(raw_text) < 100:
            print(f"  🔴 Empty or too short response! Length: {len(raw_text)}")
            print(f"  Response: {json.dumps(data)[:300]}")
            return None
        
        # Count words
        word_count = len(raw_text.split())
        print(f"  ✅ Got {len(raw_text)} chars, ~{word_count} words")
        
        # Parse metadata
        lines = raw_text.split('\n')
        title = slug = meta = excerpt = query1 = query2 = query3 = ''
        article_start = -1
        
        for i, line in enumerate(lines):
            t = line.strip()
            if t.startswith('TITLE:'): title = t[6:].strip()
            if t.startswith('SLUG:'): slug = t[5:].strip()
            if t.startswith('META:'): meta = t[5:].strip()
            if t.startswith('EXCERPT:'): excerpt = t[8:].strip()
            if t.startswith('QUERY1:'): query1 = t[7:].strip()
            if t.startswith('QUERY2:'): query2 = t[7:].strip()
            if t.startswith('QUERY3:'): query3 = t[7:].strip()
            if t == '===START===': article_start = i + 1
        
        # Extract article HTML
        article_html = ''
        if article_start >= 0:
            rest = lines[article_start:]
            end_idx = next((i for i, l in enumerate(rest) if l.strip() == '===END==='), len(rest))
            article_html = '\n'.join(rest[:end_idx]).strip()
        
        h2_count = len(re.findall(r'<h2', article_html))
        has_content = len(article_html) > 300 and h2_count >= 3
        
        print(f"\n  📋 Parsed Gemini Output:")
        print(f"     Title:   {title[:70]}")
        print(f"     Slug:    {slug}")
        print(f"     Meta:    {meta[:80]}...")
        print(f"     Excerpt: {excerpt[:80]}...")
        print(f"     Query1:  {query1}")
        print(f"     Query2:  {query2}")
        print(f"     Query3:  {query3}")
        print(f"     HTML:    {len(article_html)} chars, {h2_count} H2 sections")
        print(f"     Valid:   {'✅ YES' if has_content else '🔴 NO'}")
        
        if has_content:
            # Show first 200 chars of article
            clean = re.sub(r'<[^>]*>', '', article_html[:300])
            print(f"\n  📖 Article preview: {clean[:200]}...")
        
        return {
            'title': title, 'slug': slug, 'meta': meta,
            'excerpt': excerpt, 'article_html': article_html,
            'query1': query1, 'query2': query2, 'query3': query3,
            'has_content': has_content, 'word_count': word_count
        }
        
    except requests.Timeout:
        print(f"  🔴 TIMEOUT after 180s!")
        return None
    except Exception as e:
        print(f"  🔴 ERROR: {str(e)[:200]}")
        return None

# ===================== STEP 4: Test Pexels API =====================
def test_pexels(queries):
    step_separator("4. Fetch Images from Pexels API")
    
    if not queries:
        print("  🔴 No image queries!")
        return
    
    for i, query in enumerate(queries, 1):
        if not query:
            print(f"  [{i}] ⚠️ Empty query, skipping")
            continue
            
        try:
            url = f"https://api.pexels.com/v1/search?query={requests.utils.quote(query)}&per_page=5&orientation=landscape"
            resp = requests.get(url, headers={'Authorization': PEXELS_API_KEY}, timeout=10)
            
            if resp.status_code == 200:
                data = resp.json()
                photos = data.get('photos', [])
                print(f"  [{i}] ✅ Query: \"{query[:40]}\" → {len(photos)} photos found")
                if photos:
                    photo = photos[0]
                    print(f"       Photo: {photo.get('photographer', '?')} — {photo.get('src', {}).get('large', '?')[:60]}...")
            else:
                print(f"  [{i}] 🔴 Pexels error: {resp.status_code} — {resp.text[:100]}")
        except Exception as e:
            print(f"  [{i}] 🔴 Error: {str(e)[:60]}")

# ===================== STEP 5: Test WordPress Connection =====================
def test_wordpress():
    step_separator("5. Test WordPress Connection")
    
    import base64
    auth = base64.b64encode(f"{WP_USER}:{WP_APP_PASSWORD}".encode()).decode()
    
    try:
        resp = requests.get(
            f"{WP_URL}/wp-json/wp/v2/posts?per_page=3&status=publish",
            headers={'Authorization': f'Basic {auth}'},
            timeout=15
        )
        
        if resp.status_code == 200:
            posts = resp.json()
            print(f"  ✅ WordPress connected! Found {len(posts)} recent posts:")
            for p in posts:
                title = p.get('title', {}).get('rendered', '?')
                slug = p.get('slug', '?')
                print(f"     - \"{title[:50]}\" (/{slug}/)")
        else:
            print(f"  🔴 WordPress error: {resp.status_code}")
            print(f"     {resp.text[:200]}")
    except Exception as e:
        print(f"  🔴 Connection error: {str(e)[:100]}")

# ===================== RUN ALL TESTS =====================
if __name__ == '__main__':
    print("🍳 justcookdaily.com — Workflow Test Script")
    print("=" * 60)
    
    # Step 1: RSS
    raw_xml, feed_url = test_rss_feeds()
    
    # Step 2: Parse
    selected_article = test_parse_rss(raw_xml)
    
    # Step 3: Gemini
    gemini_result = test_gemini(selected_article)
    
    # Step 4: Pexels
    if gemini_result:
        test_pexels([gemini_result['query1'], gemini_result['query2'], gemini_result['query3']])
    else:
        print("\n  ⚠️ Skipping Pexels test (no Gemini output)")
    
    # Step 5: WordPress
    test_wordpress()
    
    # Final Summary
    step_separator("FINAL SUMMARY")
    print(f"  RSS Feed:    {'✅' if raw_xml else '🔴'}")
    print(f"  RSS Parse:   {'✅' if selected_article else '🔴'}")
    print(f"  Gemini Pro:  {'✅' if gemini_result and gemini_result.get('has_content') else '🔴'}")
    print(f"  Pexels API:  {'✅' if gemini_result else '⏭️ skipped'}")
    print(f"  WordPress:   {'(tested above)'}")
    
    if gemini_result and gemini_result.get('has_content'):
        print(f"\n  🎉 ALL SYSTEMS GO! Workflow should produce full articles.")
        print(f"  📝 Generated title: \"{gemini_result['title'][:60]}\"")
        print(f"  📊 Word count: ~{gemini_result['word_count']}")
    else:
        print(f"\n  🔴 ISSUES FOUND — check the failed steps above.")
