from concurrent.futures import ThreadPoolExecutor, as_completed
import json, os, requests, time
import hashlib

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

def download_video(url: str, output_path: str):
    try:
        response = requests.get(url, stream=True, headers=headers, cookies=cookies)
        response.raise_for_status()

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        time.sleep(1)
        print(f"Video downloaded to: {output_path}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error downloading video: {e}")
        return False

def search(keyword, allLinks, total_results=100):
    scrappedUniqueReelsID = []
    offset = 0
    counter = 0
    allData = []
    scrapped = 0

    while True:
        time.sleep(1)
        response = requests.get(
            f'https://www.tiktok.com/api/search/item/full/?WebIdLastTime=1747628831&aid=1988&app_language=en&app_name=tiktok_web&browser_language=en-US&browser_name=Mozilla&browser_online=true&browser_platform=Win32&browser_version=5.0%20%28Windows%20NT%2010.0%3B%20Win64%3B%20x64%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F137.0.0.0%20Safari%2F537.36&channel=tiktok_web&cookie_enabled=true&count=20&data_collection_enabled=true&device_id=7506008648200537642&device_platform=web_pc&focus_state=false&from_page=search&history_len=9&is_fullscreen=false&is_page_visible=true&keyword={keyword}&odinId=7511597799822771231&offset={offset}&os=windows&priority_region=US&referer=&region=US&root_referer=https%3A%2F%2Fwww.tiktok.com%2Fsearch%2Fuser%3Fq%3Dfashion%26t%3D1748930152019&screen_height=768&screen_width=1366&search_id=20250603090626A19FF51A0D04F1007A8F&tz_name=Asia%2FCalcutta&user_is_login=true&verifyFp=verify_mbg3vl6v_ibbPFxpT_fwFM_49sH_8VGt_GYnYe1RFiFP7&web_search_code=%7B%22tiktok%22%3A%7B%22client_params_x%22%3A%7B%22search_engine%22%3A%7B%22ies_mt_user_live_video_card_use_libra%22%3A1%2C%22mt_search_general_user_live_card%22%3A1%7D%7D%2C%22search_server%22%3A%7B%7D%7D%7D&webcast_language=en&msToken=d2iICDIjIIGWQ5nklnA1fT0Ha1ea9RT2eVT7_5Lvzu3F7XSQoGcr1UdooFOGpjIbW5GgNL81tNJL2KwCHz9F2OrsYnUqrbtK_s3OSeyHS8lr_c8rylp3etqxkOObCLATOpuJzF0pTJbJcO8zwh6uplA=&X-Bogus=DFSzswVYRvsANJJeCVTeAuhPmkvz&X-Gnarly=MFDtu4fmQRR2J0JD9No/eoumEL6blL3Y8xfHw/O/i2o9nGKmToys6M63f3U-5Xbm9USEFxh28UQJ2TJ-WfyIhZvb5vS0DIvh-R9eg3k9WsoX6MF27mv54bVtHxX1kGcqM838CHiIcx0Nzdx23-HGhw3E-R/Pbv79nEPz2cDh/lQdCcaVCfMO-PHy5Tf3M4Eg7-aEiooPV0lC9qSrth1J0P-oVlswCxFRsB8Aq1LGiMBAHnjWRzFqcpp80wex7jutJYWppv/9GKyb',
            cookies=cookies,
            headers=headers,
        )

        print(response.status_code)
        json_data = response.json()
        offset = json_data.get('cursor')
        counter += len(json_data.get('item_list', []))
        # print('counter: ', counter)

        for item in json_data.get('item_list', []):
            duration = item.get('video').get('duration')
            try:
                downloadAddr = item.get('video').get('downloadAddr')
            except:
                try:
                    downloadAddr = item.get('video').get('playAddr')
                except:
                    try:
                        downloadAddr = item.get('video').get('bitrateInfo', [])[0].get('PlayAddr').get('UrlList')[0]
                    except:
                        downloadAddr = ''

            if not downloadAddr:
                # print('Not found Video URL') 
                continue
            videoUID = item.get('video').get('bitrateInfo', [])[0].get('PlayAddr').get('UrlKey')
            videoFilename = hashlib.sha256(downloadAddr.encode()).hexdigest()
            if videoUID in scrappedUniqueReelsID:
                print('Duplicate video reels found!!')
                downDupVideo += 1
                break
            else:
                scrapped += 1
                print('scrapped: ', scrapped)
                allLinks[downloadAddr] = videoFilename

            rowData = {}
            rowData['rank'] = scrapped
            rowData['keyword'] = keyword
            rowData['video_length'] = duration
            rowData['video_url'] = downloadAddr.replace('v16-webapp-prime.us.tiktok.com', 'v19-webapp-prime.us.tiktok.com')
            rowData['video_name'] = f"{videoFilename}_{keyword}"
            rowData['meesho_product_url'] = 'N/A'
            rowData['source'] = 'Tik-Tok'
            allData.append(rowData)

            if scrapped >= total_results:
                break  

        if scrapped >= total_results:
            break  

    return allData

keywords = ["gadgets", "coolgadgets", "storage", "usefulgadgets", "homeproducts"]

allLinks = {}
mainData = []
for keyword in keywords:
    print(keyword)
    nameList = search(keyword, allLinks)
    mainData.extend(nameList)

with open("tikok_data.json", "w", encoding="utf-8") as f:
    json.dump(mainData, f, ensure_ascii=False, indent=4)