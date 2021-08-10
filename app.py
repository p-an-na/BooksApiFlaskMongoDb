from bson import ObjectId
from flask import Flask, send_from_directory, jsonify, request, Response, render_template
from flask_pymongo import PyMongo
from flask_restful import Api
from flask_swagger_ui import get_swaggerui_blueprint

import request_api
from database.db import initialize_db
from resources import api_client

from utils.config_read import configReader

app = Flask(__name__)
api = Api(app)
app.debug = True

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.yml'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': 'Books Rest Api'
    }
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
app.register_blueprint(request_api.get_blueprint())




config = configReader()
app.secret_key = config['app']['secret_key']
app.config['MONGO_DBNAME'] = 'Booksdb'
app.config['MONGO_URI'] = config['database']['db_endpoint']
mongodb = PyMongo(app)

initialize_db(app)

@app.route("/", methods = ["GET"])
def get():
    return render_template('index.html')

@app.route("/books/addbook", methods=["POST"])
def add_new_book():
    book_id = api_client.post_new_book()
    return jsonify(book_id)


@app.route("/books", methods=["GET"])
def get_books():
    output = api_client.get_all_books()
    return jsonify({"result": output})

@app.route("/books/authors/<authors>", methods=["GET"])
def get_book_by_authors(authors):
    output = api_client.get_authors(authors)
    return jsonify({'result': output})

@app.route("/books/title/<title>", methods=["GET"])
def get_book_by_title(title):
    output = api_client.get_title(title)
    return jsonify({'result': output})

@app.route("/books/category/<categories>", methods=["GET"])
def get_book_by_category(categories):
    output = api_client.get_category(categories)
    return jsonify({'result': output})


@app.route("/books/id/<id>", methods=["GET", "DELETE"])
def get_by_id(id):
    if request.method == "GET":
        output = api_client.book_by_id(id)
        return jsonify({'result': output})

    elif request.method == "DELETE":
        output = api_client.delete(id)
        return jsonify({'result': output})

@app.route("/books/id", methods=["PUT"])
def update_book():
    id = request.json['id']
    output = api_client.put(id)
    return jsonify({'result': output})


#@app.route("/books/id/<id>", methods=["DELETE"])
#def delete():
  #  output = api_client.delete(id)
   # return jsonify({'result': output})







if __name__ == "__main__":
    app.run(debug=True)