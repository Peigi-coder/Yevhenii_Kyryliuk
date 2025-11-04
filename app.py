from flask import Flask, jsonify, request, abort, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

@app.route('/')
def home():
    return render_template('index.html')

class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    published_date = db.Column(db.Date)
    pages = db.Column(db.Integer, default=0)
    genre = db.Column(db.String(100))
    rating = db.Column(db.Float, default=0.0)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'published_date': self.published_date.isoformat() if self.published_date else None,
            'pages': self.pages,
            'genre': self.genre,
            'rating': self.rating
        }


def _validate_book_payload(data, partial=False):
    if not data:
        abort(400, description='Brak danych JSON.')
    if not partial:
        if 'title' not in data or 'author' not in data:
            abort(400, description='Brak wymaganych pól: title i author.')
    if 'published_date' in data and data['published_date']:
        try:
            datetime.fromisoformat(data['published_date'])
        except:
            abort(400, description='Pole "published_date" musi być w formacie YYYY-MM-DD')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/books', methods=['GET'])
def list_books():
    return jsonify([b.to_dict() for b in Book.query.all()]), 200


@app.route('/api/books/<int:id>', methods=['GET'])
def get_book(id):
    b = Book.query.get_or_404(id)
    return jsonify(b.to_dict()), 200


@app.route('/api/books', methods=['POST'])
def create_book():
    data = request.get_json()
    _validate_book_payload(data)
    b = Book(
        title=data['title'].strip(),
        author=data['author'].strip(),
        published_date=datetime.fromisoformat(data['published_date']).date() if data.get('published_date') else None,
        pages=int(data.get('pages', 0)),
        genre=data.get('genre', '').strip(),
        rating=float(data.get('rating', 0))
    )
    db.session.add(b)
    db.session.commit()
    return jsonify(b.to_dict()), 201


@app.route('/api/books/<int:id>', methods=['PUT'])
def update_book(id):
    b = Book.query.get_or_404(id)
    data = request.get_json()
    _validate_book_payload(data, partial=True)

    if 'title' in data:
        b.title = data['title']
    if 'author' in data:
        b.author = data['author']
    if 'pages' in data:
        b.pages = int(data['pages'])
    if 'genre' in data:
        b.genre = data['genre'].strip()
    if 'rating' in data:
        b.rating = float(data['rating'])
    if 'published_date' in data:
        b.published_date = datetime.fromisoformat(data['published_date']).date() if data['published_date'] else None

    db.session.commit()
    return jsonify(b.to_dict()), 200


@app.route('/api/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    b = Book.query.get_or_404(id)
    db.session.delete(b)
    db.session.commit()
    return ('', 204)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000)
