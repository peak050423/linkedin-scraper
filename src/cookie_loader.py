import json

def load_cookies(file_path='linkedin_cookies.json'):
    """
    Load cookies from a JSON file and return as a dictionary.
    """
    with open(file_path, 'r') as file:
        linkedin_cookies = json.load(file)
    
    
    cookies = {cookie['name']: cookie['value'] for cookie in linkedin_cookies}
    return cookies
