from bson import ObjectId
from flask import Response, request, jsonify
from app import mongodb


def get_all_books():
    book = mongodb.db.books
    books = book.find()
    output = []
    for b in book.find():
        output.append({'book': str(b)})
    return output

def post_new_book():
    book = mongodb.db.books
    title = request.json["title"]
    authors = request.json["authors"]
    publisher = request.json["publisher"]
    description = request.json["description"]
    category = request.json["categories"]
    price = request.json["price"]

    find_title = book.find_one({'title': title})
    find_authors = book.find_one({'authors': authors})

    if find_authors and find_title != None:
        return ("Book exist in database.")

    book_id = book.insert({"title" : title, "authors": authors, "publisher": publisher, "description": description, "categories": category, "price": price})
    return ('Sucesfully added new book. ID: ' + str(book_id))

def book_by_id(id):
    book = mongodb.db.books
    find = book.find({'_id': ObjectId(id)})
    output=[]
    for i in find:
        if i:
            output.append({'book': str(i)})

    if output != []:
        return output
    else:
        return ("ID not found")

def put(id):
    book = mongodb.db.books
    title = request.json["title"]
    authors = request.json["authors"]
    publisher = request.json["publisher"]
    description = request.json["description"]
    category = request.json["categories"]
    price = request.json["price"]
    book_update = book.update_one({'_id': ObjectId(id)},{"$set":{"title" : title, "authors": authors, "publisher": publisher, "description": description, "categories": category, "price": price}})
    find = book.find({'_id': ObjectId(id)})
    output = []
    for i in find:
        if i:
            output.append({'book': str(i)})

    if output != []:
        return ('Sucesfully updated the book.', output)
    else:
        return ("Someting went wrong.")

def delete(id):
    book = mongodb.db.books
    find = book.delete_one({'_id': ObjectId(id)})

    if find.deleted_count == 1:
        return ("Sucesfully deleted book ID:" + id)
    else:
        return ("Error")


def get_authors(authors):
    book = mongodb.db.books
    find = book.find({'authors':authors})
    output=[]
    for a in find:
        if a:
            output.append({'book': str(a)})
    if output != []:
        return  output
    else:
        return ("Author not found")

def get_title(title):
    book = mongodb.db.books
    find = book.find({'title':title})
    output=[]
    for t in find:
        if t:
            output.append({'book': str(t)})
    if output != []:
        return  output
    else:
        return ("Title not found")

def get_category(category):
    book = mongodb.db.books
    find = book.find({'categories': category})
    output=[]
    for c in find:
        if c:
            output.append({'book': str(c)})
    if output != []:
        return  output
    else:
        return ("Category not found")


