
#pip install requests beautifulsoup4

import requests
from bs4 import BeautifulSoup
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_project_details(detail_url):
    detail_page = requests.get(detail_url, verify=False)
    detail_soup = BeautifulSoup(detail_page.content, 'html.parser')

    project_details = {}
    project_details['GSTIN No'] = detail_soup.find('span', id='ContentPlaceHolder1_lblGSTIN').text.strip()
    project_details['PAN No'] = detail_soup.find('span', id='ContentPlaceHolder1_lblPAN').text.strip()
    project_details['Name'] = detail_soup.find('span', id='ContentPlaceHolder1_lblPromoterName').text.strip()
    project_details['Permanent Address'] = detail_soup.find('span', id='ContentPlaceHolder1_lblPermAddress').text.strip()

    return project_details

def scrape_projects():
    url = 'https://hprera.nic.in/PublicDashboard'
    page = requests.get(url, verify=False) 
    soup = BeautifulSoup(page.content, 'html.parser')

    project_links = []
    for link in soup.find_all('a', href=True, string='RERA No', limit=6):
        project_links.append(link['href'])

    project_details_list = []
    for link in project_links:
        detail_url = 'https://hprera.nic.in/' + link
        project_details = get_project_details(detail_url)
        project_details_list.append(project_details)

    return project_details_list

if __name__ == '__main__':
    projects = scrape_projects()
    for i, project in enumerate(projects, 1):
        print(f"Project {i}:")
        for key, value in project.items():
            print(f"{key}: {value}")
        print("\n")