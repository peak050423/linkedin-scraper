import requests
from .cookie_loader import load_cookies
from concurrent.futures import ThreadPoolExecutor, as_completed

cookies = load_cookies('linkedin_cookies.json')

headers = {
    "accept": "application/vnd.linkedin.normalized+json+2.1",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "en-US,en;q=0.9",
    "csrf-token": "ajax:4048042056122993237",  # Replace with the actual CSRF token
    "referer": "https://www.linkedin.com/company/71658149/admin/analytics/followers/",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
    "x-li-lang": "en_US",
    "x-restli-protocol-version": "2.0.0",
}

def fetch_data(url):
    """
    Fetch data from the provided URL using requests.
    """

    response = requests.get(url, cookies=cookies, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch data. Status Code: {response.status_code}")
        return None

def fetch_multiple_data(urls, follower_number):
    """
    Fetch data concurrently from multiple URLs.
    """
    results = {}
    i = 1
    with ThreadPoolExecutor(max_workers=8) as executor:  # You can adjust max_workers based on your requirements
        future_to_url = {executor.submit(fetch_data, url): url for url in urls}
        for future in as_completed(future_to_url):
            print(f"Fetch user profile {i}/{follower_number}")
            url = future_to_url[future]
            try:
                data = future.result()
                results[url] = data
            except Exception as e:
                print(f"Error fetching data from {url}: {e}")
                results[url] = None
            i += 1
    return results    

def get_page_source(url):
    """
    Fetch data from the provided URL using requests.
    """

    response = requests.get(url, cookies=cookies, headers=headers)
    
    if response.status_code == 200:
        return response
    else:
        print(f"Failed to fetch data. Status Code: {response.status_code}")
        return None
    
