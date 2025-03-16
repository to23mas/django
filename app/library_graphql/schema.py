import graphene
from graphene_django import DjangoObjectType
from library_rest.models import Book  # Reusing the Book model from library_rest

class BookType(DjangoObjectType):
    class Meta:
        model = Book
        fields = ('id', 'title', 'author', 'isbn', 'pages', 'published_date', 'created_at', 'updated_at')

class Query(graphene.ObjectType):
    all_books = graphene.List(BookType)
    book = graphene.Field(BookType, id=graphene.Int())

    def resolve_all_books(self, info):
        return Book.objects.all()

    def resolve_book(self, info, id):
        return Book.objects.get(pk=id)

class CreateBook(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        author = graphene.String(required=True)
        isbn = graphene.String(required=True)
        pages = graphene.Int(required=True)
        published_date = graphene.String(required=True)

    book = graphene.Field(BookType)

    def mutate(self, info, title, author, isbn, pages, published_date):
        book = Book.objects.create(
            title=title,
            author=author,
            isbn=isbn,
            pages=pages,
            published_date=published_date
        )
        return CreateBook(book=book)

class UpdateBook(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        title = graphene.String()
        author = graphene.String()
        isbn = graphene.String()
        pages = graphene.Int()
        published_date = graphene.String()

    book = graphene.Field(BookType)

    def mutate(self, info, id, **kwargs):
        book = Book.objects.get(pk=id)
        for key, value in kwargs.items():
            if value is not None:
                setattr(book, key, value)
        book.save()
        return UpdateBook(book=book)

class DeleteBook(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    def mutate(self, info, id):
        try:
            Book.objects.get(pk=id).delete()
            return DeleteBook(success=True)
        except Book.DoesNotExist:
            return DeleteBook(success=False)

class Mutation(graphene.ObjectType):
    create_book = CreateBook.Field()
    update_book = UpdateBook.Field()
    delete_book = DeleteBook.Field()

schema = graphene.Schema(query=Query, mutation=Mutation) 