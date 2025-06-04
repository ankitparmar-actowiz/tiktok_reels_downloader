from requests.exceptions import RequestException
import requests, threading, os, json, time
from http.client import IncompleteRead

cookies = {
    # paste your cookies here!!
}

headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'priority': 'u=1, i',
    'referer': 'https://www.tiktok.com/search/video?q=fashion%20outfits&t=1748935806394',
    'sec-ch-ua': '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
}

INPUT_FILE = "tiktok_data.json"
SAVE_FOLDER = "Videos"
MAX_RETRIES = 10

os.makedirs(SAVE_FOLDER, exist_ok=True)

session = requests.Session()

def download_video(video_data):
    url = video_data['video_url']
    video_name = video_data['video_name'] + ".mp4"
    save_path = os.path.join(SAVE_FOLDER, video_name)

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = session.get(url, headers=headers, cookies=cookies, stream=True, timeout=30)
            response.raise_for_status()

            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)

            print(f"[+] Downloaded: {video_name}")
            return  # Success

        except IncompleteRead as e:
            print(f"[!] IncompleteRead on {video_name}, attempt {attempt}/{MAX_RETRIES} — retrying...")
        except RequestException as e:
            print(f"[!] Request error on {video_name}, attempt {attempt}/{MAX_RETRIES} — {e}")
        except Exception as e:
            print(f"[!] Failed {video_name} on attempt {attempt}/{MAX_RETRIES} — {e}")

        time.sleep(2 ** attempt)  # Exponential backoff

    print(f"[X] Giving up on: {video_name} after {MAX_RETRIES} attempts.")

# Load video list
with open(INPUT_FILE, 'r', encoding='utf-8') as f:
    video_list = json.load(f)

# Launch threads
threads = []
for video in video_list:
    t = threading.Thread(target=download_video, args=(video,))
    t.start()
    threads.append(t)

for t in threads:
    t.join()

print("✅ All downloads complete.")
