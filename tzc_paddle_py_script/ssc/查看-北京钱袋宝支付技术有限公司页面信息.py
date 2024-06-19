import requests

# Replace these with your actual cookies and headers
cookies = {
    'your_cookie_name': 'your_cookie_value',
    # Add other cookies if necessary
}

headers = {
    'User-Agent': 'your_user_agent',
    'Accept': 'your_accept_header',
    # Add other headers if necessary
}


def fetch_company_info( cookies, headers):
    url = f'https://www.sscha.com'
    # print(f"Fetching info for company ID: {company_id}")  # Debugging line
    print(f"Headers: {headers}")  # Debugging line

    response = requests.get(url, cookies=cookies, headers=headers, verify=False)

    if response.status_code == 200:
        return response.text
    else:
        # print(f"Failed to fetch data for company ID: {company_id}. Status code: {response.status_code}")
        return None


def save_html_content(html_content, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(html_content)

    print(f"HTML content saved to {file_path}")


if __name__ == "__main__":
    # company_id = '2ed712d1e2a1fd0e0013adc4ef40b75d'
    html_content = fetch_company_info( cookies, headers)

    if html_content:
        output_file = f"search_info.html"
        save_html_content(html_content, output_file)
    else:
        print("No content to save.")
