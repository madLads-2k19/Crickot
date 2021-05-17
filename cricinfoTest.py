from bs4 import BeautifulSoup
import requests

URL = "https://www.espncricinfo.com/series/county-championship-2021-1244186/glamorgan-vs-yorkshire-group-3-1244261/full-scorecard"
page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser')

match = soup.find_all('div', class_ = 'match-header')
match = match[0]

team_names = match.find_all('p', class_ = 'name')
scores = match.find_all('span', class_ = 'score')
for (team_name, score) in zip(team_names, scores):
    print(team_name.text, ":", score.text)