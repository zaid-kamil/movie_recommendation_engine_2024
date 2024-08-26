from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from helpers import movie_data_from_tmdb
from mre import *

app = Flask(__name__)
app.secret_key = 'supersecretmre'


@app.route('/')
def index():
    flash('Welcome to the Flask App', 'info')
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/recommender', methods=['GET','POST'])
def forminput():
    return render_template('form.html')

@app.route('/results', methods=['GET','POST'])
def result():
    if request.method == 'POST':
        name = request.form['name']
        by = request.form['by']
        count = request.form['count']
        print(f'name: {name}, by: {by}, count: {count}')
        count = int(count)
        match by:
            case 'name':
                movies = get_recommendation(name, count=count)
            case 'word':
                movies = get_recommendation(name, by=by, count=count)
        if not movies:
            flash('No movies available', 'danger')
            return redirect(url_for('forminput'))
        
        if movies == 'Movie not found':
            flash('Movie not found', 'danger')
            return redirect(url_for('forminput'))
        else:
            results = [movie_data_from_tmdb(movie) for movie in movies]
            return render_template('results.html', name=name, by=by, count=count, results=results)
    return redirect(url_for('forminput'))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)