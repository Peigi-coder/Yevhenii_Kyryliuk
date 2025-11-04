from flask import Flask, jsonify, request, abort
try:
    datetime.fromisoformat(data['published_date'])
except:
    abort(400, description='Field "published_date" must be YYYY-MM-DD')




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
pages=int(data.get('pages', 0))
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
if 'title' in data: b.title = data['title']
if 'author' in data: b.author = data['author']
if 'pages' in data: b.pages = int(data['pages'])
if 'genre' in data: b.genre = data['genre'].strip()
if 'rating' in data: b.rating = float(data['rating'])

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
app.run(debug=True)
