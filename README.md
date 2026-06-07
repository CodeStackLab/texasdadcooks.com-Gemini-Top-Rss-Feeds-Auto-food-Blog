# texasdadcooks.com — Gemini Top Rss Feeds Auto food Blog

This repository contains the advanced n8n automated blogging workflow for [texasdadcooks.com](https://texasdadcooks.com).

## 🚀 Key Features

*   **Gemini 2.5 Flash**: High-quality, food-science-backed article generation ($8,000 token limit).
*   **Duplicate Protection**: Real-time checking against the last 100 WordPress posts + workflow memory (History) to ensure 100% unique content.
*   **100+ Evergreen Fallbacks**: Massive library of unique cooking topics to use when RSS feeds are empty.
*   **Pexels Integration**: High-resolution (1200x630) images with automatic copyright attribution.
*   **Category Rotation**: Automatic round-robin rotation through all 10 site categories.
*   **Smart Slugs**: Clean, SEO-optimized URLs without word truncation.

## 🛠️ Setup Instructions

1.  **Import Workflow**: Download `workflow_sanitized.json` and import it into your n8n instance.
2.  **Configure Credentials**:
    *   Open the **⚙️ SETUP** node.
    *   Replace the placeholders in the `value` fields with your actual API keys:
        *   `gemini_api_key`: Google AI Studio key.
        *   `mistral_api_key`: Mistral AI key.
        *   `pexels_api_key`: Pexels API key.
        *   `wp_app_password`: WordPress Application Password.
        *   `wp_url`: Your site URL (e.g., `https://texasdadcooks.com`).
3.  **Run**: Set your triggers (e.g., every 6 hours) and enjoy automated, high-quality blogging!

---
*Created by Antigravity (Advanced Agentic AI)*


* **Litecoin (LTC) Address:** `LaJGvzQJGmqfCFkP9cY1kjLp6hphECxWS2` (Network: LTC / Litecoin)