# TikTok Video Scraper & Downloader

This project provides two Python scripts to **scrape TikTok videos by keyword** and **download them** in bulk using multithreading. It uses TikTok's internal APIs and handles retries, unique video detection, and JSON export of metadata.

---

## Note: Add your login cookies to all python files.

## 📁 Files Overview

### 1. `tiktok_extract_links.py`
This script:
- Paste Your Downloaded Cookies Here First.
- In Search Function you can add total_results as total videos per search.
- You can add multiple keywords in keywords list.
- Saves the structured video metadata into a JSON file: `tiktok_data.json`.

### 2. `tiktok_extract_data.py`
This script:
- Paste your Downloaded cookies here too.
- It Will Read the `tiktok_data.json` video link and videoname.
- Downloads all videos using multithreaded requests with retry logic.
- Saves all searched videos into the `Videos/` folder.

---

## ⚙️ Requirements

- Python 3.7+
- `requests`

Install the dependencies:

```bash
pip install requests
