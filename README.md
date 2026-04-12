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

### 4. 🌐 Smart & AdSense-Compliant Linking Architecture
- **Inbound Linking Retention:** Updated to dynamically inject exactly **2 internal links** to relevant JustCookDaily categories, optimizing for crawl depth without over-optimizing.
- **Strict Outbound Authority:** Now strictly references a maximum of **2 high-authority scientific or research-based sources** (e.g., USDA, Harvard Nutrition, or scientific journals) to build topical authority and trustworthiness while removing all competitor recipe blog links.

### 5. 🏛️ Dual-Source Image Integration (Pexels + Wikimedia)
The workflow now employs a multi-source image strategy to enhance AdSense approval chances and provide educational value.
- **Wikimedia Commons Integration:** Dynamically fetches historical or botanical images from Wikimedia Commons for certain sections, providing food science context.
- **Copyright & Attribution Engine:** Automatically generates and appends mandatory license and credit information for every Wikimedia image used, ensuring 100% legal compliance.
- **High-Resolution Pexels Shots:** Continues to use Pexels for high-quality food photography (hero, ingredient, and process shots).

## 📊 AdSense & E-E-A-T Optimization (Recent Updates)
The system has been specifically overhauled to meet Google AdSense's strict quality guidelines:
- **E-E-A-T Focus:** Gemini prompts now mandate the inclusion of **Food Science** (molecular changes during cooking) and **Historical Context** (origins of dishes) to demonstrate expertise and authoritativeness.
- **Human-Centric Tone:** Specific filters remove generic AI phrases and "AdSense-seeking" language, resulting in more natural, first-person-style narratives.
- **Length & Depth:** Articles are structured to be between **1,500 and 2,000+ words**, exceeding the average recipe blog post depth.

## ⚙️ How to Deploy Flow to n8n
1. Navigate to your n8n workspace.
2. Select **Add Workflow**.
3. Choose **Import from File...** and upload the main `.json` file (`justcookdaily.com — Gemini Google Trends Auto Blog_ — Expiry Date_ 11 April 2027 (Valid for 1 year) — Buyer_ dalfins33.json`).
4. **Ensure Credentials:** Update the `Build Config` node with your active API keys (`Pexels`, `Gemini`, `WordPress`, and `Wikimedia` if applicable).
5. Set the Master Switch to **Active**. The system is mapped to run automatically at **10:00 AM** and **4:30 PM (Kyiv Time)** every single day.

## 🧪 Local Testing Suite
A Python simulator script (`test_workflow.py`) has been included in the repository. This enables developers to test the upstream API connections outside of the n8n environment without publishing directly to WordPress.
- Run `python test_workflow.py` to trigger an end-to-end simulation covering RSS Fetching, Prompt Injection, Gemini Article generation, and Pexels/Wikimedia integration.

---
*Maintained Exclusively for JustCookDaily.*

