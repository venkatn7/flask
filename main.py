from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector://root:c1Hf-Gfc1hf5fhc--DAhA6HFfbEf6Cbg@mysql:3306/railway"
import os

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    # books = db.relationship("Book", backref="authors", lazy='dynamic')
    # book_id = db.Column(db.Integer, db.ForeignKey("book.id"))


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    author_id = db.Column(db.Integer, db.ForeignKey("author.id"))
    author = db.relationship("Author", backref="books")

    def __int__(self, title: str):
        self.title = title


class BookSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Book
        # include_fk = True

class AuthorSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Author


    books = ma.Nested("BookSchema", many=True)

# Creation of the database tables within the application context.
with app.app_context():
    db.create_all()

author_schema = AuthorSchema(many=True)
book_schema = BookSchema(many=True)


# enable CORS
CORS(app, resources={r'/*': {'origin': '*'}})

@app.route('/', methods=["POST"])
def hello_world():  # put application's code here
    author = Author(name="Venkat")
    book = Book(title="Test your Code!", author=author)
    db.session.add(author)
    db.session.add(book)
    db.session.commit()
    result = author_schema.dump(author)
    return jsonify({'return': result})


@app.route('/', methods=["GET"])
def get_hello_world():
    queryDB = Author.query.all()
    result = author_schema.dump(queryDB)
    print(result)
    return jsonify(result)

# if __name__ == '__main__':
#     app.run(debug=True)
#
#
# @app.route('/')
# def index():
#     return jsonify({"Choo Choo": "Welcome to your Flask app 🚅"})


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
