# 🍳 JustCookDaily — Advanced AI Autoblog Automation (v5)

This private repository contains the enterprise-grade **n8n workflow** powering [JustCookDaily.com](https://justcookdaily.com/). This system generates highly authoritative, AI-driven culinary content that meets strict Google AdSense and E-E-A-T guidelines.

---

## 🏗️ 1. Core Architecture & Pipeline
The workflow follows a linear, fail-safe pipeline from trend discovery to production deployment.

### 1.1 Trigger System
- **Dual-Schedule Triggers:** The system executes twice daily (10:00 AM and 04:30 PM Kyiv Time) to ensure a steady stream of fresh content.
- **Timezone Aware:** Configured for the Europe/Kyiv timezone.

### 1.2 Intelligent Topic Discovery (`Fetch Cooking RSS Feeds`)
- **Multi-Feed Rotation:** The system maintains a database of 50+ authority cooking feeds (e.g., Serious Eats, Bon Appétit, Simply Recipes).
- **Randomized Selection:** Each run shuffles the feed list and attempts to fetch the top 6. It selects the first one that successfully returns data.
- **Fallback Engine:** If all 50+ RSS feeds are down, the system utilizes a curated hard-coded pool of 40 high-intent evergreen cooking topics to ensure the blog never misses a post.

### 1.3 Deduplication & State Management
- **60-Day Rolling Window:** Uses n8n's Static Data to track every published topic. It prevents the same recipe from being processed twice within a two-month period.
- **Article Counter:** Tracks global publication count to trigger specific Call-to-Action (CTA) events every 20 articles.

---

## 🧠 2. The Content Engine (Gemini 2.5 Flash)
The "brain" of the operation uses advanced prompt engineering to move beyond standard AI summaries.

### 2.1 Prompt Strategy: E-E-A-T Optimization
The Gemini prompts are specifically engineered for:
- **Food Science Integration:** Mandates explanations of chemical processes like the Maillard Reaction, emulsification, and protein denaturation.
- **Historical Context:** Forces a dedicated section on the cultural and regional evolution of the dish.
- **Nutritional Expertise:** Includes specific data on vitamins, minerals, and caloric density from a "scientific authority" perspective.
- **Human Tone Filters:** Explicitly bans AI boilerplate phrases and forces the inclusion of personal expertise markers like *"One trick I discovered after years in the kitchen..."*

### 2.2 Output Structure
Gemini outputs a structured block containing:
- **SEO Title & Slug:** Optimized 8-12 word titles.
- **Metadata:** 130-155 character meta-descriptions.
- **Image Queries:** Structured search terms for Pexels and Wikimedia.
- **Semantic HTML:** Pure HTML structure including `<h2>`, `<h3>`, `<ul>`, and `<ol>` tags.

---

## 🖼️ 3. Visual & Media System
### 3.1 Dual-Source Imagery (Pexels + Wikimedia)
- **Pexels API:** Fetches 3 high-resolution inline images: (1) Finished Plate, (2) Raw Ingredients, (3) Action Shot.
- **Wikimedia Commons:** Used for historical or botanical imagery to add educational value.
- **Global Image Deduplication:** Tracks image IDs within the execution loop and across historical data to ensure no duplicate photos ever appear on the same post.

### 3.2 Automated Attribution Engine
- **Legal Compliance:** Every image is wrapped in a HTML `<figure>` and `<figcaption>` block.
- **Dynamic Credits:** Automatically formats the photographer's name, source (Pexels/Wikimedia), and a direct link to the license (CC BY-SA 4.0 or Pexels License).

---

## 🔗 4. SEO & Linking Logic
### 4.1 Internal Link Strategy
- **Constraint:** Maximum of 2 internal links per post.
- **Logic:** Randomly selects 2 relevant category pages from JustCookDaily.com to preserve internal link juice without appearing spammy.

### 4.2 Outbound Authority Links (AdSense Compliance)
- **Scientific Focus Only:** The system bans all external links to other recipe blogs.
- **Authority Sources:** Only 2 outbound links are allowed, sourced randomly from a whitelist of high-authority domains:
  - USDA FoodData Central
  - Harvard Nutrition Source
  - WHO
  - National Institutes of Health (NIH)
  - American Heart Association

### 4.3 Structural SEO
- **Table of Contents (TOC):** Dynamically generated at the top of every post with anchor links for better user navigation and Google "Jump-To" link indexing.
- **Semantic HTML5:** Uses proper heading hierarchy and standard tags, ensuring 100% crawlability.

---

## 🛠️ 5. How to Insert API Keys & Setup
To get the workflow running, you must configure your credentials in n8n.

1. **Import the Workflow:** Upload the `.json` file to your n8n instance.
2. **Locate the ⚙️ SETUP Node:** This is the first `Set` node in the workflow.
3. **Insert Keys:**
   - **Gemini API Key:** Get it from [Google AI Studio](https://aistudio.google.com/).
   - **Pexels API Key:** Get it from [Pexels API](https://www.pexels.com/api/).
   - **WordPress Details:**
     - **URL:** Your site URL (e.g., `https://justcookdaily.com`).
     - **User:** Your WP username.
     - **Application Password:** Create this in WordPress (Users -> Profile -> Application Passwords).
4. **Save & Activate:** Click "Save" and ensure the "Active" toggle is ON.

---

## 🧪 6. Testing & Maintenance
### `test_workflow.py`
This repository includes a Python simulation script that allows you to:
- Verify the RSS scraping logic.
- Test the Gemini prompt output without spending WordPress credits.
- Preview the image query logic.

> [!TIP]
> **Maintenance Tip:** All API keys and fundamental configurations (URL, User, Passwords) are centralized in the **⚙️ SETUP** node. If you change your WordPress password or rotate API keys, you only need to update them in that single node.

---
*Maintained Exclusively for JustCookDaily.*
