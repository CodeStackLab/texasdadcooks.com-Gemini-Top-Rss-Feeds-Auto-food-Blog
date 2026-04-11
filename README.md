# 🍳 JustCookDaily — Advanced AI Autoblog Automation

This private repository contains the highly advanced, fully automated **n8n workflow** powering the recipe blog [JustCookDaily.com](https://justcookdaily.com/).

This workflow is an enterprise-grade AI automation system that completely autonomous long-form (2,000–2,500 words), highly SEO-optimized cooking articles directly from live RSS feeds. 

## 🚀 Advanced Core Features

### 1. 🔄 Intelligent RSS Feed Rotation Engine
Rather than relying on generic topic generators or single sources, the workflow utilizes a custom **Feed Rotation Engine**. It actively scrapes from a curated list of over **25+ authority cooking blogs** (e.g., Serious Eats, Bon Appétit, AllRecipes).
- **Randomized Rotation:** Each run dynamically selects a different premium feed.
- **Deduplication:** Prevents publishing the same recipe topic within a 60-day rolling window using n8n's global workflow static data.

### 2. 🧠 Gemini 2.5 Flash Autonomous Writer
The workflow deeply integrates with Google's latest **Gemini 2.5 Flash AI model**. 
- **100% Original Content Generation:** It doesn't summarize the RSS feed; it reads the topic and writes an entirely new, 2,500-word authoritative guide from scratch.
- **Strict SEO Structure Enforcement:** Enforces rigorous Markdown outputs, ensuring the presence of Titles, Slugs, Meta Descriptions, Categories (mapped to WP IDs), diverse Tags, compelling Excerpts, multiple `<h2>` and `<h3>` tags, and contextual FAQs.
- **Robust Markdown Parsing:** A custom-built, fail-safe parser automatically cleans and interprets Gemini's markdown deviations to prevent data loss.

### 3. 🖼️ Contextual & Deduplicated Pexels Imagery
Visually stunning content requires gorgeous imagery. The workflow integrates with the **Pexels API** in a highly context-aware manner.
- **Multi-Injection:** Seamlessly embeds three high-resolution images natively into the flow of the article: 
    1. A beautiful finished-plate hero shot.
    2. A fresh, raw ingredient laydown.
    3. An active cooking process action shot.
- **Global Memory Deduplication:** Specifically engineered with an active tracker/Set inside the logic execution. It actively checks previous image IDs fetched *during the execution loop* to **guarantee no duplicate images ever appear** on the same post, even for identical API search queries.

### 4. 🌐 Smart Linking Architecture
- **Inbound Linking Retention:** The workflow dynamically injects 3-4 internal links to other JustCookDaily category pages strategically within the body text to reduce bounce rate and pass SEO link juice.
- **Outbound Authority Links:** Strategically references high-authority websites (like The Kitchn or Food Network) within the articles to build topical authority and trustworthiness.

## ⚙️ How to Deploy Flow to n8n
1. Navigate to your n8n workspace.
2. Select **Add Workflow**.
3. Choose **Import from File...** and upload the main `.json` file (`justcookdaily.com — Gemini Google Trends Auto Blog_ — Expiry Date_ 11 April 2027 (Valid for 1 year) — Buyer_ dalfins33.json`).
4. **Ensure Credentials:** Update the `Build Config` node with your active API keys (`Pexels`, `Gemini`, `WordPress`).
5. Set the Master Switch to **Active**. The system is mapped to run automatically at **10:00 AM** and **4:30 PM (Kyiv Time)** every single day.

## 🧪 Local Testing Suite
A Python simulator script (`test_workflow.py`) has been included in the repository. This enables developers to test the upstream API connections outside of the n8n environment without publishing directly to WordPress.
- Run `python test_workflow.py` to trigger an end-to-end simulation covering RSS Fetching, Prompt Injection, Gemini Article generation, and Pexels integration.

---
*Maintained Exclusively for JustCookDaily.*
