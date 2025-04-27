import graphene

books = [
	{
		"id": 1,
		"title": "The Great Gatsby",
		"author": "F. Scott Fitzgerald",
		"isbn": "9780743273565",
		"pages": 180,
		"published_date": "1925-04-10",
	},
	{
		"id": 2,
		"title": "To Kill a Mockingbird",
		"author": "Harper Lee",
		"isbn": "9780446310789",
		"pages": 281,
		"published_date": "1960-07-11",
	},
	{
		"id": 3,
		"title": "1984",
		"author": "George Orwell",
		"isbn": "9780451524935",
		"pages": 328,
		"published_date": "1949-06-08",
	}
]

class BookType(graphene.ObjectType):
	id = graphene.Int()
	title = graphene.String()
	author = graphene.String()
	isbn = graphene.String()
	pages = graphene.Int()
	published_date = graphene.String()

class Query(graphene.ObjectType):
	all_books = graphene.List(BookType)
	book = graphene.Field(BookType, id=graphene.Int())

	def resolve_all_books(self, info):
		return [BookType(**book) for book in books]

	def resolve_book(self, info, id):
		for book in books:
			if book["id"] == id:
				return BookType(**book)
		return None

class CreateBook(graphene.Mutation):
	class Arguments:
		title = graphene.String(required=True)
		author = graphene.String(required=True)
		isbn = graphene.String(required=True)
		pages = graphene.Int(required=True)
		published_date = graphene.String(required=True)

	book = graphene.Field(BookType)

	def mutate(self, info, title, author, isbn, pages, published_date):
		new_id = max(book["id"] for book in books) + 1
		new_book = {
			"id": new_id,
			"title": title,
			"author": author,
			"isbn": isbn,
			"pages": pages,
			"published_date": published_date,
		}
		books.append(new_book)
		return CreateBook(book=BookType(**new_book))

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
		for book in books:
			if book["id"] == int(id):
				book.update({k: v for k, v in kwargs.items() if v is not None})
				return UpdateBook(book=BookType(**book))
		return None

class DeleteBook(graphene.Mutation):
	class Arguments:
		id = graphene.ID(required=True)

	success = graphene.Boolean()

	def mutate(self, info, id):
		original_length = len(books)
		books[:] = [b for b in books if b["id"] != int(id)]
		return DeleteBook(success=len(books) < original_length)

class Mutation(graphene.ObjectType):
	create_book = CreateBook.Field()
	update_book = UpdateBook.Field()
	delete_book = DeleteBook.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
