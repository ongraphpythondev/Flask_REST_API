import datetime
from flask import Flask , request 
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:1234@localhost/flask_rest"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)

api = Api(app)

class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    author = db.Column(db.String())
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, name, author):
        self.name = name
        self.author = author

    def __repr__(self):
        return f"id = {self.id} name = {self.name}"
    
# created schema
class BookSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Book
        fields = ("id", "name", "author" , "created")


# inicialize
book_schema = BookSchema()
books_schema = BookSchema(many=True)


# routing
class AllBooks(Resource):
    def get(self):
        book_obj = Book.query.all()
        return books_schema.dump(book_obj)
    
    def post(self):
        name = request.json["name"]
        author = request.json["author"]
        book_obj = Book(name = name , author = author)
        db.session.add(book_obj)
        db.session.commit()

        return book_schema.dump(book_obj)


class PerticularBook(Resource):
    def get_obj(self ,pk):
        book_obj = Book.query.filter_by(id=pk).first()
        return book_obj

    def get(self , pk):
        book_obj = self.get_obj(pk)
        return book_schema.dump(book_obj)
    
    def put(self , pk):
        book_obj = self.get_obj(pk)
        name = request.json["name"]
        author = request.json["author"]
        book_obj.name = name
        book_obj.author = author
        db.session.commit()

        return book_schema.dump(book_obj)

    def delete(self , pk):
        book_obj = self.get_obj(pk)
        db.session.delete(book_obj)
        db.session.commit()

        return book_schema.dump(book_obj)
        


api.add_resource(AllBooks, '/book')
api.add_resource(PerticularBook, '/book/<int:pk>')

if __name__ == '__main__':
    app.run(debug=True)