import requests
from bs4 import BeautifulSoup
from gtts import gTTS

filename = "article_polt.txt"
HOST = 'https://poltava.to/'
URL = 'https://poltava.to/news/'
HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
}


def get_html(url, params=''):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='stream-block-content')
    cards = []

    for item in items:
        cards.append(
            {
                'Заголовок': item.find('h2', class_='stream-block-title').get_text()
            }
        )
    return cards

def parser():
    PAGENATION = int(input("К-ть сторінок для парсингу: "))
    html = get_html(URL)
    if html.status_code == 200:
        cards = []
        for page in range(1, PAGENATION+1):
            print(f'Паршу сторінку: {page}')
            html = get_html(URL, params={'page': page})
            cards.extend(get_content(html.text))
            with open(filename, 'w') as file:
                file.write(str(cards))
    else:
        print('Error')


parser()

with open(filename, "r") as file:
    text = file.read()

obj = gTTS(text, lang="uk")
obj.save("article_polt.mp3")
print("Заголовки готові до прослуховування")