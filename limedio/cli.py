import argparse
from limedio.errors import LimedioLoginError

from limedio.limedio import LimedioLibrary


class Authenticator():
    def login(self) -> LimedioLibrary:
        '''
        use refresh() instead on exception
        '''
        pass

    def refresh(self) -> LimedioLibrary:
        '''
        refresh
        '''
        pass


def _default_handler(args, next_handler, *, authenticator: Authenticator):
    try:
        limedio = authenticator.login()
    except:
        limedio = authenticator.refresh()

    for _ in range(3):
        try:
            next_handler(args, limedio)
            break
        except Exception as e:
            print(e)
            if 'n' == input('refresh (Y/n)'):
                break
            limedio = authenticator.refresh()


def status_handler(args, limedio):
    for i, book in enumerate(limedio.borrowing()):
        print(f'[{i}] {book["due_date"]}\t{book["title"]}')


def search_handler(args, limedio):
    books = limedio.search(args.query)
    string = limedio.format_books_search(books)
    print(string.strip())


def get_parser(*, authenticator):
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    status_parser = subparsers.add_parser('status')
    status_parser.set_defaults(handler=lambda args: _default_handler(args, status_handler, authenticator=authenticator))

    search_parser = subparsers.add_parser('search')
    search_parser.add_argument('query')
    search_parser.set_defaults(handler=lambda args: _default_handler(args, search_handler, authenticator=authenticator))
    return parser


def parse_args_with_handler(parser: argparse.ArgumentParser):
    args = parser.parse_args()
    if hasattr(args, 'handler'):
        args.handler(args)
    else:
        parser.print_help()
