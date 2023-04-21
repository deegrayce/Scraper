import requests
from bs4 import BeautifulSoup

def request_github_trending(url):
    response = requests.get(url)
    return response.content

def extract(page):
    soup = BeautifulSoup(page, 'html.parser')
    repository_rows = soup.find_all('li', class_='repo-list-item')
    return repository_rows

def transform(html_repos):
    repositories_data = []
    for rep in html_repos:
        developer = rep.find('span', class_='text-normal').text.strip()
        repository_name = rep.find('h3').text.strip()
        nbr_stars = rep.find('a', class_='muted-link').text.strip()
        repositories_data.append({'developer': developer, 'repository_name': repository_name, 'nbr_stars': nbr_stars})
    return repositories_data

import csv
def format(repositories_data):
    csv_data = [['Developer', 'Repository Name', 'Number of Stars']]
    for rep in repositories_data:
        csv_data.append([rep['developer'], rep['repository_name'], rep['nbr_stars']])
    csv_string = "\n".join([",".join(row) for row in csv_data])
    return csv_string

def main():
    url = "https://github.com/trending"
    page = request_github_trending(url)
    repositories = extract(page)
    repositories_data = transform(repositories)
    csv_data = format(repositories_data)
    filename = "github_trending_repositories.csv"
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(csv_data)
    print(f"Data written to {filename}")

#if _name_ == '_main_':
    #main()
