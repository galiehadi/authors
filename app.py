from flask import Flask, request, jsonify
from flask_cors import CORS
from cachetools import TTLCache
import pandas as pd
from sqlalchemy import create_engine
import service.config as config

app = Flask(__name__)
CORS(app, supports_credentials=True)

# Setup database connection
_USER_ = config._USER_
_PASS_ = config._PASS_
_IP_ = config._IP_
_DB_NAME_ = config._DB_NAME_
con = f"mysql+mysqlconnector://{_USER_}:{_PASS_}@{_IP_}/{_DB_NAME_}"
engine = create_engine(con)

# Setup caching
cache = TTLCache(maxsize=100, ttl=300)  # Cache with max size 100 and TTL of 300 seconds (5 minutes)

# =============================== Authors Routes =============================== #

@app.route('/service/library/authors')
def all_authors():
    cache_key = 'all_authors'
    data = cache.get(cache_key)

    if data is None:
        try:
            q = """SELECT id, name, bio, birth_date FROM authors"""
            df = pd.read_sql(q, engine)
            data = df.to_dict('records')
            cache[cache_key] = data
        except Exception as e:
            data = {"error": str(e)}

    return jsonify(data)

@app.route('/service/library/authors/<authorsId>')
def specific_authors(authorsId):
    cache_key = f'specific_authors_{authorsId}'
    data = cache.get(cache_key)

    if data is None:
        try:
            q = f"""SELECT id, name, bio, birth_date FROM authors WHERE id = {authorsId}"""
            df = pd.read_sql(q, engine)
            if len(df) > 0:
                data = df.iloc[0].to_dict()
                cache[cache_key] = data
            else:
                data = {}
        except Exception as e:
            data = {"error": str(e)}

    return jsonify(data)

@app.route('/service/library/authors', methods=['POST'])
def add_authors():
    payload = request.get_json()
    name = payload['name']
    bio = payload['bio']
    birth_date = payload['birth_date']

    try:
        q = f"""INSERT INTO authors (name, bio, birth_date) VALUES ('{name}', '{bio}', '{birth_date}')"""
        with engine.connect() as conn:
            conn.execute(q)
        
        cache.clear()
        return jsonify({"message": "Success"})
    except Exception as e:
        return jsonify({"message": "Failed", "error": str(e)})

@app.route('/service/library/authors/update', methods=['PUT'])
def update_authors():
    payload = request.get_json()
    author_id = payload['id']
    name = payload['name']
    bio = payload['bio']
    birth_date = payload['birth_date']

    try:
        q = f"""UPDATE authors SET name = '{name}', bio = '{bio}', birth_date = '{birth_date}' WHERE id = {author_id}"""
        with engine.connect() as conn:
            conn.execute(q)
        
        cache.clear()
        return jsonify({"message": "Success"})
    except Exception as e:
        return jsonify({"message": "Failed", "error": str(e)})

@app.route('/service/library/authors/delete/<id>', methods=['DELETE'])
def delete_authors(id):
    try:
        q = f"""DELETE FROM authors WHERE id = {id}"""
        with engine.connect() as conn:
            conn.execute(q)
        
        cache.clear()
        return jsonify({"message": "Success"})
    except Exception as e:
        return jsonify({"message": "Failed", "error": str(e)})

# =============================== Books Routes =============================== #

@app.route('/service/library/books')
def all_books():
    cache_key = 'all_books'
    data = cache.get(cache_key)

    if data is None:
        try:
            q = """SELECT id, title, description, publish_date, author_id FROM books"""
            df = pd.read_sql(q, engine)
            data = df.to_dict('records')
            cache[cache_key] = data
        except Exception as e:
            data = {"error": str(e)}

    return jsonify(data)

@app.route('/service/library/books/<bookId>')
def specific_books(bookId):
    cache_key = f'specific_books_{bookId}'
    data = cache.get(cache_key)

    if data is None:
        try:
            q = f"""SELECT id, title, description, publish_date, author_id FROM books WHERE id = {bookId}"""
            df = pd.read_sql(q, engine)
            if len(df) > 0:
                data = df.iloc[0].to_dict()
                cache[cache_key] = data
            else:
                data = {}
        except Exception as e:
            data = {"error": str(e)}

    return jsonify(data)

@app.route('/service/library/books', methods=['POST'])
def add_books():
    payload = request.get_json()
    title = payload['title']
    description = payload['description']
    publish_date = payload['publish_date']
    author_id = payload['author_id']

    try:
        q = f"""INSERT INTO books (title, description, publish_date, author_id) 
                VALUES ('{title}', '{description}', '{publish_date}', {author_id})"""
        with engine.connect() as conn:
            conn.execute(q)
        
        cache.clear()
        return jsonify({"message": "Success"})
    except Exception as e:
        return jsonify({"message": "Failed", "error": str(e)})

@app.route('/service/library/books/update', methods=['PUT'])
def update_books():
    payload = request.get_json()
    book_id = payload['id']
    title = payload['title']
    description = payload['description']
    publish_date = payload['publish_date']
    author_id = payload['author_id']

    try:
        q = f"""UPDATE books 
                SET title = '{title}', description = '{description}', 
                    publish_date = '{publish_date}', author_id = {author_id}
                WHERE id = {book_id}"""
        with engine.connect() as conn:
            conn.execute(q)
        
        cache.clear()
        return jsonify({"message": "Success"})
    except Exception as e:
        return jsonify({"message": "Failed", "error": str(e)})

@app.route('/service/library/books/delete/<id>', methods=['DELETE'])
def delete_books(id):
    try:
        q = f"""DELETE FROM books WHERE id = {id}"""
        with engine.connect() as conn:
            conn.execute(q)
        
        cache.clear()
        return jsonify({"message": "Success"})
    except Exception as e:
        return jsonify({"message": "Failed", "error": str(e)})

# =============================== Utility Routes =============================== #

@app.route('/service/library/all/data')
def all_data():
    try:
        q = """SELECT 
                a.id as author_id, a.name as author_name, a.bio as author_bio, a.birth_date as author_birth_date,
                b.id as book_id, b.title as book_title, b.description as book_description, b.publish_date as book_publish_date
                FROM authors a
                LEFT JOIN books b ON a.id = b.author_id"""
        df = pd.read_sql(q, engine)
        authors = {}
        for row in df.itertuples(index=False):
            author_id = row.author_id
            if author_id not in authors:
                authors[author_id] = {
                    "author_id": author_id,
                    "name": row.author_name,
                    "bio": row.author_bio,
                    "birth_date": row.author_birth_date,
                    "books": []
                }
            
            if pd.notna(row.book_id):  # Check if there are book details
                book = {
                    "book_id": row.book_id,
                    "title": row.book_title,
                    "description": row.book_description,
                    "publish_date": row.book_publish_date
                }
                authors[author_id]["books"].append(book)
        
        data = list(authors.values())
        return jsonify({"message": "Success", "data": data})
    except Exception as e:
        return jsonify({"message": "Failed", "error": str(e)})

# ============================================================================ #

if __name__ == '__main__':
    app.run('0.0.0.0', port=8083, debug=False)
