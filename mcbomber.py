import requests
from bs4 import BeautifulSoup
import re

# input url
url = input('Enter URL to scrape: ')

# type check
if 'myanimelist' in url:
    print('Detected MyAnimeList page. Initializing...')
    title_tag = 'div'
    title_attr = {'class': 'title'}
    title_selector = 'a'
    link_prefix = 'https://osu.ppy.sh/beatmapsets?q='
    regex = r'https?://myanimelist\.net/anime/producer/(\d+)/?.*'
    match = re.match(regex, url)
    if match:
        url = f'https://myanimelist.net/anime/producer/{match.group(1)}'
    else:
        print('Please input a valid URL.')
        exit()
elif 'vndb' in url:
    print('Detected VNDB page. Initializing...')
    title_tag = 'tr'
    title_attr = {'class': 'vn'}
    title_selector = 'td > a'
    link_prefix = 'https://osu.ppy.sh/beatmapsets?q='
    regex = r'https?://vndb\.org/p(\d+)/?.*'
    match = re.match(regex, url)
    if match:
        url = f'https://vndb.org/p{match.group(1)}'
    else:
        print('Please input a valid URL.')
        exit()
else:
    print('Please input a valid URL.')
    exit()

# set agent
headers = {'User-Agent': 'Mozilla/5.0'}

# its scrapin' time
response = requests.get(url, headers=headers)
html_content = response.content
soup = BeautifulSoup(html_content, 'html.parser')
titles = []
for title_elem in soup.find_all(title_tag, title_attr):
    title = title_elem.select_one(title_selector).text
    if not any(title.startswith(t) and len(title) > len(t) for t in titles):
        titles.append(title)

# generate the list
with open('deathnote.txt', 'w', encoding='utf-8') as f:
    for title in titles:
        link_title = '%22' + title.replace(' ', '%20') + '%22'
        link = link_prefix + link_title + '&s=any\n'
        f.write(link)

# (optional) generate e-mail template
convert_to_dmca = input('Do you want to convert the list to a DMCA takedown request? (Y/N)').lower()

if convert_to_dmca == 'y':
    with open('deathnote.txt', 'r') as f:
        links = f.readlines()
    dmca_text = 'こんにちは。この度、「osu.ppy.sh」というフォーラムで、貴社のライセンスコンテンツが無断で使用されていることが判明しました。\n\nこのリンク先には、以下のコンテンツが掲載されています。\n'
    dmca_text += '\n'.join([f'{i+1}. {link.strip()}' for i, link in enumerate(links)])
    dmca_text += '\n\n以上、未許可のコンテンツをご紹介しました。おそらくもっとあると思います。\n\nご面倒をおかけいたしますが、よろしくお'
    with open('template.txt', 'w', encoding='utf-8') as f:
            f.write(dmca_text)
    print('Happy hunting.')
