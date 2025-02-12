from datetime import datetime
import platform
import io
import csv
from src import getFollowerList, getLikersList
from apify import Actor

def get_current_timestamp():
    """
    Get current timestamp (cross-platform).
    """
    current_datetime = datetime.now()
    if platform.system() == "Windows":
        return current_datetime.strftime('%#m-%d-%Y_%#I-%M-%p')
    else:
        return current_datetime.strftime('%-m-%d-%Y_%-I-%M-%p')

async def main():
    # Initialize the actor
    await Actor.init()

    # Get input from Apify
    input = await Actor.get_input()
    scraper_type = input.get('scraperType')

    print("--------------------", input)

    if not scraper_type:
        raise ValueError('scraperType parameter is required')

    current_timestamp = get_current_timestamp()
    result = []
    filename = ""

    if scraper_type == '1':  # Company Followers Scraper
        company_url = input.get('companyUrl')
        follower_number = input.get('followerNumber')

        if not company_url or not follower_number:
            raise ValueError('Missing required parameters for company scraper')

        company_id = company_url.split('/')[4]
        followers_info = getFollowerList(company_id, follower_number, current_timestamp)

        if not followers_info:
            raise ValueError('No data found')

        result = followers_info
        filename = f'followers_data_{current_timestamp}.csv'

    elif scraper_type == '2':  # Post Like Scraper
        post_url = input.get('postUrl')

        if not post_url:
            raise ValueError('Missing postUrl for post-like scraper')

        likers_info = getLikersList(post_url, current_timestamp)

        if not likers_info:
            raise ValueError('No data found')

        result = likers_info
        filename = f'likers_data_{current_timestamp}.csv'

    else:
        raise ValueError('Invalid scraper type')

    # Convert data to CSV format
    if isinstance(result, list) and len(result) > 0 and isinstance(result[0], dict):
        output = io.StringIO()
        csv_writer = csv.DictWriter(output, fieldnames=result[0].keys())
        csv_writer.writeheader()
        csv_writer.writerows(result)
        csv_data = output.getvalue()
        output.close()

        # Save output to Apify key-value store
        await Actor.set_value(filename, csv_data, content_type='text/csv')

        # Return the filename and CSV data
        await Actor.push_data({"filename": filename, "csvData": csv_data})

    else:
        raise ValueError('Unexpected data format')

# Run the main function
Actor.main(main)