from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .library_rest import BOOKS  # Reuse the same data store
import graphene
from graphene_django.views import GraphQLView
from datetime import datetime

# Mock data store
books = [
    {"id": 1, "title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "isbn": "9780743273565", "pages": 180, "published_date": "1925-04-10"},
    {"id": 2, "title": "To Kill a Mockingbird", "author": "Harper Lee", "isbn": "9780446310789", "pages": 281, "published_date": "1960-07-11"},
    {"id": 3, "title": "1984", "author": "George Orwell", "isbn": "9780451524935", "pages": 328, "published_date": "1949-06-08"},
]

class Book(graphene.ObjectType):
    id = graphene.Int()
    title = graphene.String()
    author = graphene.String()
    isbn = graphene.String()
    pages = graphene.Int()
    published_date = graphene.String()

class Query(graphene.ObjectType):
    books = graphene.List(Book)
    book = graphene.Field(Book, id=graphene.Int(required=True))

    def resolve_books(self, info):
        return books

    def resolve_book(self, info, id):
        for book in books:
            if book["id"] == id:
                return book
        return None

class CreateBook(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        author = graphene.String(required=True)
        isbn = graphene.String(required=True)
        pages = graphene.Int(required=True)
        published_date = graphene.String(required=True)

    book = graphene.Field(Book)

    def mutate(self, info, title, author, isbn, pages, published_date):
        new_id = max(book["id"] for book in books) + 1
        new_book = {
            "id": new_id,
            "title": title,
            "author": author,
            "isbn": isbn,
            "pages": pages,
            "published_date": published_date
        }
        books.append(new_book)
        return CreateBook(book=new_book)

class Mutation(graphene.ObjectType):
    create_book = CreateBook.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)

# Use the built-in GraphQLView
graphql_view = csrf_exempt(GraphQLView.as_view(graphiql=True, schema=schema))

def reset_data(request):
    global books
    books = [
        {"id": 1, "title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "isbn": "9780743273565", "pages": 180, "published_date": "1925-04-10"},
        {"id": 2, "title": "To Kill a Mockingbird", "author": "Harper Lee", "isbn": "9780446310789", "pages": 281, "published_date": "1960-07-11"},
        {"id": 3, "title": "1984", "author": "George Orwell", "isbn": "9780451524935", "pages": 328, "published_date": "1949-06-08"},
    ]
    return JsonResponse({"message": "Data reset successfully", "books": books})

@csrf_exempt
def graphql_endpoint(request: HttpRequest, course: str, demo_id: int) -> JsonResponse:
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            query = data.get('query', '')
            
            # Simple query handling
            if 'allBooks' in query:
                return JsonResponse({'data': {'books': list(BOOKS.values())}})
            elif 'book(' in query:
                # Extract book ID from query
                book_id = int(query.split('book(id: ')[1].split(')')[0])
                if book_id in BOOKS:
                    return JsonResponse({'data': {'book': BOOKS[book_id]}})
                return JsonResponse({'errors': [{'message': 'Book not found'}]})
            elif 'createBook' in query:
                # Extract book data from mutation
                variables = data.get('variables', {})
                if variables:
                    global NEXT_ID
                    new_book = {
                        'id': NEXT_ID,
                        'title': variables['title'],
                        'author': variables['author'],
                        'isbn': variables['isbn'],
                        'pages': variables['pages'],
                        'published_date': variables['publishedDate']
                    }
                    BOOKS[NEXT_ID] = new_book
                    NEXT_ID += 1
                    return JsonResponse({'data': {'createBook': new_book}})
            
            return JsonResponse({'errors': [{'message': 'Invalid query'}]})
            
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            return JsonResponse({'errors': [{'message': str(e)}]}, status=400)
            
    return JsonResponse({'errors': [{'message': 'Method not allowed'}]}, status=405) 