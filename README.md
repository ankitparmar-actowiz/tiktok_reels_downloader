# TikTok Video Scraper & Downloader

This project provides two Python scripts to **scrape TikTok videos by keyword** and **download them** in bulk using multithreading. It uses TikTok's internal APIs and handles retries, unique video detection, and JSON export of metadata.

---

## 📁 Files Overview

### 1. `tiktok_extract_links.py`
This script:
- Scrapes TikTok search results for a list of keywords.
- Extracts download URLs, video duration, names, and ranks.
- Saves the structured video metadata into a JSON file: `tiktok_data.json`.

### 2. `tiktok_extract_data.py`
This script:
- Reads from `tiktok_data.json`.
- Downloads all videos using multithreaded requests with retry logic.
- Saves videos into the `Videos/` folder.

---

## ⚙️ Requirements

- Python 3.7+
- `requests`

Install the dependencies:

```bash
pip install requests
