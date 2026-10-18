
from flask import jsonify, request
from app import app, db
from app.models import Movie

@app.route('/api/movies/', methods=['GET'])
def get_movies():
    title = request.args.get('title')
    if title:
        movies = Movie.query.filter(Movie.title.ilike(f'%{title}%')).all()
    else:
        movies = Movie.query.all()
    return jsonify([{'id': m.id, 'title': m.title, 'description': m.description} for m in movies])

@app.route('/api/movies/', methods=['POST'])
def create_movie():
    data = request.json
    new_movie = Movie(title=data['title'], description=data.get('description'))
    db.session.add(new_movie)
    db.session.commit()
    return jsonify({'id': new_movie.id, 'title': new_movie.title, 'description': new_movie.description}), 201

@app.route('/api/movies/', methods=['DELETE'])
def delete_all_movies():
    Movie.query.delete()
    db.session.commit()
    return '', 204

@app.route('/api/movies/<int:id>', methods=['GET'])
def get_movie(id):
    movie = Movie.query.get_or_404(id)
    return jsonify({'id': movie.id, 'title': movie.title, 'description': movie.description})

@app.route('/api/movies/<int:id>', methods=['PUT'])
def update_movie(id):
    movie = Movie.query.get_or_404(id)
    data = request.json
    movie.title = data.get('title', movie.title)
    movie.description = data.get('description', movie.description)
    db.session.commit()
    return jsonify({'id': movie.id, 'title': movie.title, 'description': movie.description})

@app.route('/api/movies/<int:id>', methods=['DELETE'])
def delete_movie(id):
    movie = Movie.query.get_or_404(id)
    db.session.delete(movie)
    db.session.commit()
    return '', 204
