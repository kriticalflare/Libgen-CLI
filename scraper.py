import requests
from bs4 import BeautifulSoup as bs4
import bookModel

# http://gen.lib.rus.ec/search.php?req=animal+farm&lg_topic=libgen&open=0&view=simple&res=25&phrase=1&column=def
searchterm = input('Enter the title of the book you want to search: ')
result = requests.get('http://gen.lib.rus.ec/', params={'req': searchterm})

# print(result.status_code)
# print(result.headers)

if result.status_code != 200:
    print('Something went wrong! Try again later')
    quit()

source = result.content
soup = bs4(source, 'html5lib')
table = soup.find('table', class_='c')
rows = table.find_all('tr')


books = []

mirrors = ['Gen.lib.rus.ec', 'Libgen.lc',
           'Z-Library', 'Libgen.pw', 'BookFI.net']

for row in rows:
    links = row.find_all('a')
    mirrorcount = 0
    book = bookModel.Book()
    downloads = []
    for link in links:
        title_text = None
        try:
            title = link.attrs['title']
            if title == '':
                title_text = link.text
                book.book_title = title_text

            elif title in mirrors:
                download_link = link.attrs['href']
                mirrorcount += 1
                downloads.append(download_link)
            book.mirror_list = downloads
        except KeyError:
            pass
    books.append(book)

print('RESULTS: \n\n')

if len(books) == 1:
    print('No results Found!')
    quit()
result_count = 0
for b in books:
    t = b.book_title
    if t is not None:
        result_count += 1
        print(f'{result_count}. {t}')

index = input('Enter the book number you want to download: ')
index = int(index)
if index <= len(books):
    mirrorindex = 0
    l = books[index - 1].mirror_list
    for m in l:
        mirrorindex += 1
        print(f'{mirrorindex }. {m}')
