import requests

BASE_URL = 'http://127.0.0.1:8000/'  # Replace with your actual API base URL

def login(username, password):
    url = BASE_URL + 'api/login/'
    data = {'username': username, 'password': password}
    response = requests.post(url, data=data)
    if response.status_code == 200:
        print("Login successful!")
        return True
    else:
        print("Login failed:", response.text)
        return False

def post_story(username, password, headline, category, region, details):
    url = BASE_URL + 'api/stories/'
    data = {
        'username': username,
        'password': password,
        'headline': headline,
        'category': category,
        'region': region,
        'details': details
    }
    headers = {}  # Include authentication token or session information here
    response = requests.post(url, data=data, headers=headers)
    if response.status_code == 201:
        print("Story posted successfully!")
    else:
        print("Failed to post story:", response.text)

def logout():
    url = BASE_URL + 'api/logout/'
    response = requests.post(url)
    if response.status_code == 200:
        print("Logged out successfully!")
        return True
    else:
        print("Failed to logout: ", response.text)
        return False

def get_stories(story_cat='*', story_region='*', story_date='*'):
    url = BASE_URL + 'api/get_stories/'
    params = {
        'story_cat': story_cat,
        'story_region': story_region,
        'story_date': story_date
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        stories = response.json().get('stories')
        for story in stories:
            print(story)  # Process the retrieved stories as needed
    else:
        print("Failed to get stories:", response.text)

def delete_story(username, password, key):
    url = BASE_URL + f'api/stories/{key}/'
    response = requests.delete(url, headers={'Username': username, 'Password': password})
    if response.status_code == 200:
        print("Story deleted successfully!")
    else:
        print(f"Failed to delete story: {response.status_code} - {response.text}")

def register_agency(agency_name, url, agency_code):
    url = BASE_URL + 'api/directory/register/'
    data = {
        'agency_name': agency_name,
        'url': url,
        'agency_code': agency_code
    }
    response = requests.post(url, json=data)
    if response.status_code == 201:
        print("Agency registered successfully!")
    else:
        print("Failed to register agency:", response.text)

def list_agencies():
    url = BASE_URL + 'api/directory/list/'
    response = requests.get(url)
    if response.status_code == 200:
        agencies = response.json().get('agency_list')
        for agency in agencies:
            print(agency)  # Process the retrieved agencies as needed
    else:
        print("Failed to get agency list:", response.text)

def unregister_agency():
    print("To unregister a company from the directory, please contact the directory admin.")

def main():
    username = 'rohan'
    password = 'test123'

    if login(username, password):
        while True:
            command = input("Enter a command (post, list, delete, logout, exit): ").strip().lower()

            if command == 'post':
                headline = input("Enter the headline: ")
                category = input("Enter the category: ")
                region = input("Enter the region: ")
                details = input("Enter the details: ")
                post_story(username, password, headline, category, region, details)

            elif command == 'list':
                get_stories(story_cat='*', story_region='uk', story_date='*')

            elif command == 'delete':
                key = int(input("Enter the story key: "))
                delete_story(username, password, key)

            elif command == 'logout':
                if logout():
                    username = 'x'
                    password = 'y'

            elif command == 'exit':
                logout()
                print("Exiting...")
                break

            else:
                print("Invalid command.")

if __name__ == "__main__":
    main()
