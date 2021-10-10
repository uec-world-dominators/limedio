import http.cookiejar
import requests
import bs4

from limedio.errors import LimedioLoginError


class LimedioLibrary():
    def __init__(self, prefix: str, cookies: http.cookiejar.CookieJar) -> None:
        self.session = requests.Session()
        self.session.cookies = cookies
        self.prefix = prefix

    def borrowing(self):
        url = f'{self.prefix}/opac/user/holding-borrowings'
        res = self.session.get(url)
        if res.status_code == 200 and res.url == url:
            html = res.text
            doc = bs4.BeautifulSoup(html, 'html.parser')
            books_elem = doc.select('#myLibraryReservationContents #resultCards .searchCard')
            return self.parse_books_result_cards(books_elem)
        else:
            raise LimedioLoginError()

    def search(self, query: str):
        url = f'{self.prefix}/opac/search?q={query}'
        res = self.session.get(url)
        if res.status_code == 200 and res.url == url:
            html = res.text
            doc = bs4.BeautifulSoup(html, 'html.parser')
            books_elem = doc.select('#resultCards .searchCard')
            return self.parse_books_result_cards(books_elem)
        else:
            raise LimedioLoginError()

    def parse_books_result_cards(self, books_elem):
        books = []
        for book_elem in books_elem:
            book = self.parse_book_search_card(book_elem)
            books.append(book)
        return books

    def parse_book_search_card(self, book_elem):
        book = {}
        title = book_elem.select_one('.informationArea h3').text.strip()
        book['title'] = title
        for dl in book_elem.select('.informationArea dl'):
            key_elem = dl.select_one('dt')
            value_elem = dl.select_one('dd')
            if key_elem and value_elem:
                key = key_elem.text.strip()
                value = value_elem.text.strip()
                book[self.ja_to_en(key)] = value
        return book

    def ja_to_en(self, key):
        return {
            '著者': 'author',
            '出版社': 'publisher',
            '年月情報': 'publish_date',
            '資料ID': 'id',
            '返却予定': 'due_date',
            '延長回数': 'count',
            '著者名': 'author',
            '出版': 'publisher',
            'ISBN':	'isbn',
            '所蔵': 'location',
            '状況': 'status',
        }[key]

    def format_books_search(self, books):
        result = ''
        for i, book in enumerate(books):
            result += f"[{i}] {book.get('title')}\t{book.get('status')}\n"
        return result
