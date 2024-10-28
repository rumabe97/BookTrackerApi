from googleapiclient.discovery import build
from config import settings

service = build('books', 'v1', developerKey=settings.GOOGLE_API_KEY)


def fetch_book_data_from_google_books(idGoogle):
    request = service.volumes().get(volumeId=idGoogle)
    response = request.execute()
    print(response)
    book_info = response['volumeInfo']
    if book_info is None: return None
    return complete_book_information(book_info, idGoogle)


def fetch_books_data_from_google_books(title, author, start_index, max_results):
    query = f'intitle:{title}'
    if author:
        query += f'+inauthor:{author}'

    request = service.volumes().list(
        q=query,
        langRestrict='es',
        maxResults=max_results,
        startIndex=start_index
    )
    response = request.execute()
    result = []
    for item in response.get('items', []):
        result.append(complete_book_information(item['volumeInfo'], item['id']))

    return result


def search_newest_books(subject, order, start_index, max_results):
    query = 'subject:' + subject
    results = service.volumes().list(
        q=query,
        langRestrict='es',
        orderBy=order,
        maxResults=max_results,
        startIndex=start_index
    ).execute()

    result = []
    for item in results.get('items', []):
        result.append(complete_book_information(item['volumeInfo'], item['id']))

    return result


def complete_book_information(book_info, idGoogle):
    isbn_13, isbn_10 = get_isbn(book_info)
    return {
        'title': book_info.get('title'),
        'subTitle': book_info.get('subtitle'),
        'description': book_info.get('description'),
        'author': ', '.join(book_info.get('authors', [])),
        'genre': ', '.join(book_info.get('categories', [])),
        'pages': book_info.get('pageCount'),
        'coverImage': book_info.get('imageLinks', {}).get('thumbnail', ''),
        'publishedDate': book_info.get('publishedDate'),
        'description': book_info.get('description', ''),
        'averageRating': book_info.get('averageRating'),
        'isbn13': isbn_13,
        'isbn10': isbn_10,
        'idGoogle': idGoogle
    }


def get_isbn(book_info):
    isbn_13 = None
    isbn_10 = None

    identifiers = book_info.get('industryIdentifiers', [])

    for identifier in identifiers:
        if identifier.get('type') == 'ISBN_13':
            isbn_13 = identifier.get('identifier')
        elif identifier.get('type') == 'ISBN_10':
            isbn_10 = identifier.get('identifier')
    return isbn_13, isbn_10


def healthcheckApi():
    query = 'test'
    result = service.volumes().list(
        q=query,
        maxResults=1
    ).execute()

    if not result or "items" not in result:
        return False

    return True
