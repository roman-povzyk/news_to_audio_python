import requests
from bs4 import BeautifulSoup
from gtts import gTTS

filename = "article_ukrpravda.txt"
URL_UKRPRAVDA = 'https://www.pravda.com.ua/'
HEADERS_UKRPRAVDA = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
}


def get_html(url, params=''):
    r = requests.get(url, headers=HEADERS_UKRPRAVDA, params=params)
    return r


def get_content(html):
    number_articles = int(input('Скільки заголовків хочеш прослухати: ')) + 1
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='article_news')
    cards = []

    i = 0
    for item in items:
        i += 1
        if i < number_articles:
            cards.append(
                    {
                        f'Заголовок {i}': item.find('div', class_='article_header').get_text()
                    }
                )
    return cards

def parser():
    html = get_html(URL_UKRPRAVDA)
    if html.status_code == 200:
        cards = []
        cards.extend(get_content(html.text))
        with open(filename, 'w') as file:
            file.write(str(cards))
        print("Записую всі заголовки до файлу.")
    else:
        print('Error')

parser()

with open(filename, "r") as file:
    text = file.read()

print("Начитую всі заголовки.")
obj = gTTS(text, lang="uk")
obj.save("article_ukrpavda.mp3")
print('Заголовки «УП» готові до прослуховування')