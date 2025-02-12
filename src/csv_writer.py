import csv

def write_to_csv(data, user_choice, current_timestamp):
    """
    Write data to a CSV file.
    """
    if not data:
        print("No data to write to CSV.")
        return

    fieldnames = ['fullName', 'jobTitle', 'profileUrl', 'imageUrl', 'connectionDegree', 'followedAt', 'timestamp']
    filename = ''

    if user_choice == '1': 
        # fieldnames.append()
        filename = f'followers_data_{current_timestamp}.csv'
    elif user_choice == '2':
        fieldnames = ['fullName', 'jobTitle', 'profileUrl', 'imageUrl', 'connectionDegree', 'timestamp']
        filename = f'likers_data_{current_timestamp}.csv'
    
    # Include all positions as columns
    for row in data:
        for key in row.keys():
            if key.startswith('positions/') and key not in fieldnames:
                fieldnames.append(key)

    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

    print(f"Data saved to {filename}")

# Note: Ensure this script is in the correct directory or update the import statement in main.py accordingly
